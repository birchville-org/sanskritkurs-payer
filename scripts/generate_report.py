#!/usr/bin/env python3
import os
import json
import re
from pathlib import Path
from datetime import datetime

ROOT = Path(__file__).parent.parent
DOCS = ROOT / "docs"
SCRATCH = ROOT / "scratch"
STATUS_FILE = SCRATCH / "last_status.json"
SESSION_FILE = SCRATCH / "session_status.json"
REPORT_FILE = ROOT / "TRANSLATION_REPORT.md"

LANGS = {
    "de": "Deutsch",
    "en": "English",
    "it": "Italiano",
    "es": "Español",
    "fr": "Français",
    "hi": "हिंदी",
    "ru": "Русский",
    "uk": "Українська",
    "ta": "தமிழ்",
    "pa": "ਪੰਜਾਬੀ",
    "la": "Latina",
    "rm": "Rumantsch",
    "ro": "Română",
    "he": "עברית",
    "id": "Indonesia",
    "zh-CN": "简体中文",
    "zh": "繁體中文",
    "ar": "العربية",
    "th": "ไทย",
    "fi": "Suomi",
    "hu": "Magyar",
    "el": "Ελληνικά",
    "cop": "ⲙⲉⲧⲣⲉⲙⲛ̀ⲭⲏⲙⲓ",
    "fa": "فارسی",
    "nl": "Nederlands",
    "grc": "Ἀρχαία",
    "am": "አማርኛ",
    "af": "Afrikaans",
    "lt": "Lietuvių",
    "sh": "Srpskohrvatski",
    "sq": "Shqip",
}

META_FILES = [
    "index.md",
    "lektionen/glossar.md",
    "grammatik.md",
    "themen.md",
    "impressum.md",
    "licenses.md",
    "lektionen/inhaltsverzeichnis.md",
    "lektionen/wortliste.md"
]

def count_translated(d, pattern):
    if not d.exists():
        return 0, 0
    files = list(d.glob(pattern))
    total = len(files)
    translated = sum(1 for f in files if "TODO: Fallback translation" not in f.read_text(encoding="utf-8", errors="ignore"))
    return total, translated

def count_meta_translated(code):
    base_dir = DOCS if code == "de" else DOCS / code
    total = len(META_FILES)
    translated = 0
    for rel_path in META_FILES:
        p = base_dir / rel_path
        if p.exists():
            content = p.read_text(encoding="utf-8", errors="ignore")
            if "TODO: Fallback translation" not in content:
                translated += 1
    return total, translated

def get_current_activity():
    import subprocess
    running_langs = []
    try:
        res = subprocess.run(["ps", "-ef"], capture_output=True, text=True, check=True)
        for line in res.stdout.splitlines():
            if "lan_translate.py" in line and "grep" not in line:
                parts = line.split()
                for idx, part in enumerate(parts):
                    if part in ("--lang", "-l") and idx + 1 < len(parts):
                        langs_val = parts[idx + 1]
                        for c in langs_val.split(","):
                            c = c.strip()
                            if c and c not in running_langs:
                                running_langs.append(c)
    except Exception:
        pass
        
    activities = []
    for lang in running_langs:
        lang_dir = DOCS / "lektionen" if lang == "de" else DOCS / lang / "lektionen"
        if lang_dir.exists():
            files = list(lang_dir.glob("*.md"))
            if files:
                latest_file = max(files, key=lambda f: f.stat().st_mtime)
                activities.append({
                    "lang": lang,
                    "file": latest_file.name,
                    "mtime": latest_file.stat().st_mtime
                })
    return activities

