#!/usr/bin/env python3
"""
Generate official Payer Sanskritkurs Translation Status Report.
Master Basis: 137 files (61 lektionen + 11 schriften + 61 uebungen + 4 root).
"""
import os
import sys
import glob
import re
import subprocess
from pathlib import Path
from datetime import datetime

ROOT = Path(__file__).parent.parent
DOCS = ROOT / "docs"
REPORT_FILE = ROOT / "TRANSLATION_REPORT.md"

LANG_MAP = [
    ('de', 'Deutsch', '🇩🇪'),
    ('en', 'English', '🇬🇧'),
    ('it', 'Italiano', '🇮🇹'),
    ('es', 'Español', '🇪🇸'),
    ('fr', 'Français', '🇫🇷'),
    ('ru', 'Русский', '🇷🇺'),
    ('uk', 'Українська', '🇺🇦'),
    ('rm', 'Rumantsch', '🇨🇭'),
    ('ar', 'العربية', '🇸🇦'),
    ('fi', 'Suomi', '🇫🇮'),
    ('ta', 'தமிழ்', '🇮🇳'),
    ('pa', 'ਪੰਜਾਬੀ', '🇮🇳'),
    ('la', 'Latina', '🇻🇦'),
    ('id', 'Bahasa Indonesia', '🇮🇩'),
    ('th', 'ไทย', '🇹🇭'),
    ('hi', 'हिंदी', '🇮🇳'),
    ('el', 'Ελληνικά', '🇬🇷'),
    ('grc', 'Ἀρχαία', '🏛️'),
    ('ro', 'Română', '🇷🇴'),
    ('he', 'עברית', '🇮🇱'),
    ('hu', 'Magyar', '🇭🇺'),
    ('zh-CN', '简体中文', '🇨🇳'),
    ('am', 'አማርኛ', '🇪🇹'),
    ('pt', 'Português', '🇵🇹'),
    ('cop', 'ⲙⲉⲧⲣⲉⲙⲛ̀ⲭⲏⲙⲓ', '🇪🇬'),
    ('af', 'Afrikaans', '🇿🇦'),
    ('nl', 'Nederlands', '🇳🇱'),
    ('fa', 'فارسی', '🇮🇷'),
    ('lt', 'Lietuvių', '🇱🇹'),
    ('sh', 'Srpsko-hrvatski', '🇷🇸'),
    ('sq', 'Shqip', '🇦🇱'),
    ('zh', '繁體中文', '🇹🇼')
]

TOTAL_MASTER = 137

def get_active_process():
    try:
        res = subprocess.run(["ps", "-eo", "pid,etime,time,args"], capture_output=True, text=True)
        for line in res.stdout.splitlines():
            if "lan_translate.py" in line and "grep" not in line:
                parts = line.strip().split(None, 3)
                if len(parts) >= 4:
                    pid, etime, cputime, cmd = parts[0], parts[1], parts[2], parts[3]
                    m = re.search(r'--lang\s+([a-zA-Z0-9_-]+)', cmd)
                    lang = m.group(1) if m else "?"
                    return {
                        "pid": pid,
                        "etime": etime,
                        "cputime": cputime,
                        "cmd": cmd,
                        "lang": lang
                    }
    except Exception:
        pass
    return None

