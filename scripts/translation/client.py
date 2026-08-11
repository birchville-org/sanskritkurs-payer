"""
LLM Client, API communication, TPS performance monitoring, auto-restart triggers, and Lingua language detection.
"""

import os
import sys
import time
import json
import subprocess
from .config import API_URL, MODEL, LANG_NAMES
from .protector import (
    protect_devanagari, restore_devanagari,
    protect_iast_lines, restore_iast_lines,
    protect_br, restore_br,
    protect_structure, restore_structure
)

try:
    from lingua import Language, LanguageDetectorBuilder
    _LINGUA_DETECTOR = LanguageDetectorBuilder.from_all_languages().with_low_accuracy_mode().build()
except Exception:
    _LINGUA_DETECTOR = None

def translate_text(text, target_lang):
    lang_name = LANG_NAMES.get(target_lang, target_lang)
    _mark_skt = (target_lang == 'hi')
    protected, deva_registry = protect_devanagari(text)
    protected, iast_registry = protect_iast_lines(protected)
    protected = protect_br(protected)
    protected, struct_registry = protect_structure(protected)
    heading_mappings = {
        'en': "e.g. '# Lesson N'",
        'es': "e.g. '# Lección N'",
        'it': "e.g. '# Lezione N'",
        'fr': "e.g. '# Leçon N'",
        'hi': "e.g. '# पाठ N'",
        'ru': "e.g. '# Урок N'",
        'uk': "e.g. '# Урок N'",
        'bg': "e.g. '# Урок N'",
        'ta': "e.g. '# பாடம் N'",
        'pa': "e.g. '# ਪਾਠ N'",
        'la': "e.g. '# Lectio N'",
        'rm': "e.g. '# Lecziun N'",
        'ro': "e.g. '# Lecție N'",
        'he': "e.g. '# שיעור N'",
        'id': "e.g. '# Pelajaran N'",
        'zh-CN': "e.g. '# 第N课'",
        'ar': "e.g. '# الدرس N'",
        'arc': "e.g. '# ܡܠܦܢܘܬܐ N'",
        'th': "e.g. '# บทที่ N'",
        'el': "e.g. '# Μάθημα N'",
        'fa': "e.g. '# درس N'",
        'cop': "e.g. '# ⲙⲁⲑⲏⲙⲁ N'",
    }
    target_example = heading_mappings.get(target_lang, "")
    if target_example:
        target_example = f" ({target_example})"
    system = (
        f"You are a scholarly translator. Translate ALL German text in this Sanskrit-education markdown to {lang_name}. "
        "Rules: "
        "(1) Translate every German word — including captions, image descriptions, verse translations, and prose. "
        "(2) Preserve unchanged: Markdown syntax, IAST transliterations, YAML frontmatter keys, HTML comments, ⟨DEVA_N⟩ placeholders, ⟨IAST_L_N⟩ placeholders, ⟨BR⟩ placeholders, and ⟨STRUCT_N⟩ placeholders. "
        f"(3) Translate '# Lektion N' headings to the target-language equivalent{target_example}. "
        "(4) NEVER add TODO comments, fallback markers, or any annotations of your own. If unsure how to translate a word or sentence into the target language, translate it into English as a fallback (NEVER leave it in German). "
        "(5) Keep the scholarly editorial tone throughout. "
        "(6) CRITICAL: Preserve the exact line count of the source. Every source line must appear as exactly one output line. NEVER delete, merge, or collapse lines. "
        "(6a) CRITICAL: Each non-empty line of the input is prefixed with a bracketed identifier like [L0], [L1], [L2]... You MUST preserve these identifiers exactly at the start of each translated line. Do not translate, modify, or remove them. "
        "(7) CRITICAL: Copy every ⟨DEVA_N⟩ and ⟨IAST_L_N⟩ placeholder character-for-character. They are replaced with Devanāgarī and IAST text after translation — do NOT interpret, transliterate, or remove them. "
        "(7a) CRITICAL: Lines consisting ONLY of ⟨DEVA_N⟩ tokens (and spaces/punctuation like ।  ॥) are Sanskrit verse lines. Copy every token on that line verbatim. NEVER transliterate Sanskrit verses into the target script — the placeholders will be restored to Devanāgarī automatically. "
        "(7b) CRITICAL: Preserve ALL Markdown image syntax exactly: ![alt](/path/to/image.jpg) — never drop the parentheses around the image path. "
        "(8) Numbered exercise sentences (e.g. '3. Śūdras erlangen...', '4. Die Kṣatriyas...') MUST be translated to the target language even when they begin with Sanskrit proper nouns in IAST notation. The IAST proper noun is preserved as-is; only the surrounding German words are translated."
    )
    best_result = None
    best_missing: list = list(deva_registry.keys())
    is_fallback = False

    max_ph_retries = 4
    for ph_attempt in range(max_ph_retries):
        current_api_url = API_URL
        current_model = MODEL
        is_fallback = False

        temps = [0.1, 0.3, 0.5, 0.7]
        penalties = [1.15, 1.20, 1.25, 1.30]
        temperature = temps[min(ph_attempt, len(temps)-1)]
        repetition_penalty = penalties[min(ph_attempt, len(penalties)-1)]

        # Prepare indexed prompt
        source_lines = protected.split('\n')
        indexed_lines = []
        for idx, l in enumerate(source_lines):
            if l.strip():
                indexed_lines.append(f"[L{idx}] {l}")
            else:
                indexed_lines.append(l)
        indexed_protected = '\n'.join(indexed_lines)

        user_prompt = indexed_protected
        if ph_attempt > 0 and 'qc_reason' in locals():
            if is_fallback:
                sys.stdout.write(f"\n[{target_lang}] FALLBACK TRIGGERED: Switching to OpenRouter ({current_model}) for this chunk due to persistent QC failures.\n")
                sys.stdout.flush()
            user_prompt = f"CRITICAL CORRECTION REQUIRED:\nYour previous translation failed Quality Control for this reason: {qc_reason}\n\nYou MUST fix this error. If you failed to translate sentences, translate EVERY single word now. If you dropped lines, preserve line count strictly. Translate the following text:\n\n{indexed_protected}"

        data = {
            "model": current_model,
            "messages": [
                {"role": "system", "content": system},
                {"role": "user", "content": user_prompt}
            ],
            "temperature": temperature,
            "max_tokens": 8192,
            "repetition_penalty": repetition_penalty
        }

        max_retries = 5
        got_response = False
        for attempt in range(max_retries):
            try:
                from .lock import touch_nyx_lock_heartbeat
                touch_nyx_lock_heartbeat()

                start_time = time.time()
                curl_cmd = ['curl', '-s', '-X', 'POST', current_api_url, '-H', 'Content-Type: application/json']
                api_key = 'local'
                curl_cmd.extend(['-H', f"Authorization: Bearer {api_key}"])
                curl_cmd.extend(['-d', json.dumps(data), '--connect-timeout', '15', '--max-time', '900', '--keepalive-time', '15'])

                _proc = subprocess.run(
                    curl_cmd,
                    capture_output=True, text=True, timeout=905
                )
                end_time = time.time()
                if _proc.returncode != 0:
                    raise OSError(f"curl exit {_proc.returncode}: {_proc.stderr[:200]}")
                res_data = json.loads(_proc.stdout)
                if 'error' in res_data:
                    raise RuntimeError(f"API Error: {res_data['error']}")
                raw_result = res_data['choices'][0]['message']['content']
                got_response = True

                # Parse and restore lines based on prefixes
                import re
                result_lines = raw_result.split('\n')
                restored_lines = [None] * len(source_lines)
                unmatched_lines = []
                for r_line in result_lines:
                    m = re.match(r'^\s*\[[LЛlл]?(\d+)\]\s*(.*)$', r_line)
                    if m:
                        idx = int(m.group(1))
                        content = m.group(2)
                        if 0 <= idx < len(source_lines):
                            restored_lines[idx] = content
                        else:
                            unmatched_lines.append(r_line)
                    else:
                        if r_line.strip():
                            unmatched_lines.append(r_line)

                unmatched_idx = 0
                line_dropped = False
                for idx, src_l in enumerate(source_lines):
                    if src_l.strip():
                        if restored_lines[idx] is None:
                            if unmatched_idx < len(unmatched_lines):
                                clean_line = re.sub(r'^\s*\[[LЛlл]?\d+\]\s*', '', unmatched_lines[unmatched_idx])
                                restored_lines[idx] = clean_line
                                unmatched_idx += 1
                            else:
                                line_dropped = True
                                restored_lines[idx] = src_l
                    else:
                        restored_lines[idx] = ''

                result = '\n'.join(restored_lines)
                got_response = True

                # Performance Monitoring (Log speed, rely on connection timeout/death for restarts)
                if 'usage' in res_data and 'completion_tokens' in res_data['usage']:
                    comp_tokens = res_data['usage']['completion_tokens']
                    elapsed = end_time - start_time
                    if elapsed > 0:
                        tps = comp_tokens / elapsed
                        ts = time.strftime('%H:%M:%S')
                        sys.stdout.write(f"[{ts}]      [Speed: {tps:.1f} t/s | {comp_tokens} tokens in {elapsed:.1f}s]\n")
                        sys.stdout.flush()

                # QUALITY CONTROL (QC)
                source_lines = protected.split('\n')
                result_lines = result.split('\n')
                qc_failed = False
                qc_reason = ""

                if line_dropped:
                    qc_failed = True
                    qc_reason = "Line dropped by LLM (missing prefix line restoration)"

                if not qc_failed and len([l for l in source_lines if l.strip()]) != len([l for l in result_lines if l.strip()]):
                    qc_failed = True
                    qc_reason = f"Line count mismatch (Expected non-empty: {len([l for l in source_lines if l.strip()])}, Got: {len([l for l in result_lines if l.strip()])})"
                elif not qc_failed:
                    missing_struct = [k for k in struct_registry if k not in result]
                    if missing_struct:
                        qc_failed = True
                        qc_reason = f"Missing structure placeholders: {len(missing_struct)} dropped"

                if not qc_failed and target_lang != 'de':
                    safe_german_words = ['und', 'oder', 'nicht', 'sich', 'wird', 'werden', 'auch', 'dass', 'auf', 'für']
                    ger_pattern = re.compile(r'\b(' + '|'.join(safe_german_words) + r')\b', re.IGNORECASE)
                    ger_result_count = len(ger_pattern.findall(result))
                    if ger_result_count >= 3:
                        ger_source_count = len(ger_pattern.findall(protected))
                        if ger_result_count >= (ger_source_count * 0.2):
                            qc_failed = True
                            qc_reason = f"Untranslated German detected ({ger_result_count} marker words found)"

                if not qc_failed and target_lang not in ('de', 'en'):
                    safe_english_words = ['the', 'is', 'to', 'and', 'that', 'of', 'for', 'this', 'are', 'with']
                    en_pattern = re.compile(r'\b(' + '|'.join(safe_english_words) + r')\b', re.IGNORECASE)
                    en_result_count = len(en_pattern.findall(result))
                    if en_result_count >= 3:
                        en_source_count = len(en_pattern.findall(protected))
                        if en_result_count > en_source_count + 2:
                            qc_failed = True
                            qc_reason = f"English fallback leak detected ({en_result_count} English marker words found)"

                if qc_failed:
                    if ph_attempt < max_ph_retries - 1:
                        sys.stdout.write(f"[{target_lang}] QC failed: {qc_reason} — retrying ({ph_attempt + 2}/{max_ph_retries}, T={temperature})...\n")
                        sys.stdout.flush()
                        break
                    else:
                        sys.stdout.write(f"[{target_lang}] [!] QC REJECTED: {qc_reason} on final attempt {ph_attempt + 1}. Refusing un-QC'd output.\n")
                        sys.stdout.flush()
                        return f"ERROR: Quality Control Failed - {qc_reason}", ph_attempt

                missing = [k for k in deva_registry if k not in result]
                if len(missing) < len(best_missing):
                    best_result = result
                    best_missing = missing
                if not missing:
                    result = restore_devanagari(result, deva_registry, _mark_skt)
                    result = restore_iast_lines(result, iast_registry)
                    result = restore_br(result)
                    result = restore_structure(result, struct_registry)
                    return result, ph_attempt

                if ph_attempt < max_ph_retries - 1:
                    sys.stdout.write(
                        f"[{target_lang}] Placeholder drop ({len(missing)}): "
                        f"{missing[:3]}{'…' if len(missing) > 3 else ''} "
                        f"— retrying ({ph_attempt + 2}/{max_ph_retries}, T={temperature})...\n"
                    )
                    sys.stdout.flush()
                break
            except Exception as e:
                err_str = str(e)
                wait_time = (2 ** attempt) * 5

                err_lower = err_str.lower()
                is_local = 'localhost' in current_api_url or '127.0.0.1' in current_api_url or 'nyx.local' in current_api_url
                if is_local and ("exit 28" in err_str or "timeout" in err_lower or "500" in err_str or "exit 7" in err_str or "exit 56" in err_str or "exit 52" in err_str or "refused" in err_lower or "choices" in err_lower):
                    ts = time.strftime('%H:%M:%S')
                    sys.stdout.write(f"\n[{ts}] [{target_lang}] Temporary connection issue ({err_str}). Retrying HTTP request in {wait_time}s...\n")
                    sys.stdout.flush()

                if "prefill_memory_exceeded" in err_str or "prefill_memory_exceeded" in err_lower:
                    sys.stdout.write(f"\n[!] oMLX Prefill Memory Guard error: {err_str}\nSkipping immediately to next fallback tier...\n")
                    sys.stdout.flush()
                    break

                if "API Error" in err_str:
                    if "'code': 404" in err_str or "'code': 400" in err_str:
                        sys.stdout.write(f"\n[!] API Error 400/404 (Bad Request/Model not found): {err_str}\nSkipping to next fallback tier...\n")
                        sys.stdout.flush()
                        break
                    if "'code': 402" in err_str or "'code': 401" in err_str:
                        sys.stdout.write(f"\n[FATAL] Unrecoverable Auth/Credit API Error encountered: {err_str}\nAborting translation completely.\n")
                        sys.stdout.flush()
                        sys.exit(1)

                msg = f"[{time.strftime('%H:%M:%S')}] [{target_lang}] Connection failed (attempt {attempt+1}/{max_retries}): {err_str}. Retrying in {wait_time}s...\n"
                sys.stdout.write(msg)
                sys.stdout.flush()
                time.sleep(wait_time)

        if not got_response:
            if ph_attempt < max_ph_retries - 1:
                sys.stdout.write(f"[{target_lang}] WARNING: API failed. Escalating to next fallback tier (attempt {ph_attempt + 2})...\n")
                sys.stdout.flush()
                continue
            sys.stdout.write(f"[{target_lang}] FATAL: Maximum inner connection retries reached and no more fallback tiers available.\n")
            sys.stdout.flush()
            return f"ERROR: Failed to translate after {max_retries} attempts.", ph_attempt

    sys.stdout.write(
        f"[{target_lang}] WARNING: LLM dropped {len(best_missing)} Devanāgarī "
        f"placeholder(s) after {max_ph_retries} attempts: "
        f"{best_missing[:5]}{'…' if len(best_missing) > 5 else ''}\n"
    )
    sys.stdout.flush()
    if best_result is None:
        best_result = protected
    result = restore_devanagari(best_result, deva_registry, _mark_skt)
    result = restore_iast_lines(result, iast_registry)
    result = restore_br(result)
    result = restore_structure(result, struct_registry)
    return result, max_ph_retries - 1
