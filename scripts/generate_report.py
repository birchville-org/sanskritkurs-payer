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
import difflib
from pathlib import Path
from datetime import datetime
import time
import json

sys.path.insert(0, str(Path(__file__).parent))
from translation.config import DE_FALLBACK_ALLOWED, STALE_LOCK_SEC
from translation_qa import check_has_de_phrases

ROOT = Path(__file__).parent.parent
DOCS = ROOT / "docs"
REPORT_FILE = ROOT / "TRANSLATION_REPORT.md"
CACHE_FILE = ROOT / ".last_report_cache.json"

def get_top_unfinished_language():
    """Returns the language code of the unfinished language with the highest completion percentage."""
    all_rows = []
    for code, name, emoji in LANG_MAP:
        if code == "de":
            continue
        queue = get_translation_queue(code)
        sauber = TOTAL_MASTER - len(queue)
        pct = round((sauber / TOTAL_MASTER) * 100.0, 1)
        if len(queue) > 0:
            all_rows.append({"code": code, "sauber": sauber, "pct": pct, "queue_len": len(queue)})
    if not all_rows:
        return "ALL_FINISHED"
    all_rows.sort(key=lambda r: (r["pct"], -r["queue_len"]), reverse=True)
    return all_rows[0]["code"]

def load_report_cache():
    if CACHE_FILE.exists():
        try:
            return json.loads(CACHE_FILE.read_text(encoding="utf-8"))
        except Exception:
            pass
    return {}

def save_report_cache(cache_data):
    try:
        CACHE_FILE.write_text(json.dumps(cache_data, indent=2, ensure_ascii=False), encoding="utf-8")
    except Exception:
        pass

if str(ROOT / "scripts") not in sys.path:
    sys.path.insert(0, str(ROOT / "scripts"))

from translation_qa import (
    DE_FALLBACK_ALLOWED, EXCLUDE_META, check_has_de_phrases, 
    is_file_fallback, get_language_status
)

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
    ('bg', 'Български', '🇧🇬'),
    ('zh', '繁體中文', '🇹🇼'),
    ('tr', 'Türkçe', '🇹🇷'),
    ('vi', 'Tiếng Việt', '🇻🇳'),
    ('zu', 'isiZulu', '🇿🇦')
]