def get_chunk_info(lang):
    if not lang or lang == "?":
        return None

    active_file = None
    curr_chunk = 1
    total_chunks = 1

    # Check translation.log for real-time progress of active_file and chunk
    log_path = ROOT / "translation.log"
    if log_path.exists():
        try:
            lines = log_path.read_text(encoding="utf-8", errors="ignore").splitlines()
            lang_prefix = f"[{lang}]"
            
            # Find the active_file for this specific language
            for line in reversed(lines[-300:]):
                if line.startswith(lang_prefix):
                    m_file = re.search(r'(?:Translating|Outdated|Fallback tags detected in)\s+([a-zA-Z0-9_-]+\.md)', line)
                    if m_file:
                        active_file = m_file.group(1)
                        break
            
            # Find chunk section progress
            for line in reversed(lines[-100:]):
                m_sec = re.search(r'->\s*(?:section|surgical fallback|Chunk|chunk)\s*(\d+)(?:/(\d+))?', line, re.IGNORECASE)
                if m_sec:
                    curr_chunk = int(m_sec.group(1))
                    if m_sec.group(2):
                        total_chunks = int(m_sec.group(2))
                    break
        except Exception:
            pass

    # Fallback to filesystem mtime if active_file not parsed from log
    if not active_file:
        lang_dir = DOCS / lang if lang != "de" else DOCS
        if lang_dir.exists():
            files = list(lang_dir.glob("**/*.md"))
            files = [f for f in files if "qa_viewer" not in f.name and "deleteme" not in f.name]
            if files:
                files.sort(key=os.path.getmtime, reverse=True)
                active_file = files[0].name

    if active_file and total_chunks == 1:
        try:
            matches = list(DOCS.glob(f"**/{active_file}"))
            if matches:
                from lan_translate import chunk_content
                content = matches[0].read_text(encoding="utf-8", errors="ignore")
                chunks = chunk_content(content)
                total_chunks = len(chunks) if chunks else 1
        except Exception:
            total_chunks = 1

    return {
        "file_name": active_file or "lektionen / wortliste",
        "curr_chunk": curr_chunk,
        "total_chunks": max(total_chunks, curr_chunk)
    }

