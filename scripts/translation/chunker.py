"""
Chunking utilities, hashing, and progress heartbeats for translation pipeline.
"""

import hashlib
import json
import time

def hash_chunk(chunk: str) -> str:
    """Return MD5 hash of stripped chunk string."""
    return hashlib.md5(chunk.strip().encode('utf-8')).hexdigest()

def chunk_content(content: str, max_chunk_size: int = 1500) -> list:
    """Splits content into safe, manageable chunks of max ~1500 characters breaking at markdown boundaries."""
    lines = content.split('\n')
    chunks = []
    current_chunk = []
    current_size = 0
    MAX_CHUNK = max_chunk_size

    for line in lines:
        is_header = line.startswith('## ') or line.startswith('### ')
        is_safe_break = (not line.strip() or line.startswith(':::')) and not line.startswith('|')

        if (is_header or is_safe_break) and current_chunk and current_size >= MAX_CHUNK:
            chunks.append('\n'.join(current_chunk))
            current_chunk = []
            current_size = 0

        current_chunk.append(line)
        current_size += len(line) + 1

    if current_chunk:
        c_str = '\n'.join(current_chunk)
        if c_str.strip():
            chunks.append(c_str)

    return [c for c in chunks if c.strip()]

def touch_progress_heartbeat(filename: str, chunk_idx: int, total_chunks: int, lang: str):
    """Write timestamp to /tmp/payer_progress_heartbeat.json ONLY when a chunk/file is successfully written."""
    try:
        data = {
            "timestamp": time.time(),
            "time_str": time.strftime("%Y-%m-%d %H:%M:%S"),
            "filename": filename,
            "chunk": f"{chunk_idx}/{total_chunks}",
            "lang": lang
        }
        with open("/tmp/payer_progress_heartbeat.json", "w", encoding="utf-8") as f:
            json.dump(data, f)
    except Exception:
        pass
