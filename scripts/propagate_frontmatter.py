#!/usr/bin/env python3
"""
propagate_frontmatter.py — Injects translated frontmatter into target-language lesson files.

For each lesson in range [start, end], for each target language:
  - Skips files that already have 'title'
  - Reads title/subtitle from DE source (must already have been populated by add_frontmatter.py)
  - Batch-translates subtitles via LLM (one call per language for all lessons)
  - Writes translated frontmatter into target file, preserving lesson_id, status, last_reconstructed

Usage:
  python3 scripts/propagate_frontmatter.py [--range START END] [--langs LANG ...]
  python3 scripts/propagate_frontmatter.py --range 1 20 --langs en it bg ru uk
"""

import os
import re
import sys
import json
import urllib.request

BASE_DIR = os.path.join(os.path.dirname(__file__), '..', 'docs')
MODEL = "Qwen3.6-35B-A3B-UD-Q4_K_M.gguf"
API_URL = "http://192.168.1.22:8000/v1/chat/completions"

TITLE_PREFIX = {
    'en': 'Lesson',
    'it': 'Lezione',
    'bg': 'Урок',
    'ru': 'Урок',
    'uk': 'Урок',
}

CATEGORY = {
    'en': 'Grammar',
    'it': 'Grammatica',
    'bg': 'Граматика',
    'ru': 'Грамматика',
    'uk': 'Граматика',
}

LANG_NAMES = {
    'en': 'English',
    'it': 'Italian',
    'bg': 'Bulgarian',
    'ru': 'Russian',
    'uk': 'Ukrainian',
}


def parse_frontmatter(content):
    if not content.startswith('---\n'):
        return None, {}, content
    end = content.find('\n---', 3)
    if end == -1:
        return None, {}, content
    fm_block = content[4:end]
    body = content[end + 4:]
    fm_lines = fm_block.splitlines()
    fm_keys = {}
    for line in fm_lines:
        m = re.match(r'^(\w+):\s*(.*)', line)
        if m:
            fm_keys[m.group(1)] = m.group(2).strip('"').strip("'")
    return fm_lines, fm_keys, body


def batch_translate_subtitles(subtitles_de, lang):
    """Translate {lesson_num_str: subtitle_de} → {lesson_num_str: subtitle_lang} in one LLM call."""
    input_json = json.dumps(subtitles_de, ensure_ascii=False, indent=None)
    system = (
        f"You are a translator for a Sanskrit grammar course. "
        f"Translate the German lesson subtitles in the JSON below to {LANG_NAMES[lang]}. "
        "Preserve ALL IAST transliterations (ā, ī, ū, ṛ, ṝ, ṁ, ṃ, ḥ, ś, ṣ, ṭ, ḍ, ṇ, ñ, ṅ, etc.) exactly as-is. "
        "Preserve all Devanāgarī characters exactly as-is. "
        "Output ONLY a valid JSON object with the same integer keys and translated string values. "
        "No explanation, no markdown fences, no extra text."
    )
    payload = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": input_json},
        ],
        "temperature": 0.3,
        "max_tokens": 2000,
    }
    body_bytes = json.dumps(payload, ensure_ascii=False).encode('utf-8')
    req = urllib.request.Request(API_URL, data=body_bytes,
                                 headers={'Content-Type': 'application/json'})
    with urllib.request.urlopen(req, timeout=60) as resp:
        result = json.loads(resp.read().decode('utf-8'))
    text = result['choices'][0]['message']['content'].strip()
    # Strip markdown fences if the model adds them
    text = re.sub(r'^```(?:json)?\s*', '', text, flags=re.MULTILINE)
    text = re.sub(r'```\s*$', '', text, flags=re.MULTILINE)
    return json.loads(text.strip())


def inject_frontmatter(filepath, title, subtitle, category):
    with open(filepath, encoding='utf-8') as f:
        content = f.read()
    fm_lines, fm_keys, body = parse_frontmatter(content)
    if fm_lines is None:
        print(f"    SKIP (no frontmatter): {os.path.basename(filepath)}")
        return False
    if 'title' in fm_keys:
        print(f"    SKIP (already has title): {os.path.basename(filepath)}")
        return False

    new_lines = [f'title: {title}']
    if subtitle:
        escaped = subtitle.replace('"', '\\"')
        new_lines.append(f'subtitle: "{escaped}"')
    new_lines.extend(fm_lines)
    if 'category' not in fm_keys:
        new_lines.append(f'category: "{category}"')
    if 'status' not in fm_keys:
        new_lines.append('status: stable')

    new_content = '---\n' + '\n'.join(new_lines) + '\n---' + body
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print(f'    UPDATED {os.path.basename(filepath)}: "{title}"')
    return True


def main():
    args = sys.argv[1:]
    start, end = 1, 20
    langs = list(TITLE_PREFIX.keys())

    if '--range' in args:
        i = args.index('--range')
        start, end = int(args[i + 1]), int(args[i + 2])
    if '--langs' in args:
        i = args.index('--langs')
        langs = [a for a in args[i + 1:] if not a.startswith('--')]

    print(f'propagate_frontmatter.py — lessons {start}–{end}, langs: {", ".join(langs)}\n')

    # Step 1: Find which lessons/langs need updating and collect DE subtitles
    work = {}   # {lang: {num_str: subtitle_de}}
    for lang in langs:
        work[lang] = {}
        for num in range(start, end + 1):
            fname = f'lektion{num:02d}.md'
            de_path = os.path.join(BASE_DIR, 'lektionen', fname)
            lang_path = os.path.join(BASE_DIR, lang, 'lektionen', fname)
            if not os.path.exists(de_path) or not os.path.exists(lang_path):
                continue
            with open(lang_path, encoding='utf-8') as f:
                _, lm_keys, _ = parse_frontmatter(f.read())
            if 'title' in lm_keys:
                continue
            with open(de_path, encoding='utf-8') as f:
                _, de_keys, _ = parse_frontmatter(f.read())
            work[lang][str(num)] = de_keys.get('subtitle', '')

    total = sum(len(v) for v in work.values())
    if total == 0:
        print('Nothing to do — all files already have title.')
        return

    for lang in langs:
        if work[lang]:
            print(f'[{lang}] {len(work[lang])} lesson(s) need updating: {", ".join(sorted(work[lang], key=int))}')

    # Step 2: Batch-translate subtitles per language
    print()
    translations = {}
    for lang in langs:
        with_subtitle = {k: v for k, v in work[lang].items() if v}
        if not with_subtitle:
            translations[lang] = {}
            continue
        print(f'[{lang}] Translating {len(with_subtitle)} subtitle(s) via LLM...')
        try:
            result = batch_translate_subtitles(with_subtitle, lang)
            translations[lang] = result
            print(f'[{lang}] Done.')
        except Exception as e:
            print(f'[{lang}] ERROR: {e}  — will use DE subtitles as fallback')
            translations[lang] = {}

    # Step 3: Inject frontmatter
    print()
    for lang in langs:
        if not work[lang]:
            continue
        print(f'[{lang}]')
        for num_str in sorted(work[lang], key=int):
            num = int(num_str)
            fname = f'lektion{num:02d}.md'
            lang_path = os.path.join(BASE_DIR, lang, 'lektionen', fname)
            subtitle_de = work[lang][num_str]
            subtitle = translations[lang].get(num_str) or translations[lang].get(str(num)) or subtitle_de
            title = f'{TITLE_PREFIX[lang]} {num}'
            inject_frontmatter(lang_path, title, subtitle, CATEGORY[lang])

    print('\nDone.')


if __name__ == '__main__':
    main()
