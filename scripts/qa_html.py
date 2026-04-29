import os
import sys

def check_html_file(filepath):
    errors = []
    try:
        with open(filepath, 'rb') as f:
            raw = f.read()
            # Try to decode as UTF-8
            try:
                content = raw.decode('utf-8')
            except UnicodeDecodeError:
                errors.append("File is not UTF-8 encoded.")
                return errors

        # 1. Check for Meta Charset
        if 'charset=windows-1252' in content:
            errors.append("Legacy meta charset found (windows-1252). Should be updated to utf-8 if file is converted.")

        # 2. Check for Übersicht marking
        if "Übersicht" in content:
            if "<!-- SKIP_TRANSLATION_START -->" not in content:
                errors.append("Found 'Übersicht' section but missing <!-- SKIP_TRANSLATION_START --> marker.")

    except Exception as e:
        errors.append(f"Error reading file: {e}")

    return errors

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 qa_html.py <file_or_dir>")
        sys.exit(1)

    target = sys.argv[1]
    if os.path.isfile(target):
        files = [target]
    else:
        files = [os.path.join(dp, f) for dp, dn, filenames in os.walk(target) for f in filenames if f.endswith(".htm") or f.endswith(".html")]

    total_errors = 0
    for f in files:
        file_errors = check_html_file(f)
        if file_errors:
            print(f"❌ {f}:")
            for err in file_errors:
                print(f"  - {err}")
            total_errors += len(file_errors)
        # else:
        #     print(f"✅ {f}: Standard compliant.")

    if total_errors:
        print(f"\nTotal issues found: {total_errors}")
    else:
        print("\nAll HTML checks passed!")
