#!/bin/bash

# Translates the 11 new languages sequentially to avoid overloading the nyx.local API
# Order: th, el, cop, grc, fa, nl, af, lt, sh, sq, akk

echo "Starting massive language expansion (11 languages)..."

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

echo "All 11 languages completed!"
\npython3 scripts/lan_translate.py --lang am all\npython3 scripts/lan_translate.py --lang gez all\n