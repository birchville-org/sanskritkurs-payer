#!/usr/bin/env python3
"""
Security Audit Agent (Local QA)
-------------------------------
Gathers `npm audit` and `npm outdated` data and feeds it to a local
Ollama Gemma 4 model to generate a human-readable security report.
"""

import json
import subprocess
import urllib.request
import urllib.error
import sys

OLLAMA_URL = "http://localhost:11434/v1/chat/completions"
MODEL_NAME = "gemma4:12b-mlx"

def run_command(cmd):
    """Run a shell command and return stdout. Returns empty string on failure."""
    try:
        # npm audit exits with non-zero if vulnerabilities are found, so we must ignore exit codes.
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        return result.stdout
    except Exception as e:
        print(f"[!] Error running command '{cmd}': {e}")
        return ""

def auto_update_and_verify():
    """
    Attempts to update packages and verifies the build.
    Returns a status string to be included in the LLM prompt.
    """
    print("[*] Starte Auto-Update Phase...")
    
    print("[*] Führe 'npm update' aus...")
    subprocess.run("npm update", shell=True, capture_output=True, text=True)
    
    print("[*] Führe Build Gate ('npm run docs:build') aus...")
    build_res = subprocess.run("npm run docs:build", shell=True, capture_output=True, text=True)
    
    if build_res.returncode == 0:
        print("[*] Build Gate erfolgreich! Updates werden beibehalten.")
        return "Auto-Update war ERFOLGREICH. Das Projekt kompiliert nach 'npm update' fehlerfrei."
    else:
        print("[!] Build Gate FEHLGESCHLAGEN! Führe Rollback durch...")
        subprocess.run("git checkout package.json package-lock.json", shell=True)
        subprocess.run("npm install", shell=True)
        return "Auto-Update ist FEHLGESCHLAGEN. 'npm run docs:build' ist nach dem Update gecrasht. Ein Git-Rollback wurde automatisch durchgeführt, das System ist wieder im Ursprungszustand."

def gather_npm_data():
    print("[*] Running 'npm audit --json'...")
    audit_raw = run_command("npm audit --json")
    
    print("[*] Running 'npm outdated --json'...")
    outdated_raw = run_command("npm outdated --json")
    
    # Parse JSON
    audit_data = {}
    try:
        audit_data = json.loads(audit_raw)
    except Exception:
        print("[!] Warning: Could not parse npm audit JSON.")
        
    outdated_data = {}
    try:
        if outdated_raw.strip():
            outdated_data = json.loads(outdated_raw)
    except Exception:
        print("[!] Warning: Could not parse npm outdated JSON.")

    # Filter audit data to save tokens
    vulns = audit_data.get("vulnerabilities", {})
    metadata = audit_data.get("metadata", {}).get("vulnerabilities", {})
    
    # Filter outdated data
    # Only keep current, wanted, and latest versions
    filtered_outdated = {}
    for pkg, info in outdated_data.items():
        filtered_outdated[pkg] = {
            "current": info.get("current", "unknown"),
            "wanted": info.get("wanted", "unknown"),
            "latest": info.get("latest", "unknown")
        }

    return {
        "vulnerability_summary": metadata,
        "vulnerabilities": vulns,
        "outdated_packages": filtered_outdated
    }

def ask_gemma(prompt_data, update_status):
    system_prompt = (
        "Du bist ein Senior DevOps und Security Engineer. "
        "Analysiere die folgenden komprimierten JSON-Daten zu npm audit (Sicherheitslücken) "
        "und npm outdated (veraltete Pakete) für ein Web-Projekt.\n\n"
        f"WICHTIGE INFO ZUM AUTO-UPDATE:\n{update_status}\n\n"
        "Erstelle einen prägnanten, professionellen Markdown-Report auf Deutsch.\n\n"
        "Struktur:\n"
        "1. Zusammenfassung (Berichte kurz über den Status des Auto-Updates: Erfolgreich oder Rollback? Gibt es noch kritische Probleme?)\n"
        "2. Kritische Sicherheitslücken (falls vorhanden, nenne das Paket und das Risiko)\n"
        "3. Veraltete Pakete (fasse die wichtigsten Updates zusammen)\n"
        "4. Konkrete Handlungsempfehlung (Was muss der Entwickler noch manuell tun?)\n\n"
        "Antworte direkt mit dem Markdown-Report ohne weitere Begrüßung."
    )
    
    user_prompt = f"Hier sind die Rohdaten:\n```json\n{json.dumps(prompt_data, indent=2)}\n```"

    payload = {
        "model": MODEL_NAME,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        "temperature": 0.2, # Low temp for analytical tasks
        "max_tokens": 2048
    }
    
    headers = {"Content-Type": "application/json"}
    req = urllib.request.Request(OLLAMA_URL, data=json.dumps(payload).encode('utf-8'), headers=headers, method="POST")
    
    print(f"[*] Sende Daten an lokales Modell ({MODEL_NAME})...")
    try:
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read().decode('utf-8'))
            message = result.get("choices", [{}])[0].get("message", {})
            
            # Print reasoning if available (Gemma 4 specific)
            reasoning = message.get("reasoning", "")
            if reasoning:
                print("\n\033[90m--- Gemma Reasoning ---\n" + reasoning.strip() + "\n-----------------------\033[0m\n")
            
            return message.get("content", "")
    except urllib.error.URLError as e:
        print(f"[!] Fehler bei der Verbindung zu Ollama: {e}")
        return None

def send_email(report_markdown, target_email="marcodem@me.com"):
    """
    Sends the report using macOS Mail.app via AppleScript.
    It automatically addresses and sends the email in the background.
    """
    print(f"[*] Sende E-Mail automatisch an {target_email} über macOS Mail.app...")
    
    # We must escape quotes and backslashes for AppleScript
    safe_content = report_markdown.replace('\\', '\\\\').replace('"', '\\"')
    
    applescript = f'''
    tell application "Mail"
        set newMessage to make new outgoing message with properties {{subject:"Payer Projekt: Security & Update Audit", content:"{safe_content}", visible:false}}
        tell newMessage
            make new to recipient at end of to recipients with properties {{address:"{target_email}"}}
            send
        end tell
    end tell
    '''
    
    try:
        subprocess.run(["osascript", "-e", applescript], check=True)
        print("[*] E-Mail wurde erfolgreich versendet!")
    except subprocess.CalledProcessError as e:
        print(f"[!] Fehler beim Versenden der E-Mail: {e}")

if __name__ == "__main__":
    update_status = auto_update_and_verify()
    
    data = gather_npm_data()
    print("[*] Daten gesammelt. Analysiere...")
    
    report = ask_gemma(data, update_status)
    
    if report:
        print("\n" + "="*50)
        print("FINALER REPORT:")
        print("="*50)
        print(report)
        print("="*50 + "\n")
        
        send_email(report)
    else:
        print("[!] Konnte keinen Report generieren.")
