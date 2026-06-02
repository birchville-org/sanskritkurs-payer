---
plan: 12-2
status: complete
completed: 2026-06-01
key-files:
  created:
    - docs/es/lektionen/wortliste.md
    - docs/ta/lektionen/wortliste.md
    - docs/pa/lektionen/wortliste.md
    - docs/ta/licenses.md
    - docs/pa/licenses.md
  modified:
    - scripts/sync_wortliste.py
---

## Wortlisten und Lizenz-Seiten ES/TA/PA

Alle Wortlisten und Lizenz-Seiten wurden generiert:

- **ES**: wortliste.md (aus übersetzten Lektionen zusammengestellt)
- **TA**: wortliste.md + licenses.md ✅
- **PA**: wortliste.md + licenses.md ✅

`sync_wortliste.py` wurde um `--lang LANG`-Parameter erweitert — generiert sprachspezifische Wortlisten aus bereits übersetzten Lektionsdateien ohne KI-Aufruf.

## Self-Check: PASSED
