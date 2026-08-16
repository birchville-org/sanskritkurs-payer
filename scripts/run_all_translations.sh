#!/bin/bash

# Enforce single runner instance using cross-platform Python lock on inherited file descriptor 200
exec 200>/tmp/payer_runner_bash.lock
python3 -c "import fcntl, sys; fcntl.flock(200, fcntl.LOCK_EX | fcntl.LOCK_NB)" 2>/dev/null || exit 0

# Script to translate multiple languages sequentially with robust retries and fallback
# Dynamic Order: Unfinished languages sorted by highest completion percentage descending
# Strict 100% Completion Loop: Always process top language until 100% clean (0 fallbacks)
# Circuit breaker variables for detecting stuck progress
PREV_LANG=""
PREV_SAUBER=-1
STUCK_COUNT=0
SKIP_LANGS=""

while true; do
    TOP_LANG=$(python3 -c "
import sys; sys.path.insert(0, 'scripts')
from generate_report import get_top_unfinished_language, get_translation_queue, TOTAL_MASTER
skip = '$SKIP_LANGS'.split()
# Find top language not in skip list
top = get_top_unfinished_language()
if top in skip:
    from generate_report import get_next_queued_language
    top = get_next_queued_language(top)
print(top if top else 'ALL_FINISHED')
")

    if [ "$TOP_LANG" = "ALL_FINISHED" ]; then
        if [ -n "$SKIP_LANGS" ]; then
            echo "⚠️ Retrying skipped languages: $SKIP_LANGS"
            SKIP_LANGS=""
            continue
        fi
        echo "🎉 All languages are 100% completed with 0 fallbacks!"
        python3 scripts/send_notification_email.py "Sanskritkurs: ALLE SPRACHEN FERTIG" "Alle Sprachen wurden zu 100% mit 0 Fallbacks fertiggestellt." 2>/dev/null || true
        break
    fi

    # Check progress since last run of same language
    CURR_SAUBER=$(python3 -c "
import sys; sys.path.insert(0, 'scripts')
from generate_report import get_translation_queue, TOTAL_MASTER
print(TOTAL_MASTER - len(get_translation_queue('$TOP_LANG')))
")

    if [ "$TOP_LANG" = "$PREV_LANG" ]; then
        if [ "$CURR_SAUBER" -le "$PREV_SAUBER" ]; then
            STUCK_COUNT=$((STUCK_COUNT + 1))
            echo "⚠️ [CIRCUIT BREAKER] [$TOP_LANG] No progress made ($CURR_SAUBER/136 clean, attempt $STUCK_COUNT/2)."
            if [ "$STUCK_COUNT" -ge 2 ]; then
                echo "🚨 [CIRCUIT BREAKER TRIPPED] [$TOP_LANG] Stuck at $CURR_SAUBER/136 clean. Temporarily skipping to next language..."
                SKIP_LANGS="$SKIP_LANGS $TOP_LANG"
                PREV_LANG=""
                STUCK_COUNT=0
                continue
            fi
        else
            STUCK_COUNT=0
        fi
    else
        PREV_LANG="$TOP_LANG"
        STUCK_COUNT=0
    fi
    PREV_SAUBER=$CURR_SAUBER

    echo "============================================================"
    echo "🎯 TARGET LANGUAGE: [$TOP_LANG] (Clean: $CURR_SAUBER/136)"
    echo "============================================================"

    EXTRA_FLAGS=""

    START_TIME=$(date +%s)
    if python3 scripts/lan_translate.py --lang "$TOP_LANG" $EXTRA_FLAGS; then
        END_TIME=$(date +%s)
        ELAPSED=$((END_TIME - START_TIME))
        ELAPSED_FMT="$(($ELAPSED / 3600))h $((($ELAPSED % 3600) / 60))m $(($ELAPSED % 60))s"
        echo "[$TOP_LANG] ✓ Finished translation run in $ELAPSED_FMT. Re-evaluating status..."

        NEW_QUEUE_LEN=$(python3 -c "
import sys; sys.path.insert(0, 'scripts')
from generate_report import get_translation_queue
print(len(get_translation_queue('$TOP_LANG')))
" 2>/dev/null || echo "1")

        if [ "$NEW_QUEUE_LEN" -eq 0 ]; then
            echo "🎉 [COMPLETED] [$TOP_LANG] is 100% clean (136/136 files)!"
            python3 scripts/send_notification_email.py "Sanskritkurs Fertiggestellt: $TOP_LANG (100% Sauber)" "Die Sprache [$TOP_LANG] wurde erfolgreich zu 100% vollständig und sauber übersetzt (136/136 Dateien, 0 Fallbacks). Dauer des letzten Durchlaufs: $ELAPSED_FMT." 2>/dev/null || true
        fi
    else
        echo "[$TOP_LANG] ⚠️ Error occurred. Retrying [$TOP_LANG] in 10 seconds..."
        sleep 10
    fi
done