TOTAL_MASTER = 136

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

                    # Check lock file mtime
                    lock_stale = False
                    lock_file = Path("/tmp/payer_translation_nyx.lock")

                    if lock_file.exists():
                        if (time.time() - lock_file.stat().st_mtime) > STALE_LOCK_SEC:
                            lock_stale = True

                    is_stuck = lock_stale

                    # Report stuck process if lock heartbeat is stale (> STALE_LOCK_SEC)
                    if is_stuck and pid.isdigit():
                        sys.stdout.write(f"\n[!] AUTOMATED MONITORING NOTICE: Process PID {pid} appears stuck (lock heartbeat stale > {STALE_LOCK_SEC}s).\n")
                        sys.stdout.flush()

                    return {
                        "pid": pid,
                        "etime": etime,
                        "cputime": cputime,
                        "cmd": cmd,
                        "lang": lang,
                        "is_stuck": is_stuck
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

    # Gather log files (background task logs take priority over static translation.log)
    log_files = []
    task_logs = list(Path("/Users/marco/.gemini/antigravity-ide/brain").rglob("tasks/*.log"))
    if task_logs:
        task_logs.sort(key=lambda f: f.stat().st_mtime, reverse=True)
        log_files.extend(task_logs)
    if (ROOT / "translation.log").exists():
        log_files.append(ROOT / "translation.log")

    lang_prefix = f"[{lang}]"
    for log_path in log_files:
        try:
            lines = log_path.read_text(encoding="utf-8", errors="ignore").splitlines()
            for line in reversed(lines[-500:]):
                m_file = re.search(r'\[?' + re.escape(lang) + r'\]?\s+(?:Translating|Outdated|Fallback tags detected in|Queue Item:)\s+([a-zA-Z0-9_-]+\.md)', line, re.IGNORECASE)
                if m_file:
                    active_file = m_file.group(1)
                    break
            if active_file:
                for line in reversed(lines[-200:]):
                    m_sec = re.search(r'->\s*(?:section|surgical fallback|Chunk|chunk|Sektion)\s*(\d+)(?:/(\d+))?', line, re.IGNORECASE)
                    if m_sec:
                        curr_chunk = int(m_sec.group(1))
                        if m_sec.group(2):
                            total_chunks = int(m_sec.group(2))
                        break
                break
        except Exception:
            pass
        if active_file and total_chunks == 1:
            try:
                target_p = DOCS / lang / "lektionen" / active_file
                if not target_p.exists():
                    target_p = DOCS / lang / active_file
                if target_p.exists():
                    from translation.file_processor import chunk_content
                    content = target_p.read_text(encoding="utf-8", errors="ignore")
                    chunks = chunk_content(content)
                    total_chunks = len(chunks) if chunks else 1
            except Exception:
                total_chunks = 1

    return {
        "file_name": active_file or "lektionen / wortliste",
        "curr_chunk": curr_chunk,
        "total_chunks": max(total_chunks, curr_chunk)
    }

def get_translation_queue(code):
    if code == "de":
        return []
    lang_dir = DOCS / code
    queue_files = []
    
    # 1. Main pages
    main_pages = ['index.md', 'grammatik.md', 'themen.md', 'impressum.md', 'settings.md']
    for p in main_pages:
        queue_files.append((DOCS / p, lang_dir / p))
    # 2. Lessons 01-61
    for i in range(1, 62):
        queue_files.append((DOCS / f'lektionen/lektion{i:02d}.md', lang_dir / f'lektionen/lektion{i:02d}.md'))
    # 3. Scripts 01-11
    for i in range(1, 12):
        queue_files.append((DOCS / f'lektionen/schrift{i:02d}.md', lang_dir / f'lektionen/schrift{i:02d}.md'))
    # 4. Exercises 01-61
    for i in range(1, 62):
        queue_files.append((DOCS / f'lektionen/uebung{i:02d}.md', lang_dir / f'lektionen/uebung{i:02d}.md'))
    # 5. Wortlisten
    for p in ['lektionen/wortliste.md', 'lektionen/inhaltsverzeichnis.md']:
        queue_files.append((DOCS / p, lang_dir / p))

    todo_queue = []
    for src, tgt in queue_files:
        if not src.exists():
            continue
        if not tgt.exists():
            todo_queue.append((tgt.name, "Fehlt (neu)"))
            continue
        if tgt.stat().st_mtime < src.stat().st_mtime:
            todo_queue.append((tgt.name, "Veraltet"))
            continue
        txt = tgt.read_text(encoding='utf-8', errors='ignore')
        de_txt = src.read_text(encoding='utf-8', errors='ignore')
        txt_body = re.sub(r'^---.*?---\s*', '', txt, flags=re.DOTALL)
        de_body = re.sub(r'^---.*?---\s*', '', de_txt, flags=re.DOTALL)
        is_de_exact = (txt == de_txt) or (len(txt_body) > 0 and abs(len(txt) - len(de_txt)) / max(len(txt), len(de_txt)) < 0.05 and txt_body[:200] == de_body[:200])
        has_de = check_has_de_phrases(txt, code, fast=True)
        if "TODO: Fallback translation" in txt or is_de_exact or has_de:
            reason = "DE-Kopie" if is_de_exact else "DE-Reste"
            todo_queue.append((tgt.name, reason))

    return todo_queue

def get_performance_info():
    log_files = [ROOT / "translation_runner.log", ROOT / "translation.log"]
    speeds = []
    for log_path in log_files:
        if log_path.exists():
            try:
                lines = log_path.read_text(encoding="utf-8", errors="ignore").splitlines()
                speed_lines = [l for l in lines if '[Speed:' in l]
                for line in reversed(speed_lines[-20:]):
                    m = re.search(r'\[Speed:\s*([\d\.]+)\s*t/s\s*\|\s*(\d+)\s*tokens in\s*([\d\.]+)s\]', line)
                    if m:
                        tps = float(m.group(1))
                        tokens = int(m.group(2))
                        sec = float(m.group(3))
                        speeds.append((tps, tokens, sec))
                        if len(speeds) >= 10:
                            break
            except Exception:
                pass
        if speeds:
            break
    if speeds:
        latest = speeds[0]
        avg_tps = round(sum(s[0] for s in speeds) / len(speeds), 1)
        return {
            "latest_tps": latest[0],
            "latest_tokens": latest[1],
            "latest_sec": latest[2],
            "avg_tps": avg_tps
        }
    return None

def generate_report():
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S CEST")
    active_proc = get_active_process()
    prev_cache = load_report_cache()
    prev_time = prev_cache.get("timestamp", "Unbekannt")
    prev_data = prev_cache.get("data", {})
    
    rows = []
    for code, name, emoji in LANG_MAP:
        lang_dir = DOCS / code if code != "de" else DOCS
        if not lang_dir.exists():
            rows.append({
                "code": code, "name": name, "emoji": emoji,
                "vorhanden": 0, "sauber": 0, "fallbacks": 0, "pct": 0.0,
                "todo_queue": []
            })
            continue
        
        all_md = list(lang_dir.glob("**/*.md"))
        EXCLUDE_META = {"licenses.md", "AUTHORS_GUIDE.md", "settings.md", "impressum.md", "grammatik.md", "themen.md", "qa_help.md"}
        files = [f for f in all_md if f.name not in EXCLUDE_META and "qa_viewer" not in f.name and "deleteme" not in f.name and not f.name.startswith("test") and not f.name.endswith("-test.md")]
        vorhanden = min(TOTAL_MASTER, len(files))
        
        if code == "de":
            pct = 100.0
            sauber = TOTAL_MASTER
            vorhanden = TOTAL_MASTER
            fallbacks = 0
            todo_queue = []
        else:
            todo_queue = get_translation_queue(code)
            queue_len = len(todo_queue)
            sauber = max(0, TOTAL_MASTER - queue_len)
            fallbacks = len([item for item in todo_queue if "DE-" in item[1] or "Fallback" in item[1]])
            pct = round((sauber / TOTAL_MASTER) * 100.0, 1) if queue_len > 0 else 100.0

        # Calculate Delta against previous report cache
        p_info = prev_data.get(code, {})
        p_sauber = p_info.get("sauber")
        p_pct = p_info.get("pct")
        p_fb = p_info.get("fallbacks")

        if p_sauber is not None:
            d_sauber = sauber - p_sauber
            d_pct = round(pct - p_pct, 1)
            d_fb = fallbacks - p_fb
            
            delta_parts = []
            if d_sauber != 0:
                delta_parts.append(f"{'+' if d_sauber > 0 else ''}{d_sauber} Sauber")
            if d_fb != 0:
                delta_parts.append(f"{'+' if d_fb > 0 else ''}{d_fb} FB")
            if d_pct != 0.0:
                delta_parts.append(f"Δ {'+' if d_pct > 0 else ''}{d_pct:.1f}%")
            
            delta_str = " | ".join(delta_parts) if delta_parts else "—"
        else:
            delta_str = "—"

        rows.append({
            "code": code, "name": name, "emoji": emoji,
            "vorhanden": vorhanden, "sauber": sauber, "fallbacks": fallbacks, "pct": pct,
            "todo_queue": todo_queue,
            "delta_str": delta_str
        })

    # Save current cache
    new_cache = {
        "timestamp": timestamp,
        "data": {r["code"]: {"sauber": r["sauber"], "fallbacks": r["fallbacks"], "pct": r["pct"]} for r in rows}
    }
    save_report_cache(new_cache)

    # Filter rows:
    # 1. 'de' (Master)
    # 2. Unfinished languages sorted by pct descending
    de_row = [r for r in rows if r["code"] == "de"]
    finished_rows = [r for r in rows if r["code"] != "de" and r["sauber"] == TOTAL_MASTER and r["fallbacks"] == 0]
    unfinished_rows = [r for r in rows if r["code"] != "de" and (r["sauber"] < TOTAL_MASTER or r["fallbacks"] > 0)]
    unfinished_rows.sort(key=lambda r: (r["pct"], -r["fallbacks"]), reverse=True)
    
    show_all = "--all" in sys.argv
    display_rows = de_row + finished_rows + unfinished_rows if show_all else unfinished_rows
    
    # Active process details
    active_lang_code = active_proc["lang"] if active_proc else (unfinished_rows[0]["code"] if unfinished_rows else None)
    active_row = next((r for r in rows if r["code"] == active_lang_code), None)
    chunk_info = get_chunk_info(active_lang_code)
    
    lines = []
    lines.append(f"📊 Translation Status Report (Master-Basis: {TOTAL_MASTER} Dateien)")
    lines.append(f"Timestamp: {timestamp}")
    if prev_time and prev_time != "Unbekannt":
        lines.append(f"Vergleich zum letzten Bericht: `{prev_time}`\n")
    else:
        lines.append("\n")
    
    if finished_rows:
        fin_codes = ", ".join([f"`{r['code']}`" for r in finished_rows])
        lines.append(f"✅ **{len(finished_rows)} Sprachen vollständig fertig (100%, 0 Fallbacks):** {fin_codes}\n")
    
    lines.append("🎯 Aktuell in Übersetzung (Höchste Prozentzahl unter 100%):\n")
    
    if active_row:
        lines.append(f"Sprache: {active_row['emoji']} {active_row['name']} ({active_row['code']})")
        if active_proc:
            if active_proc.get('is_stuck'):
                lines.append(f"Prozess-PID: ⚠️ {active_proc['pid']} (`{active_proc['cmd']}` – **EINGEFROREN / DEADLOCK ERKANNT**, CPU-Time: {active_proc['cputime']}, etime: {active_proc['etime']})")
            else:
                lines.append(f"Prozess-PID: {active_proc['pid']} (`{active_proc['cmd']}` – Ungepuffert & Aktiv, CPU-Time: {active_proc['cputime']})")
        else:
            lines.append("Prozess-PID: Nicht aktiv (Wartet auf Start)")
        
        file_str = chunk_info["file_name"] if chunk_info else "lektionen / wortliste"
        curr_c = chunk_info["curr_chunk"] if chunk_info else 1
        total_c = chunk_info["total_chunks"] if chunk_info else 1
        file_pct = round((curr_c / total_c) * 100.0, 1)
        lines.append(f"Aktuelle Datei / Chunk-Fortschritt: `{file_str}` (Sektion {curr_c}/{total_c} Chunks – {file_pct}% dieser Datei) | Gesamt: **{active_row['sauber']}/{TOTAL_MASTER} Dateien ({active_row['pct']}%)**")
        
        # Exact Pipeline Execution Queue for active language
        q = active_row["todo_queue"]
        if q:
            q_items = [f"`{fname}` ({reason})" for fname, reason in q[:8]]
            q_str = ", ".join(q_items)
            more_str = f" ... (+{len(q)-8} weitere)" if len(q) > 8 else ""
            lines.append(f"Pipeline-Queue ({len(q)} Dateien ausstehend): {q_str}{more_str}")
        else:
            lines.append("Pipeline-Queue: Keine (Alle Dateien in der Pipeline verarbeitet)")

        if active_row["delta_str"] != "—":
            lines.append(f"Delta zum letzten Bericht: **{active_row['delta_str']}**")

        lines.append("Server: 100% KOSTENLOS über den lokalen Server (`nyx.local:8000`).")
        perf_info = get_performance_info()
        if perf_info:
            target_tps = 9.7
            tps_val = perf_info['latest_tps']
            dev_pct = round(((target_tps - tps_val) / target_tps) * 100.0, 1) if tps_val < target_tps else 0.0
            
            if dev_pct > 10.0:
                lines.append(f"Performance: ⚠️ **ABWEICHUNG >10% VON SZENARIO B** ({tps_val} t/s vs. Soll {target_tps} t/s, -{dev_pct}%) | Ø {perf_info['avg_tps']} t/s – *Neustart-Schwelle: < 5.0 t/s*\n")
            else:
                lines.append(f"Performance: ⚡ **Szenario B im Soll** ({tps_val} t/s | Ø {perf_info['avg_tps']} t/s | Letzter Chunk: {perf_info['latest_tokens']} Tokens in {perf_info['latest_sec']}s) – *Neustart-Schwelle: < 5.0 t/s*\n")
        else:
            lines.append("Performance: ⚡ Aktiv (Warte auf ersten Chunk) – *Neustart-Schwelle: < 5.0 t/s*\n")
    
    lines.append("| Locale | Sprache | Sauber | Fallbacks | Pipeline Queue | Delta (Δ) | Fortschritt | Status |")
    lines.append("| :--- | :--- | :---: | :---: | :--- | :---: | :---: | :--- |")
    
    for idx, r in enumerate(display_rows):
        q = r["todo_queue"]
        if r["code"] == "de":
            status = "Master-Quelle"
            offen_str = "0 (Fertig)"
        elif r["pct"] >= 100.0 and len(q) == 0:
            status = "✅ 100% Fertig"
            offen_str = "0 (Fertig)"
        elif active_proc and r["code"] == active_proc["lang"]:
            file_str = chunk_info['file_name'] if chunk_info else 'in Bearbeitung'
            curr_c = chunk_info["curr_chunk"] if chunk_info else 1
            total_c = chunk_info["total_chunks"] if chunk_info else 1
            status = f"🎯 Aktiv (`{file_str}` Sektion {curr_c}/{total_c})"
            offen_str = f"{len(q)} ({', '.join([item[0] for item in q])})" if len(q) <= 3 and q else f"{len(q)} Dateien"
        elif not active_proc and ((show_all and idx == len(de_row) + len(finished_rows)) or (not show_all and idx == 0)):
            status = f"⚠️ Nächste (Wartet auf Start)"
            offen_str = f"{len(q)} ({', '.join([item[0] for item in q])})" if len(q) <= 3 and q else f"{len(q)} Dateien"
        elif (show_all and idx == len(de_row) + len(finished_rows)) or (not show_all and idx == 0):
            status = "🔄 Nächste Sprache"
            offen_str = f"{len(q)} ({', '.join([item[0] for item in q])})" if len(q) <= 3 and q else f"{len(q)} Dateien"
        else:
            status = "⌛ In Warteschlange"
            offen_str = f"{len(q)} ({', '.join([item[0] for item in q])})" if len(q) <= 3 and q else f"{len(q)} Dateien"
            
        code_str = f"`{r['code']}`"
        lines.append(f"| {code_str} | {r['name']} | {r['sauber']}/{TOTAL_MASTER} | {r['fallbacks']} | {offen_str} | {r['delta_str']} | {r['pct']:.1f}% | {status} |")

    report_text = "\n".join(lines)
    REPORT_FILE.write_text(report_text, encoding="utf-8")
    return report_text

if __name__ == "__main__":
    sys.path.insert(0, str(ROOT / "scripts"))
    print(generate_report())
