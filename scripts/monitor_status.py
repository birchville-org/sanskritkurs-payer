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

ACTIVE_LANGS = [
    'de', 'en', 'it', 'es', 'fr', 'hi', 'ru', 'uk', 'ta', 'pa', 
    'la', 'rm', 'ro', 'he', 'id', 'zh-CN', 'ar', 'th', 'el', 'cop',
    'grc', 'fa', 'nl', 'af', 'lt', 'sh', 'sq', 'am', 'gez', 'fi', 'hu',
    'zh', 'pt'
]

LANGS = {
    "de": ("Deutsch",  DOCS / "lektionen"),
    "en": ("English",  DOCS / "en/lektionen"),
    "it": ("Italiano", DOCS / "it/lektionen"),
    "es": ("Español",  DOCS / "es/lektionen"),
    "fr": ("Français", DOCS / "fr/lektionen"),
    "hi": ("हिंदी",    DOCS / "hi/lektionen"),
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
    "th": ("ไทย",      DOCS / "th/lektionen"),
    "am": ("አማርኛ", DOCS / "am/lektionen"),
    "gez": ("ግዕዝ", DOCS / "gez/lektionen"),
    "el": ("Ελληνικά", DOCS / "el/lektionen"),
    "cop": ("ⲙⲉⲧⲣⲉⲙⲛ̀ⲭⲏⲙⲓ", DOCS / "cop/lektionen"),
    "grc": ("Ἀρχαία", DOCS / "grc/lektionen"),
    "fa": ("فارسی", DOCS / "fa/lektionen"),
    "nl": ("Nederlands", DOCS / "nl/lektionen"),
    "af": ("Afrikaans", DOCS / "af/lektionen"),
    "lt": ("Lietuvių", DOCS / "lt/lektionen"),
    "sh": ("Srpskohrvatski", DOCS / "sh/lektionen"),
    "sq": ("Shqip", DOCS / "sq/lektionen"),
    "fi": ("Suomi", DOCS / "fi/lektionen"),
    "hu": ("Magyar", DOCS / "hu/lektionen"),
    "zh": ("繁體中文", DOCS / "zh/lektionen"),
    "pt": ("Português", DOCS / "pt/lektionen"),
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
        return 8, 0
    root_pages = ["index.md", "grammatik.md", "themen.md", "impressum.md"]
    lek_pages = ["index.md", "inhaltsverzeichnis.md", "wortliste.md", "glossar.md"]
    total = len(root_pages) + len(lek_pages)
    translated = 0
    
    # Check parent directory (docs root)
    parent_dir = d.parent
    for filename in root_pages:
        file_path = parent_dir / filename
        if file_path.exists():
            content = file_path.read_text(encoding="utf-8", errors="ignore")
            if "TODO: Fallback translation" not in content:
                translated += 1
                
    # Check lektionen directory
    for filename in lek_pages:
        file_path = d / filename
        if file_path.exists():
            content = file_path.read_text(encoding="utf-8", errors="ignore")
            if "TODO: Fallback translation" not in content:
                translated += 1
                
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
print(f"  {'':4} {'Sprache':<17}  {'Lektionen':<10}  {'Schriften':<10}  {'Übungen':<10}  {'Root':<8}  {'% Fortschritt':<12}")
print(f"  {'':4} {'-'*17}  {'-'*10}  {'-'*10}  {'-'*10}  {'-'*8}  {'-'*12}")

lang_rows = []
for code, (name, d) in LANGS.items():
    lekt_t, lekt_tr = count_files(d, "lektion*.md")
    schr_t, schr_tr = count_files(d, "schrift*.md")
    ueb_t, ueb_tr   = count_files(d, "uebung*.md")
    root_t, root_tr = root_files(d)
    
    lekt_max = 61
    schr_max = 11
    ueb_max = 61
    root_max = 8
    total_max = lekt_max + schr_max + ueb_max + root_max
    total_tr = lekt_tr + schr_tr + ueb_tr + root_tr
    pct = (total_tr / total_max) * 100.0 if total_max else 0.0
    
    lekt_ok = "✅" if lekt_tr >= lekt_max else "🔄" if lekt_tr > 0 else "⏳"
    schr_ok = "✅" if schr_tr >= schr_max else "🔄" if schr_tr > 0 else "⏳"
    ueb_ok  = "✅" if ueb_tr  >= ueb_max else "🔄" if ueb_tr  > 0 else "⏳"
    root_ok = "✅" if root_tr >= root_max else "🔄" if root_tr > 0 else "⏳"
    
    is_complete = (total_tr >= total_max) or (lekt_tr >= lekt_max and schr_tr >= schr_max and ueb_tr >= ueb_max and root_tr >= root_max)
    is_started = (lekt_tr > 0 or schr_tr > 0 or ueb_tr > 0 or root_tr > 0)
    lang_ok = "✅" if is_complete else "🔄" if is_started else "⏳"
    
    lang_rows.append({
        "code": code,
        "name": name,
        "lang_ok": lang_ok,
        "lekt_ok": lekt_ok, "lekt_tr": lekt_tr, "lekt_max": lekt_max,
        "schr_ok": schr_ok, "schr_tr": schr_tr, "schr_max": schr_max,
        "ueb_ok": ueb_ok, "ueb_tr": ueb_tr, "ueb_max": ueb_max,
        "root_ok": root_ok, "root_tr": root_tr, "root_max": root_max,
        "total_tr": total_tr, "total_max": total_max,
        "pct": pct,
        "is_complete": is_complete
    })

# Sort: Complete languages first, then unfinished languages ordered by highest percentage descending
completed_rows = [r for r in lang_rows if r["is_complete"]]
unfinished_rows = [r for r in lang_rows if not r["is_complete"]]
unfinished_rows.sort(key=lambda r: (r["pct"], r["lekt_tr"]), reverse=True)

sorted_rows = completed_rows + unfinished_rows

for r in sorted_rows:
    code_pad = f"{r['code']:<5}"
    name_pad = pad_str(r['name'], 11)
    pct_str = f"{r['pct']:>5.1f}%"
    print(f"  {r['lang_ok']}  {code_pad} {name_pad}  "
          f"{r['lekt_ok']} {r['lekt_tr']:>2}/{r['lekt_max']:<2}  "
          f"{r['schr_ok']} {r['schr_tr']:>2}/{r['schr_max']:<2}  "
          f"{r['ueb_ok']} {r['ueb_tr']:>2}/{r['ueb_max']:<2}  "
          f"{r['root_ok']} {r['root_tr']:>2}/{r['root_max']:<2}  "
          f"[{pct_str}]")

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
