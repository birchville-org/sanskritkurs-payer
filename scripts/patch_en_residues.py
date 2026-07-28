import os
import sys
import time
import re
import json

# Add the scripts directory to the path so we can import from lan_translate
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from lan_translate import log_failure, BASE_DIR, LANG_NAMES, SONNET_MODEL, SONNET_API_URL

_EN_RESIDUE_PATTERNS = re.compile(
    r'\b(?:stem(?:s)?|root(?:s)?|example(?:s)?|present class|present stem|'
    r'aorist class|aorist stem|perfect stem|genitive case|nominative case|'
    r'accusative case|instrumental case|dative case|ablative case|locative case|'
    r'vocative case|stem gradation|strong stem|weak stem|verb root|noun stem)\b',
    re.IGNORECASE
)

# All target languages minus English
langs = ['bg', 'uk', 'hi', 'ar', 'ta', 'la', 'rm', 'arc', 'it', 'es', 'ru', 'fr', 'pa', 'ro', 'id', 'zh-CN', 'he']

def scan_en_residues(content: str) -> list:
    flagged = []
    in_frontmatter = False
    in_deleteme = False
    frontmatter_count = 0

    for i, line in enumerate(content.split('\n')):
        stripped = line.strip()

        # Track YAML frontmatter
        if stripped == '---' and i < 5:
            frontmatter_count += 1
            in_frontmatter = frontmatter_count == 1
            if frontmatter_count == 2:
                in_frontmatter = False
            continue
        if in_frontmatter:
            continue

        # Track ::: deleteme-box containers (these often contain english citations/licenses)
        if '::: deleteme-box' in stripped or ':::deleteme-box' in stripped:
            in_deleteme = True
        if in_deleteme and stripped == ':::':
            in_deleteme = False
            continue
        if in_deleteme:
            continue

        # Skip blockquotes as they often contain original English Wikipedia quotes (e.g. "> In the oldest parts of the Ṛgveda...")
        if stripped.startswith('>'):
            continue

        # Skip lines that are purely Devanāgarī, IAST, or URLs
        if not stripped or stripped.startswith('http') or stripped.startswith('<!--'):
            continue

        # Skip image metadata captions if they contain [Bildquelle / [Image
        if '[Bildquelle' in line or '[Image' in line or '[image' in line or '[चित्र स्रोत' in line:
            continue

        # Skip grammar-box headers
        if stripped.startswith(':::') or stripped == '---':
            continue

        if _EN_RESIDUE_PATTERNS.search(line):
            flagged.append((i, line))

    return flagged

def sonnet_patch_en_residues(content: str, flagged_lines: list, target_lang: str) -> str:
    api_key = 'local'
    lang_name = LANG_NAMES.get(target_lang, target_lang)
    lines = content.split('\n')
    flagged_indices = {i for i, _ in flagged_lines}

    # Build a context window: flagged lines ± 2 lines of context
    context_indices = set()
    for i in flagged_indices:
        for j in range(max(0, i - 2), min(len(lines), i + 3)):
            context_indices.add(j)

    # Format the snippet with line markers
    snippet_lines = []
    for i in sorted(context_indices):
        marker = ">>" if i in flagged_indices else "  "
        snippet_lines.append(f"[L{i}]{marker} {lines[i]}")
    snippet = '\n'.join(snippet_lines)

    system = (
        f"You are a scholarly translator fixing English residues in a {lang_name} Sanskrit-education text. "
        "Lines marked with >> contain English words that were not translated. "
        "Rules: "
        "(1) Translate ONLY the English words on lines marked >>. "
        "(2) Preserve all Markdown syntax, IAST, Devanāgarī (⟪...⟫), and container syntax exactly. "
        "(3) Return ONLY the corrected lines in the format [LN] corrected_text — one per line. "
        "(4) Do NOT return context lines (without >>). "
        "(5) Keep the scholarly editorial tone."
    )
    data = {
        "model": SONNET_MODEL,
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": snippet}
        ],
        "temperature": 0.1,
        "max_tokens": 2048,
    }

    import subprocess as _sp
    curl_cmd = [
        'curl', '-s', '-X', 'POST', SONNET_API_URL,
        '-H', 'Content-Type: application/json',
        '-H', f'Authorization: Bearer {api_key}',
        '-d', json.dumps(data), '--max-time', '120'
    ]

    try:
        proc = _sp.run(curl_cmd, capture_output=True, text=True, timeout=125)
        if proc.returncode != 0:
            raise OSError(f"curl exit {proc.returncode}: {proc.stderr[:200]}")
        res = json.loads(proc.stdout)
        patched_text = res['choices'][0]['message']['content']
    except Exception as e:
        sys.stdout.write(f"  [!] SONNET FALLBACK API error: {e}\n")
        sys.stdout.flush()
        return content

    patched_lines = list(lines)
    for resp_line in patched_text.split('\n'):
        m = re.match(r'^\[L(\d+)\](?:>>)?\s*(.*)', resp_line.strip())
        if m:
            idx = int(m.group(1))
            corrected = m.group(2)
            if 0 <= idx < len(patched_lines):
                patched_lines[idx] = corrected

    return '\n'.join(patched_lines)

def main():
    print("Starting Sonnet patch for ENGLISH residues...")
    for lang in langs:
        print(f"\n=== Processing {lang} ===")
        lesson_dir = os.path.join(BASE_DIR, lang, "lektionen")
        if not os.path.isdir(lesson_dir):
            continue
        
        for l_num in range(1, 62):
            filename = f"lektion{l_num:02d}.md"
            filepath = os.path.join(lesson_dir, filename)
            if not os.path.exists(filepath):
                continue
                
            with open(filepath, encoding='utf-8') as f:
                content = f.read()
                
            flagged = scan_en_residues(content)
            if not flagged:
                continue
                
            print(f"[{lang}] {filename}: {len(flagged)} EN residues found.")
            patched = sonnet_patch_en_residues(content, flagged, lang)
            
            flagged_after = scan_en_residues(patched)
            
            # Write patched content atomically
            import tempfile
            tmp_fd, tmp_p = tempfile.mkstemp(dir=lesson_dir, suffix='.tmp')
            with os.fdopen(tmp_fd, 'w', encoding='utf-8') as wf:
                wf.write(patched)
            os.replace(tmp_p, filepath)
            
            resolved = len(flagged) - len(flagged_after)
            print(f"  ✓ Patched {resolved}/{len(flagged)} EN residues. {len(flagged_after)} remaining.")
            
            if flagged_after:
                log_failure(lang, filename, 'EN_RESIDUE', flagged_after, f"After Sonnet EN patch: {len(flagged_after)} unresolved")
                
            time.sleep(0.5)

if __name__ == "__main__":
    main()
