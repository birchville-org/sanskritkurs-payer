"""
Force session state management and completion locks for translation pipeline.
"""

import os
import glob
import json
import time
import datetime
from .config import BASE_DIR
from .quality_control import scan_german_residues
from .terms import EXCLUDE_META

def get_force_session_path(lang: str) -> str:
    """Return path to force session timestamp file."""
    session_dir = os.path.join(BASE_DIR, ".payer", "sessions")
    os.makedirs(session_dir, exist_ok=True)
    return os.path.join(session_dir, f"{lang}_force.json")

def get_force_session_start_time(lang: str, init_if_missing: bool = True) -> float:
    """Get or initialize the start timestamp for a forced translation session."""
    p = get_force_session_path(lang)
    if os.path.exists(p):
        try:
            with open(p, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data.get("session_start", 0)
        except Exception:
            pass
    if init_if_missing:
        now = time.time()
        with open(p, 'w', encoding='utf-8') as f:
            json.dump({"session_start": now, "created_at": datetime.datetime.now().isoformat()}, f)
        return now
    return 0.0

def clear_force_session(lang: str):
    """Remove force session file when a language is 100% completed."""
    p = get_force_session_path(lang)
    if os.path.exists(p):
        try:
            os.remove(p)
        except Exception:
            pass

def is_language_completed(lang: str) -> bool:
    """Return True if language has 136 clean files with 0 fallbacks and 0 German residues."""
    if lang == "de":
        return True
    lang_dir = os.path.join(BASE_DIR, lang)
    if not os.path.exists(lang_dir):
        return False
    md_files = glob.glob(os.path.join(lang_dir, "**/*.md"), recursive=True)
    clean_files = [f for f in md_files if os.path.basename(f) not in EXCLUDE_META and "qa_viewer" not in f and "deleteme" not in f]
    if len(clean_files) < 136:
        return False
    for fpath in clean_files:
        try:
            with open(fpath, 'r', encoding='utf-8', errors='ignore') as f:
                c = f.read()
            if scan_german_residues(c, target_lang=lang) or 'TODO: Fallback translation' in c:
                return False
        except Exception:
            return False
    return True
