#!/bin/bash

# Enforce single runner instance using cross-platform Python lock on inherited file descriptor 200
exec 200>/tmp/payer_runner_bash.lock
python3 -c "import fcntl, sys; fcntl.flock(200, fcntl.LOCK_EX | fcntl.LOCK_NB)" 2>/dev/null || exit 0

# Script to translate multiple languages sequentially with robust retries and fallback
# Dynamic Order: Unfinished languages sorted by highest completion percentage descending
# Strict 100% Completion Loop: Always process top language until 100% clean (0 fallbacks)
while true; do
    TOP_LANG=$(python3 -c "
import sys; sys.path.insert(0, 'scripts')
from generate_report import get_top_unfinished_language
print(get_top_unfinished_language())
")

    if [ "$TOP_LANG" = "ALL_FINISHED" ]; then
        echo "🎉 All languages are 100% completed with 0 fallbacks!"
        python3 scripts/send_notification_email.py "Sanskritkurs: ALLE SPRACHEN FERTIG" "Alle Sprachen wurden zu 100% mit 0 Fallbacks fertiggestellt." 2>/dev/null || true
        break
    fi

    echo "============================================================"
    echo "🎯 TARGET LANGUAGE: [$TOP_LANG] (Highest completion %)"
    echo "============================================================"

    if python3 scripts/lan_translate.py --lang "$TOP_LANG" -f; then
        echo "[$TOP_LANG] ✓ Finished translation run. Re-evaluating status..."
    else
        echo "[$TOP_LANG] ⚠️ Error occurred. Retrying [$TOP_LANG] in 10 seconds..."
        sleep 10
    fi
done