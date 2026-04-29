import os
import re
import sys

def check_markdown_file(filepath):
    errors = []
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
        lines = content.split('\n')

    # 1. Check YAML Frontmatter
    if not content.startswith('---\n'):
        errors.append("Missing YAML Frontmatter start ('---')")
    else:
        # Simple check for closing ---
        parts = content.split('---\n')
        if len(parts) < 3:
             errors.append("Missing YAML Frontmatter end ('---')")

    # 2. Check for exactly one H1
    h1_count = len(re.findall(r'^# ', content, re.MULTILINE))
    if h1_count == 0:
        errors.append("Missing H1 heading (# ...)")
    elif h1_count > 1:
        errors.append(f"Multiple H1 headings found ({h1_count})")

    # 3. Check for Cyrillic injections (Simplified logic from detect_cyrillic.py)
    # Range for Devanagari: \u0900-\u097F
    # Range for Cyrillic: \u0400-\u04FF
    devanagari_blocks = re.findall(r'[\u0900-\u097F]+', content)
    for block in devanagari_blocks:
        # This is a bit simplistic; the detection script usually looks for cyrillic in devanagari strings
        pass
    
    cyrillic_chars = re.findall(r'[\u0400-\u04FF]', content)
    # We allow Cyrillic if it's in the Bulgarian docs, but not in Devanagari text
    is_bg = "/bg/" in filepath
    if cyrillic_chars and not is_bg:
         errors.append(f"Found {len(cyrillic_chars)} Cyrillic characters in non-Bulgarian file.")

    # 4. Check for VitePress Admonitions (::: container)
    admonitions = re.findall(r'^::: ', content, re.MULTILINE)
    # This is just an info check, not strictly an error if missing, 
    # but we can check for unclosed containers
    containers = re.findall(r'^:::.*$', content, re.MULTILINE)
    if len(containers) % 2 != 0:
        errors.append("Unclosed VitePress container (::: )")

    return errors

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 qa_check.py <file_or_dir>")
        sys.exit(1)

    target = sys.argv[1]
    if os.path.isfile(target):
        files = [target]
    else:
        files = [os.path.join(dp, f) for dp, dn, filenames in os.walk(target) for f in filenames if f.endswith(".md")]

    total_errors = 0
    for f in files:
        file_errors = check_markdown_file(f)
        if file_errors:
            print(f"❌ {f}:")
            for err in file_errors:
                print(f"  - {err}")
            total_errors += len(file_errors)
        else:
            print(f"✅ {f}: Standard compliant.")

    if total_errors:
        print(f"\nTotal errors found: {total_errors}")
        sys.exit(1)
    else:
        print("\nAll checks passed!")
        sys.exit(0)