def main():
    os.makedirs(SCRATCH, exist_ok=True)
    import time
    
    # Load session status if it exists and is younger than 12 hours (43200s)
    last_status = {}
    is_valid_session = False
    if SESSION_FILE.exists():
        mtime = SESSION_FILE.stat().st_mtime
        if time.time() - mtime < 43200:
            try:
                with open(SESSION_FILE, "r", encoding="utf-8") as f:
                    last_status = json.load(f)
                is_valid_session = True
            except Exception:
                pass
                
    # Fallback to last_status if session is invalid but we want some baseline
    if not is_valid_session and STATUS_FILE.exists():
        try:
            with open(STATUS_FILE, "r", encoding="utf-8") as f:
                last_status = json.load(f)
        except Exception:
            pass

    current_status = {}
    table_rows = []
    
    for code, name in LANGS.items():
        if code == "de":
            d = DOCS / "lektionen"
        else:
            d = DOCS / code / "lektionen"
            
        t_lekt, tr_lekt = count_translated(d, "lektion*.md")
        t_schr, tr_schr = count_translated(d, "schrift*.md")
        t_ueb, tr_ueb = count_translated(d, "uebung*.md")
        t_meta, tr_meta = count_meta_translated(code)
        
        current_status[code] = {
            "lekt": tr_lekt,
            "schr": tr_schr,
            "ueb": tr_ueb,
            "meta": tr_meta
        }
        
        # Calculate deltas
        d_lekt = 0
        d_schr = 0
        d_ueb = 0
        d_meta = 0
        
        if code in last_status:
            d_lekt = tr_lekt - last_status[code].get("lekt", tr_lekt)
            d_schr = tr_schr - last_status[code].get("schr", tr_schr)
            d_ueb = tr_ueb - last_status[code].get("ueb", tr_ueb)
            d_meta = tr_meta - last_status[code].get("meta", tr_meta)
            
        def fmt_delta(val):
            return f"+{val}" if val > 0 else f"{val}" if val < 0 else "0"
            
        # Determine status icons
        icon_lekt = "✅" if tr_lekt >= 61 else "🔄" if tr_lekt > 0 else "⏳"
        icon_schr = "✅" if tr_schr >= 11 else "🔄" if tr_schr > 0 else "⏳"
        icon_ueb  = "✅" if tr_ueb  >= 61 else "🔄" if tr_ueb  > 0 else "⏳"
        icon_meta = "✅" if tr_meta >= t_meta and t_meta > 0 else "🔄" if tr_meta > 0 else "⏳"
        
        # General state icon
        if icon_lekt == "✅" and icon_schr == "✅" and icon_ueb == "✅" and icon_meta == "✅":
            state_icon = "✅"
        elif icon_lekt == "⏳" and icon_schr == "⏳" and icon_ueb == "⏳" and icon_meta == "⏳":
            state_icon = "⏳"
        else:
            state_icon = "🔄"
            
        table_rows.append({
            "state_icon": state_icon,
            "code": code,
            "name": name,
            "lekt": f"{icon_lekt} {tr_lekt}/{61}",
            "d_lekt": fmt_delta(d_lekt),
            "schr": f"{icon_schr} {tr_schr}/{11}",
            "d_schr": fmt_delta(d_schr),
            "ueb": f"{icon_ueb} {tr_ueb}/{61}",
            "d_ueb": fmt_delta(d_ueb),
            "meta": f"{icon_meta} {tr_meta}/{t_meta}" if t_meta > 0 else "⏳ 0/0",
            "d_meta": fmt_delta(d_meta),
            "total_change": d_lekt + d_schr + d_ueb + d_meta
        })

    # Format Markdown Table
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    report_lines = []
    report_lines.append(f"### 📊 Übersetzungs-Statusreport — {now_str}")
    report_lines.append("")
    report_lines.append("|   | Code | Sprache | Lektionen | Delta | Schriften | Delta | Übungen | Delta | Metadaten | Delta |")
    report_lines.append("|---|------|---------|-----------|-------|-----------|-------|---------|-------|-----------|-------|")
    
    for row in table_rows:
        bold = "**" if row["total_change"] > 0 else ""
        end_bold = "**" if row["total_change"] > 0 else ""
        
        # Highlight changes with bold row content
        report_lines.append(f"| {row['state_icon']} | {row['code']} | {bold}{row['name']}{end_bold} | {row['lekt']} | {bold}{row['d_lekt']}{end_bold} | {row['schr']} | {bold}{row['d_schr']}{end_bold} | {row['ueb']} | {bold}{row['d_ueb']}{end_bold} | {row['meta']} | {bold}{row['d_meta']}{end_bold} |")
        
    # Activities section
    report_lines.append("")
    report_lines.append("### 🔄 Laufende Übersetzungen (Aktivitäten)")
    report_lines.append("")
    
    activities = get_current_activity()
    if not activities:
        report_lines.append("*Keine aktiven Übersetzungs-Jobs gefunden.*")
    else:
        report_lines.append("| Code | Sprache | Aktuelle Datei | Letzte Änderung |")
        report_lines.append("|------|---------|----------------|-----------------|")
        for act in activities:
            lang_name = LANGS.get(act["lang"], act["lang"])
            time_str = datetime.fromtimestamp(act["mtime"]).strftime("%H:%M:%S")
            report_lines.append(f"| `{act['lang']}` | {lang_name} | `{act['file']}` | {time_str} |")

    # Queue planning section
    report_lines.append("")
    report_lines.append("### 📅 Geplante Reihenfolge der Übersetzungen")
    report_lines.append("")
    
    planned_langs = [
        ("th", "Thailändisch"),
        ("el", "Neugriechisch"),
        ("fi", "Finnisch"),
        ("hu", "Ungarisch"),
        ("cop", "Koptisch"),
        ("grc", "Altgriechisch"),
        ("fa", "Persisch"),
        ("nl", "Niederländisch"),
        ("af", "Afrikaans"),
        ("lt", "Lietuvių"),
        ("sh", "Srpskohrvatski"),
        ("sq", "Shqip"),
        ("am", "Amharic")
    ]
    
    active_codes = [act["lang"] for act in activities]
    
    idx = 1
    for code, name in planned_langs:
        is_done = False
        if code in current_status:
            stat = current_status[code]
            if stat["lekt"] == 61 and stat["schr"] == 11 and stat["ueb"] == 61:
                is_done = True
                
        if is_done:
            continue
            
        if code in active_codes:
            status_str = "🔄 Läuft"
        else:
            status_str = "⏳ Ausstehend"
            
        report_lines.append(f"{idx}. **{code}** ({name}) — {status_str}")
        idx += 1

    report_content = "\n".join(report_lines)
    
    # Print to console
    print(report_content)
    
    # Write to report file in root directory
    with open(REPORT_FILE, "w", encoding="utf-8") as f:
        f.write(report_content + "\n")
        
    # If this was a new session, save the status as the session baseline
    if not is_valid_session:
        with open(SESSION_FILE, "w", encoding="utf-8") as f:
            json.dump(current_status, f, ensure_ascii=False, indent=2)
            
    # Always save current status in last_status.json
    with open(STATUS_FILE, "w", encoding="utf-8") as f:
        json.dump(current_status, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    main()