def generate_report():
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S CEST")
    active_proc = get_active_process()
    
    rows = []
    for code, name, emoji in LANG_MAP:
        p = DOCS / code if code != "de" else DOCS
        if not p.exists():
            rows.append({
                "code": code, "name": name, "emoji": emoji,
                "vorhanden": 0, "sauber": 0, "fallbacks": 0, "pct": 0.0
            })
            continue
        
        all_md = list(p.glob("**/*.md"))
        EXCLUDE_META = {"licenses.md", "AUTHORS_GUIDE.md", "settings.md", "impressum.md", "grammatik.md", "themen.md", "qa_help.md"}
        files = [f for f in all_md if f.name not in EXCLUDE_META and "qa_viewer" not in f.name and "deleteme" not in f.name]
        vorhanden = min(TOTAL_MASTER, len(files))
        
        fallbacks = 0
        sauber = 0
        for f in files:
            txt = f.read_text(encoding="utf-8", errors="ignore")
            if "TODO: Fallback translation" in txt:
                fallbacks += 1
            else:
                sauber += 1
        sauber = min(TOTAL_MASTER, sauber)
        
        if code == "de":
            pct = 100.0
            sauber = TOTAL_MASTER
            vorhanden = TOTAL_MASTER
            fallbacks = 0
        else:
            if fallbacks > 0:
                pct = round((sauber / TOTAL_MASTER) * 100.0, 1)
                if pct >= 100.0:
                    pct = 99.3 # Cap below 100% if fallbacks remain
            else:
                pct = min(100.0, round((sauber / TOTAL_MASTER) * 100.0, 1))
            
        rows.append({
            "code": code, "name": name, "emoji": emoji,
            "vorhanden": vorhanden, "sauber": sauber, "fallbacks": fallbacks, "pct": pct
        })

    # Filter rows:
    # 1. 'de' (Master)
    # 2. Unfinished languages sorted by pct descending
    de_row = [r for r in rows if r["code"] == "de"]
    finished_rows = [r for r in rows if r["code"] != "de" and r["pct"] >= 100.0 and r["fallbacks"] == 0]
    unfinished_rows = [r for r in rows if r["code"] != "de" and (r["pct"] < 100.0 or r["fallbacks"] > 0)]
    unfinished_rows.sort(key=lambda r: (r["pct"], -r["fallbacks"]), reverse=True)
    
    show_all = "--all" in sys.argv
    display_rows = de_row + finished_rows + unfinished_rows if show_all else unfinished_rows
    
    # Active process details
    active_lang_code = active_proc["lang"] if active_proc else (unfinished_rows[0]["code"] if unfinished_rows else None)
    active_row = next((r for r in rows if r["code"] == active_lang_code), None)
    chunk_info = get_chunk_info(active_lang_code)
    
    lines = []
    lines.append("📊 Translation Status Report (Master-Basis: 137 Dateien)")
    lines.append(f"Timestamp: {timestamp}\n")
    
    if finished_rows:
        fin_codes = ", ".join([f"`{r['code']}`" for r in finished_rows])
        lines.append(f"✅ **{len(finished_rows)} Sprachen vollständig fertig (100%, 0 Fallbacks):** {fin_codes}\n")
    
    lines.append("🎯 Aktuell in Übersetzung (Höchste Prozentzahl unter 100%):\n")
    
    if active_row:
        lines.append(f"Sprache: {active_row['emoji']} {active_row['name']} ({active_row['code']})")
        if active_proc:
            lines.append(f"Prozess-PID: {active_proc['pid']} (`{active_proc['cmd']}` – Ungepuffert & Aktiv, CPU-Time: {active_proc['cputime']})")
        else:
            lines.append("Prozess-PID: Nicht aktiv (Wartet auf Start)")
        
        file_str = chunk_info["file_name"] if chunk_info else "lektionen / wortliste"
        curr_c = chunk_info["curr_chunk"] if chunk_info else 1
        total_c = chunk_info["total_chunks"] if chunk_info else 1
        file_pct = round((curr_c / total_c) * 100.0, 1)
        lines.append(f"Aktuelle Datei / Chunk-Fortschritt: `{file_str}` (Sektion {curr_c}/{total_c} Chunks – {file_pct}% dieser Datei) | Gesamt: **{active_row['sauber']}/137 Dateien ({active_row['pct']}%)**")
        lines.append("Server: 100% KOSTENLOS über den lokalen Server (`nyx.local:8000`).\n")
    
    lines.append("| Locale | Sprache | Vorhanden | Sauber | Fallbacks | Gesamt-Fortschritt | Delta | Status |")
    lines.append("| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :--- |")
    
    for idx, r in enumerate(display_rows):
        if r["code"] == "de":
            status = "Master-Quelle"
        elif r["pct"] >= 100.0 and r["fallbacks"] == 0:
            status = "✅ 100% Fertig"
        elif r["fallbacks"] > 0:
            status = f"🔄 {r['fallbacks']} Fallbacks zu bereinigen"
        elif active_proc and r["code"] == active_proc["lang"]:
            file_str = chunk_info['file_name'] if chunk_info else 'in Bearbeitung'
            curr_c = chunk_info["curr_chunk"] if chunk_info else 1
            total_c = chunk_info["total_chunks"] if chunk_info else 1
            status = f"🎯 Aktiv in Übersetzung ({file_str} – Chunk {curr_c}/{total_c})"
        elif not active_proc and ((show_all and idx == len(de_row) + len(finished_rows)) or (not show_all and idx == 0)):
            status = f"⚠️ Lokale Ressourcen erschöpft ({TOTAL_MASTER - r['sauber']} Dateien offen – Wartet auf OpenRouter-Freigabe)"
        elif (show_all and idx == len(de_row) + len(finished_rows)) or (not show_all and idx == 0):
            status = "🔄 Nächste Sprache"
        else:
            status = "🔄 In Warteschlange" if r["sauber"] > 0 else "⌛ In Warteschlange"
            
        code_str = f"`{r['code']}`"
        lines.append(f"| {code_str} | {r['name']} | {r['vorhanden']}/{TOTAL_MASTER} | {r['sauber']} | {r['fallbacks']} | {r['pct']:.1f}% | 0 | {status} |")

    report_text = "\n".join(lines)
    REPORT_FILE.write_text(report_text, encoding="utf-8")
    return report_text

if __name__ == "__main__":
    sys.path.insert(0, str(ROOT / "scripts"))
    print(generate_report())
