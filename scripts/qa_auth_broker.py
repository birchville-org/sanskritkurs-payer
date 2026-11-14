#!/usr/bin/env python3
"""
Zero-PAT GitHub API Broker for Payer QA Viewer behind Traefik + Authelia.
Reads Authelia identity headers (Remote-User, Remote-Name, Remote-Email, Remote-Groups)
and proxies authenticated lesson reads/writes to the GitHub REST API using a single
server-side GITHUB_TOKEN.
"""

import base64
import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN", "").strip()
GITHUB_REPO = os.environ.get("GITHUB_REPO", "birchville-org/sanskritkurs-payer").strip()
DRAFT_BRANCH = os.environ.get("QA_DRAFT_BRANCH", "author-drafts").strip()
BASE_BRANCH = os.environ.get("QA_BASE_BRANCH", "main").strip()
BROKER_HOST = os.environ.get("QA_BROKER_HOST", "127.0.0.1").strip()
BROKER_PORT = int(os.environ.get("QA_BROKER_PORT", "8081"))

ALLOWED_PATH_RE = re.compile(
    r"^docs/(?:([a-z]{2,3}(?:-[A-Z]{2})?)/)?(?:lektionen/)?(?:lektion|schrift|uebung|glossar|index)[a-z0-9_-]*\.md$"
)


def parse_groups(raw_groups: str) -> list[str]:
    if not raw_groups:
        return []
    return [g.strip().lower() for g in raw_groups.split(",") if g.strip()]


def check_write_permission(filepath: str, groups: list[str]) -> tuple[bool, str]:
    """
    Enforces LLDAP / Authelia group permissions and TOTALBREMSE:
    - lldap_strict_readonly: strictly read-only
    - admins / lldap_admin: full write access (including German master)
    - users / alexandria-users / authors: write access to translations only
    - lector-<lang>: write access restricted to docs/<lang>/...
    """
    m = ALLOWED_PATH_RE.match(filepath)
    if not m:
        return False, "Path not allowed by whitelist"

    lang_group = m.group(1)  # None if German master (docs/lektionen/...)
    is_german_master = lang_group is None

    if "lldap_strict_readonly" in groups:
        return False, "Read-only group (lldap_strict_readonly)"

    is_admin = "admins" in groups or "lldap_admin" in groups
    if is_admin:
        return True, "Admin access"

    if is_german_master:
        return False, "TOTALBREMSE: German master is restricted to admins"

    # Check specific lector-<lang> restrictions
    lector_langs = [g[len("lector-"):] for g in groups if g.startswith("lector-")]
    if lector_langs:
        if lang_group.lower() in lector_langs:
            return True, f"Lector access for {lang_group}"
        return False, f"Restricted to languages: {', '.join(lector_langs)}"

    # Standard authenticated author groups from LLDAP
    if any(g in groups for g in ("users", "alexandria-users", "authors", "editors")):
        return True, "Author access"

    return False, "No write-enabled group membership found"


def github_request(method: str, endpoint: str, body: dict | None = None) -> tuple[int, dict]:
    url = f"https://api.github.com/repos/{GITHUB_REPO}/{endpoint.lstrip('/')}"
    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json",
        "User-Agent": "Payer-QA-Broker/1.0",
    }
    data = None
    if body is not None:
        headers["Content-Type"] = "application/json"
        data = json.dumps(body).encode("utf-8")

    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            raw = resp.read().decode("utf-8")
            return resp.status, json.loads(raw) if raw else {}
    except urllib.error.HTTPError as e:
        raw = e.read().decode("utf-8", errors="replace")
        try:
            err_json = json.loads(raw)
        except Exception:
            err_json = {"message": raw}
        return e.code, err_json


def ensure_draft_branch() -> None:
    status, _ = github_request("GET", f"branches/{urllib.parse.quote(DRAFT_BRANCH)}")
    if status == 200:
        return
    status_main, main_data = github_request("GET", f"git/ref/heads/{urllib.parse.quote(BASE_BRANCH)}")
    if status_main != 200:
        raise RuntimeError(f"Could not resolve base branch {BASE_BRANCH}: {main_data}")
    sha = main_data["object"]["sha"]
    status_create, create_data = github_request(
        "POST",
        "git/refs",
        {"ref": f"refs/heads/{DRAFT_BRANCH}", "sha": sha},
    )
    if status_create not in (200, 201):
        raise RuntimeError(f"Could not create branch {DRAFT_BRANCH}: {create_data}")


class QABrokerHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        sys.stderr.write(f"[qa-broker] {self.address_string()} - {format % args}\n")

    def _send_json(self, status: int, payload: dict):
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def _get_identity(self) -> dict:
        user = (self.headers.get("Remote-User") or "").strip()
        name = (self.headers.get("Remote-Name") or user).strip()
        email = (self.headers.get("Remote-Email") or (f"{user}@birchville.org" if user else "")).strip()
        groups = parse_groups(self.headers.get("Remote-Groups") or "")
        is_admin = "admins" in groups or "lldap_admin" in groups
        can_write = bool(user) and ("lldap_strict_readonly" not in groups) and (
            is_admin
            or any(g in groups for g in ("users", "alexandria-users", "authors", "editors"))
            or any(g.startswith("lector-") for g in groups)
        )
        return {
            "authenticated": bool(user),
            "user": user,
            "name": name,
            "email": email,
            "groups": groups,
            "isAdmin": is_admin,
            "canWrite": can_write,
            "repo": GITHUB_REPO,
        }

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        if parsed.path == "/api/qa/me":
            identity = self._get_identity()
            self._send_json(200, identity)
            return

        if parsed.path == "/api/qa/file":
            identity = self._get_identity()
            if not identity["authenticated"]:
                self._send_json(401, {"error": "Authentication required (Authelia Remote-User missing)"})
                return

            qs = urllib.parse.parse_qs(parsed.query)
            filepath = (qs.get("path") or [""])[0].strip()
            if not ALLOWED_PATH_RE.match(filepath):
                self._send_json(403, {"error": f"Path not allowed: {filepath}"})
                return

            encoded_path = urllib.parse.quote(filepath)
            status, data = github_request("GET", f"contents/{encoded_path}?ref={urllib.parse.quote(DRAFT_BRANCH)}")
            branch_used = DRAFT_BRANCH
            if status != 200:
                status, data = github_request("GET", f"contents/{encoded_path}?ref={urllib.parse.quote(BASE_BRANCH)}")
                branch_used = BASE_BRANCH

            if status != 200:
                self._send_json(status, {"error": data.get("message", "File not found on GitHub")})
                return

            raw_b64 = data.get("content", "")
            content = base64.b64decode(raw_b64).decode("utf-8")
            self._send_json(
                200,
                {
                    "path": filepath,
                    "branch": branch_used,
                    "sha": data.get("sha"),
                    "content": content,
                },
            )
            return

        self._send_json(404, {"error": "Not found"})

    def do_PUT(self):
        parsed = urllib.parse.urlparse(self.path)
        if parsed.path != "/api/qa/file":
            self._send_json(404, {"error": "Not found"})
            return

        identity = self._get_identity()
        if not identity["authenticated"]:
            self._send_json(401, {"error": "Authentication required (Authelia Remote-User missing)"})
            return

        length = int(self.headers.get("Content-Length") or "0")
        if length <= 0 or length > 2_000_000:
            self._send_json(400, {"error": "Invalid payload size"})
            return

        try:
            body = json.loads(self.rfile.read(length).decode("utf-8"))
        except Exception:
            self._send_json(400, {"error": "Invalid JSON"})
            return

        filepath = (body.get("path") or "").strip()
        content = body.get("content")
        if not filepath or content is None:
            self._send_json(400, {"error": "Missing path or content"})
            return

        allowed, reason = check_write_permission(filepath, identity["groups"])
        if not allowed:
            self._send_json(403, {"error": f"Permission denied: {reason}"})
            return

        try:
            ensure_draft_branch()
            encoded_path = urllib.parse.quote(filepath)
            status_get, existing = github_request("GET", f"contents/{encoded_path}?ref={urllib.parse.quote(DRAFT_BRANCH)}")
            file_sha = existing.get("sha") if status_get == 200 else None

            b64_content = base64.b64encode(content.encode("utf-8")).decode("ascii")
            commit_payload = {
                "message": f"docs(qa): update {filepath} by {identity['user']}",
                "content": b64_content,
                "branch": DRAFT_BRANCH,
                "committer": {"name": "Payer QA Broker", "email": "qa-broker@birchville.org"},
                "author": {"name": identity["name"], "email": identity["email"]},
            }
            if file_sha:
                commit_payload["sha"] = file_sha

            status_put, put_res = github_request("PUT", f"contents/{encoded_path}", commit_payload)
            if status_put not in (200, 201):
                self._send_json(status_put, {"error": put_res.get("message", "GitHub commit failed")})
                return

            # Ensure open PR exists
            owner = GITHUB_REPO.split("/")[0]
            pr_url = None
            status_prs, prs = github_request(
                "GET",
                f"pulls?head={urllib.parse.quote(owner + ':' + DRAFT_BRANCH)}&base={urllib.parse.quote(BASE_BRANCH)}&state=open",
            )
            if status_prs == 200 and isinstance(prs, list):
                if len(prs) > 0:
                    pr_url = prs[0].get("html_url")
                else:
                    status_pr_create, pr_data = github_request(
                        "POST",
                        "pulls",
                        {
                            "title": "QA Lektorat / Autoren-Entwürfe",
                            "head": DRAFT_BRANCH,
                            "base": BASE_BRANCH,
                            "body": "Automatisch erstellter Pull Request aus dem Payer QA-Viewer (Authelia Zero-PAT Broker).",
                        },
                    )
                    if status_pr_create in (200, 201):
                        pr_url = pr_data.get("html_url")

            self._send_json(
                200,
                {
                    "ok": True,
                    "path": filepath,
                    "branch": DRAFT_BRANCH,
                    "commit": put_res.get("commit", {}).get("sha"),
                    "prUrl": pr_url,
                },
            )
        except Exception as e:
            self._send_json(500, {"error": str(e)})


def main():
    if not GITHUB_TOKEN:
        print("ERROR: GITHUB_TOKEN is not set. Exiting.", file=sys.stderr)
        sys.exit(1)
    server = ThreadingHTTPServer((BROKER_HOST, BROKER_PORT), QABrokerHandler)
    print(f"Payer QA Auth Broker listening on http://{BROKER_HOST}:{BROKER_PORT} (repo: {GITHUB_REPO})")
    server.serve_forever()


if __name__ == "__main__":
    main()
