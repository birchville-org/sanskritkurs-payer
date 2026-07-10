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

LANGS = {
    "de": "Deutsch",
    "en": "English",
    "it": "Italiano",
    "es": "Español",
    "fr": "Français",
    "hi": "हिंदी",
    "bg": "Български",
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
    "arc": "ܐܪܡܝܐ",
}

META_FILES = [
    "index.md",
    "glossar.md",
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
    total = 0
    translated = 0
    for rel_path in META_FILES:
        p = base_dir / rel_path
        if p.exists():
            total += 1
            content = p.read_text(encoding="utf-8", errors="ignore")
            if "TODO: Fallback translation" not in content:
                translated += 1
    return total, translated

def main():
    os.makedirs(SCRATCH, exist_ok=True)
    
    # Load last status if exists
    last_status = {}
    if STATUS_FILE.exists():
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
    print(f"### 📊 Übersetzungs-Statusreport — {now_str}")
    print()
    print("|   | Code | Sprache | Lektionen | Delta | Schriften | Delta | Übungen | Delta | Metadaten | Delta |")
    print("|---|------|---------|-----------|-------|-----------|-------|---------|-------|-----------|-------|")
    
    for row in table_rows:
        bold = "**" if row["total_change"] > 0 else ""
        end_bold = "**" if row["total_change"] > 0 else ""
        
        # Highlight changes with bold row content
        print(f"| {row['state_icon']} | {row['code']} | {bold}{row['name']}{end_bold} | {row['lekt']} | {bold}{row['d_lekt']}{end_bold} | {row['schr']} | {bold}{row['d_schr']}{end_bold} | {row['ueb']} | {bold}{row['d_ueb']}{end_bold} | {row['meta']} | {bold}{row['d_meta']}{end_bold} |")
        
    # Save current status as last status
    with open(STATUS_FILE, "w", encoding="utf-8") as f:
        json.dump(current_status, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    main()
