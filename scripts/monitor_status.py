#!/usr/bin/env python3
"""Monitor script: translation progress + GSD phase status."""
import os, re, subprocess
from pathlib import Path
from datetime import datetime

ROOT = Path(__file__).parent.parent
DOCS = ROOT / "docs"

LANGS = {
    "de": ("Deutsch",  DOCS / "lektionen"),
    "en": ("English",  DOCS / "en/lektionen"),
    "it": ("Italiano", DOCS / "it/lektionen"),
    "es": ("Español",  DOCS / "es/lektionen"),
    "fr": ("Français", DOCS / "fr/lektionen"),
    "hi": ("हिंदी",    DOCS / "hi/lektionen"),
    "bg": ("Български",DOCS / "bg/lektionen"),
    "ru": ("Русский",  DOCS / "ru/lektionen"),
    "uk": ("Українська",DOCS/"uk/lektionen"),
    "ta": ("தமிழ்",    DOCS / "ta/lektionen"),
    "pa": ("ਪੰਜਾਬੀ",   DOCS / "pa/lektionen"),
    "la": ("Latina",   DOCS / "la/lektionen"),
    "rm": ("Rumantsch",DOCS / "rm/lektionen"),
    "ro": ("Română",   DOCS / "ro/lektionen"),
}

def count_files(d, pattern):
    if not d.exists():
        return 0
    return len(list(d.glob(pattern)))

def root_files(d):
    if not d.exists():
        return 0
    return len([f for f in d.glob("*.md")
                if not re.match(r'(lektion|schrift|uebung)\d', f.name)])

def status_bar(n, total, width=20):
    filled = int(width * n / total) if total else 0
    bar = "█" * filled + "░" * (width - filled)
    return f"[{bar}] {n:3}/{total}"

def check_translation_job():
    try:
        result = subprocess.run(
            ["pgrep", "-f", "lan_translate.py"],
            capture_output=True, text=True
        )
        pids = result.stdout.strip().split()
        if pids:
            # get elapsed time
            ps = subprocess.run(
                ["ps", "-p", pids[0], "-o", "etime="],
                capture_output=True, text=True
            )
            return f"läuft (PID {pids[0]}, {ps.stdout.strip()})"
        return "gestoppt"
    except Exception:
        return "unbekannt"

def get_phase_status():
    phases_dir = ROOT / ".planning/phases"
    if not phases_dir.exists():
        return []
    phases = []
    for d in sorted(phases_dir.iterdir()):
        if not d.is_dir():
            continue
        plans = list(d.glob("*-PLAN.md"))
        done = len([p for p in plans if p.name.startswith(tuple("0123456789")) and
                    "complete" in p.read_text(encoding="utf-8", errors="ignore").lower()[:200]])
        phases.append((d.name, len(plans), done))
    return phases

def get_state():
    state_file = ROOT / ".planning/STATE.md"
    if not state_file.exists():
        return {}
    text = state_file.read_text(encoding="utf-8")
    m = re.search(r'milestone:\s*(\S+)', text)
    s = re.search(r'status:\s*(\S+)', text)
    p = re.search(r'percent:\s*(\d+)', text)
    return {
        "milestone": m.group(1) if m else "?",
        "status": s.group(1) if s else "?",
        "percent": p.group(1) if p else "?",
    }

# ── Header ──────────────────────────────────────────────────────────────────
print()
now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
print("═" * 60)
print(f"  PAYER SANSKRITKURS — Monitor Status   {now}")
print("═" * 60)

# ── GSD State ───────────────────────────────────────────────────────────────
state = get_state()
print(f"\n  Milestone : {state.get('milestone','?')}  │  "
      f"Status: {state.get('status','?')}  │  "
      f"Fortschritt: {state.get('percent','?')}%\n")

# ── Übersetzungsjob ──────────────────────────────────────────────────────────
job = check_translation_job()
print(f"  Übersetzungsjob: {job}\n")

# ── Übersetzungsstatus ───────────────────────────────────────────────────────
print("  ── Übersetzungsstand ──────────────────────────────────")
print(f"  {'':4} {'Sprache':<12} {'Lektionen':>20}  {'Schriften':>14}  {'Übungen':>14}  Root")
print(f"  {'':4} {'-'*12}  {'-'*20}  {'-'*14}  {'-'*14}  ----")
for code, (name, d) in LANGS.items():
    lekt = count_files(d, "lektion*.md")
    schr = count_files(d, "schrift*.md")
    ueb  = count_files(d, "uebung*.md")
    root = root_files(d)
    lekt_ok = "✅" if lekt == 61 else "🔄" if lekt > 0 else "⏳"
    schr_ok = "✅" if schr == 11 else "🔄" if schr > 0 else "⏳"
    ueb_ok  = "✅" if ueb  == 61 else "🔄" if ueb  > 0 else "⏳"
    print(f"  {lekt_ok}  {code:2} {name:<10}  "
          f"{lekt:3}/61 {schr_ok}  "
          f"{schr:3}/11 {ueb_ok}  "
          f"{ueb:3}/61  {root}")

# ── Phasenstatus ─────────────────────────────────────────────────────────────
print("\n  ── GSD Phasenstatus ───────────────────────────────────")
phases_dir = ROOT / ".planning/phases"
if phases_dir.exists():
    for d in sorted(p for p in phases_dir.iterdir()
                    if p.is_dir() and not p.name.startswith('$') and not p.name.startswith('9')):
        plans = sorted(d.glob("*-PLAN.md"))
        total = len(plans)
        # a plan is done when a matching SUMMARY.md exists
        done = sum(1 for p in plans if (d / p.name.replace("-PLAN.md", "-SUMMARY.md")).exists())
        icon = "✅" if done == total and total > 0 else "🔄" if done > 0 else "⏳"
        print(f"  {icon} {d.name[:50]:<50} {done}/{total} Pläne")

print()
print("═" * 60)
print()
