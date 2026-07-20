#!/bin/bash

# Script to translate multiple languages sequentially with robust retries and fallback
# Order: fi, hu, th, el, cop, grc, fa, nl, af, lt, sh, sq, am

LANGUAGES=("fi" "hu" "th" "el" "cop" "grc" "fa" "nl" "af" "lt" "sh" "sq" "am")
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

echo "Starting massive language expansion with robust fallbacks..."
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