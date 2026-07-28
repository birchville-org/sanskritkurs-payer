#!/bin/bash

# Script to translate multiple languages sequentially with robust retries and fallback
# Dynamic Order: Unfinished languages sorted by highest completion percentage descending
LANGUAGES=($(python3 -c "
import sys; sys.path.insert(0, 'scripts')
from generate_report import LANG_MAP, DOCS, TOTAL_MASTER

rows = []
for code, name, emoji in LANG_MAP:
    if code == 'de': continue
    p = DOCS / code
    if not p.exists():
        rows.append({'code': code, 'pct': 0.0, 'fallbacks': 0})
        continue
    all_md = list(p.glob('**/*.md'))
    EXCLUDE_META = {'licenses.md', 'AUTHORS_GUIDE.md', 'settings.md', 'impressum.md', 'grammatik.md', 'themen.md', 'qa_help.md'}
    files = [f for f in all_md if f.name not in EXCLUDE_META and 'qa_viewer' not in f.name and 'deleteme' not in f.name]
    fallbacks = sum(1 for f in files if 'TODO: Fallback translation' in f.read_text(encoding='utf-8', errors='ignore'))
    sauber = min(TOTAL_MASTER, len(files) - fallbacks)
    if fallbacks > 0:
        pct = round((sauber / TOTAL_MASTER) * 100.0, 1)
        if pct >= 100.0: pct = 99.3
    else:
        pct = min(100.0, round((sauber / TOTAL_MASTER) * 100.0, 1))
    rows.append({'code': code, 'pct': pct, 'fallbacks': fallbacks, 'sauber': sauber})

unfinished = [r for r in rows if r['pct'] < 100.0 or r['fallbacks'] > 0]
unfinished.sort(key=lambda r: (r['pct'], -r['fallbacks']), reverse=True)
print(' '.join(r['code'] for r in unfinished))
"))
MAX_ATTEMPTS=3
RETRY_DELAY=30

run_with_retry() {
    local lang=$1
    local attempt=1
    while [ $attempt -le $MAX_ATTEMPTS ]; do
        echo "============================================================"
        echo "[$lang] Starting Translation Run (Attempt $attempt/$MAX_ATTEMPTS)"
        echo "============================================================"
        
        if python3 scripts/lan_translate.py --lang "$lang" all; then
            echo "[$lang] ✓ Completed successfully."
            return 0
        else
            echo "[$lang] ⚠️ Attempt $attempt failed with error."
            if [ $attempt -lt $MAX_ATTEMPTS ]; then
                echo "[$lang] Waiting $RETRY_DELAY seconds before next retry..."
                sleep $RETRY_DELAY
            fi
            attempt=$((attempt+1))
        fi
    done
    echo "[$lang] ❌ Translation failed after $MAX_ATTEMPTS attempts. Skipping to next language..."
    echo "$lang" >> translation_failures.log
    return 1
}

echo "Starting massive language expansion in strict order of highest percentage descending..."
echo "" > translation_failures.log

for lang in "${LANGUAGES[@]}"; do
    run_with_retry "$lang"
done

echo "Translation sequence finished!"
if [ -s translation_failures.log ]; then
    echo "⚠️ The following languages failed to translate completely: $(cat translation_failures.log | tr '\n' ' ')"
else
    echo "🎉 All languages completed successfully!"
fi