#!/usr/bin/env python3
"""Monitor script: translation progress + GSD phase status."""
import os, re, subprocess
from pathlib import Path
from datetime import datetime
import unicodedata

def vlen(s):
    return sum(2 if unicodedata.east_asian_width(c) in 'WF' else 1 for c in str(s))

def pad_str(s, width):
    return str(s) + " " * max(0, width - vlen(s))
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
    "he": ("עברית",    DOCS / "he/lektionen"),
    "id": ("Indonesia",DOCS / "id/lektionen"),
    "zh-CN": ("简体中文", DOCS / "zh-CN/lektionen"),
    "ar": ("العربية",   DOCS / "ar/lektionen"),
    "arc": ("ܐܪܡܝܐ",    DOCS / "arc/lektionen"),
    "th": ("ไทย",      DOCS / "th/lektionen"),
    "el": ("Ελληνικά", DOCS / "el/lektionen"),
    "cop": ("ⲙⲉⲧⲣⲉⲙⲛ̀ⲭⲏⲙⲓ", DOCS / "cop/lektionen"),
}

def count_files(d, pattern):
    if not d.exists():
        return 0, 0
    files = list(d.glob(pattern))
    total = len(files)
    translated = sum(1 for f in files if "TODO: Fallback translation" not in f.read_text(encoding="utf-8", errors="ignore"))
    return total, translated

def root_files(d):
    if not d.exists():
        return 0, 0
    files = [f for f in d.glob("*.md") if not re.match(r'(lektion|schrift|uebung)\d', f.name)]
    total = len(files)
    translated = sum(1 for f in files if "TODO: Fallback translation" not in f.read_text(encoding="utf-8", errors="ignore"))
    return total, translated

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
    lekt_t, lekt_tr = count_files(d, "lektion*.md")
    schr_t, schr_tr = count_files(d, "schrift*.md")
    ueb_t, ueb_tr   = count_files(d, "uebung*.md")
    root_t, root_tr = root_files(d)
    
    lekt_ok = "✅" if lekt_tr >= 61 else "🔄" if lekt_tr > 0 else "⏳"
    schr_ok = "✅" if schr_tr >= 11 else "🔄" if schr_tr > 0 else "⏳"
    ueb_ok  = "✅" if ueb_tr  >= 61 else "🔄" if ueb_tr  > 0 else "⏳"
    
    code_pad = f"{code:<5}"
    name_pad = pad_str(name, 10)
    print(f"  {lekt_ok}  {code_pad} {name_pad}  "
          f"{lekt_tr:>2}/{lekt_t:<2} {schr_ok}  "
          f"{schr_tr:>2}/{schr_t:<2} {ueb_ok}  "
          f"{ueb_tr:>2}/{ueb_t:<2}  {root_tr}/{root_t}")

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
