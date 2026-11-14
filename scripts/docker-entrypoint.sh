#!/bin/sh
set -e

if [ -n "${GITHUB_TOKEN:-}" ]; then
  echo "[entrypoint] GITHUB_TOKEN detected — starting QA Auth Broker on 127.0.0.1:8081"
  python3 /usr/local/bin/qa_auth_broker.py &
else
  echo "[entrypoint] No GITHUB_TOKEN set — running static nginx only"
fi

exec nginx -g "daemon off;"
