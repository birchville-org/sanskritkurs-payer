#!/bin/bash
#set -x
set -euo pipefail

# Find the directory of this script to locate the venv
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" &> /dev/null && pwd)"
cd "$SCRIPT_DIR/.."

if [ -f "./venv/bin/activate" ]; then
    source ./venv/bin/activate
elif [ -f "../venv/bin/activate" ]; then
    source ../venv/bin/activate
fi

# 1. Alte hängende MLX-Server Prozesse sicher beenden, bevor wir Port 8000 neu binden
pkill -f "python -m mlx_lm" || true
sleep 2

export MX_DISABLE_CACHE=1
export MLX_DEBUG_MEMORY=1

nohup python -m mlx_lm server \
  --model mlx-community/Qwen3.6-35B-A3B-4bit \
  --host 0.0.0.0 \
  --port 8000 \
  --chat-template-args '{"enable_thinking":false}' \
  --temp 0.3 \
  --max-tokens 16384 \
  --max-prefill-tokens 8192 \
  --max-batch-tokens 32768 \
  --trust-remote-code \
  > /tmp/mlx_server.log 2>&1 &

echo "MLX Server gestartet."
