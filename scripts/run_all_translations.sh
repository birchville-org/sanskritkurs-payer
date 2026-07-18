#!/bin/bash
set -e

# Translates the languages sequentially to avoid overloading the nyx.local API
# Order: fi, hu, th, el, cop, grc, fa, nl, af, lt, sh, sq, akk, am, gez

echo "Starting massive language expansion..."

python3 scripts/lan_translate.py --lang fi all
python3 scripts/lan_translate.py --lang hu all
python3 scripts/lan_translate.py --lang th all
python3 scripts/lan_translate.py --lang el all
python3 scripts/lan_translate.py --lang cop all
python3 scripts/lan_translate.py --lang grc all
python3 scripts/lan_translate.py --lang fa all
python3 scripts/lan_translate.py --lang nl all
python3 scripts/lan_translate.py --lang af all
python3 scripts/lan_translate.py --lang lt all
python3 scripts/lan_translate.py --lang sh all
python3 scripts/lan_translate.py --lang sq all
python3 scripts/lan_translate.py --lang akk all
python3 scripts/lan_translate.py --lang am all
python3 scripts/lan_translate.py --lang gez all

echo "All languages completed!"