#!/usr/bin/env bash
# ─────────────────────────────────────────────────────────────────────
# cleanup.sh — Einmaliges Aufräum-Script für sanskritkurs-payer
#
# Anleitung:
#   1. Script durchlesen und ggf. Blöcke auskommentieren
#   2. chmod +x cleanup.sh && ./cleanup.sh
#   3. Ergebnis prüfen: git status / git diff --cached
#   4. Commit: git commit -m "chore: remove stale artifacts, logs, and test files"
#   5. Dieses Script danach löschen: git rm cleanup.sh && git commit --amend --no-edit
# ─────────────────────────────────────────────────────────────────────
set -euo pipefail

echo "=== Block 1/5: .gitignore ergänzen ==="
# Neue Einträge für Dateien, die bisher noch nicht ignoriert werden
cat >> .gitignore << 'GITIGNORE'

# ── Aufräumung Juni 2025 ──────────────────────────────────────
# Build / CI Artefakte
audit_results.txt
/lighthouse-*
build_log.txt

# Einmalige Root-Artefakte
index.html
wortliste_prev.md
update_settings.py
external.yml

# Test-Dateien in docs/
docs/test*.md
docs/test*.mjs
docs/testfile.md
docs/grid-test.md
docs/sanskrit-grid-test.md

# Einmalige Fix-Scripts (bereits abgearbeitet)
scripts/fix_gramboxes_*.py
scripts/fix_signalrot.py
scripts/fix_syntax.py
scripts/start_mlx_server.sh
scripts/lektion02_test.md

# Komplettes Archiv (History bleibt in Git)
archive/
GITIGNORE
echo "   .gitignore aktualisiert"


echo ""
echo "=== Block 2/5: Bereits in .gitignore, aber noch im Index (168 Dateien) ==="
# Diese Dateien bleiben auf deiner Platte, werden aber aus Git entfernt.
# Betrifft: scratch/, __pycache__/, *.log in archive/, etc.
git ls-files --cached --ignored --exclude-standard -z | xargs -0 git rm --cached --quiet 2>/dev/null || true
echo "   Getrackt-aber-ignorierte Dateien aus dem Index entfernt"


echo ""
echo "=== Block 3/5: Log- und Build-Artefakte im Root ==="
git rm -f --quiet \
  build.log \
  build_after_17.log \
  build_final_53.log \
  build_log.txt \
  build_no_multiline.log \
  server.log \
  audit_results.txt \
  2>/dev/null || true
echo "   Logs und Build-Artefakte entfernt"


echo ""
echo "=== Block 4/5: Überflüssige Einzeldateien ==="
git rm -f --quiet \
  lighthouse-de-new.report.html \
  lighthouse-de-new.report.json \
  lighthouse-de.html \
  index.html \
  wortliste_prev.md \
  update_settings.py \
  external.yml \
  2>/dev/null || true

# Test-Dateien in docs/
git rm -f --quiet \
  docs/test.md \
  docs/test_part.md \
  docs/test_table.md \
  docs/testfile.md \
  docs/grid-test.md \
  docs/sanskrit-grid-test.md \
  docs/test-box-table.md \
  docs/test-def-list.md \
  docs/test-colspan-header.mjs \
  docs/test-grid.mjs \
  docs/test-header-merge.mjs \
  docs/test-multiline-cell-spaces.mjs \
  docs/test-multiline-cell.mjs \
  docs/test-multiline-indent-v2.mjs \
  docs/test-multiline-indent.mjs \
  docs/test-multimd-backslash.mjs \
  docs/test-multimd-real-multiline.mjs \
  docs/test-no-header.mjs \
  docs/test-unicode-break.mjs \
  2>/dev/null || true

# Einmalige Fix-Scripts in scripts/
git rm -f --quiet \
  scripts/fix_gramboxes_59_60.py \
  scripts/fix_gramboxes_60_patch.py \
  scripts/fix_gramboxes_61.py \
  scripts/fix_signalrot.py \
  scripts/fix_syntax.py \
  scripts/start_mlx_server.sh \
  scripts/lektion02_test.md \
  2>/dev/null || true
echo "   Einzeldateien entfernt"


echo ""
echo "=== Block 5/5: archive/ komplett entfernen ==="
# Die History bleibt in Git erhalten — bei Bedarf jederzeit wiederherstellbar.
git rm -rf --quiet archive/ 2>/dev/null || true
echo "   archive/ entfernt"


echo ""
echo "══════════════════════════════════════════════════════════════"
echo "  Fertig. Nächste Schritte:"
echo ""
echo "  1. Prüfen:  git status"
echo "  2. Commit:  git commit -m 'chore: remove stale artifacts, logs, and test files'"
echo "  3. Push:    git push"
echo ""
echo "  Dieses Script danach entfernen:"
echo "    git rm cleanup.sh && git commit --amend --no-edit"
echo "══════════════════════════════════════════════════════════════"
