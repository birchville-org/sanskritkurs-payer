# Phase 12: I18n Expansion V1.3 — ES, Tamil, Punjabi — Context

**Gathered:** 2026-05-31
**Status:** Ready for planning
**Source:** In-session work — Sprachen wurden bereits in dieser Session hinzugefügt

<domain>
## Phase Boundary

Phase 12 (V1.3) erweitert die bereits bestehende V1.2-Mehrsprachigkeit um drei neue Sprachen:

1. **Spanisch (ES)** — war in V1.2 geplant aber unvollständig (61 Lektionen existieren, fehlend: schrift01-11, uebung01-61, Hauptseiten, wortliste)
2. **Tamil (TA)** — komplett neu, script Dravidian, Tamil-Schrift
3. **Punjabi (PA)** — komplett neu, Gurmukhi-Schrift

Abgrenzung: Keine Änderungen an DE, EN, IT, BG, RU, UK, HI, FR (V1.2-Sprachen).

</domain>

<decisions>
## Implementation Decisions

### Bereits umgesetzte Schritte (diese Session, Commit 7ea0773)
- `docs/.vitepress/locales/pa.mjs` erstellt (Gurmukhi-Locale)
- `docs/.vitepress/config.mjs` aktualisiert: ES, TA, PA aktiviert (Imports, Sidebar, Locales, Search-Filter)
- `docs/ta/` und `docs/pa/` Verzeichnisstrukturen angelegt (inhaltsverzeichnis.md als Stub)
- `scripts/lan_translate.py`: PA hinzugefügt, TA aktiviert (LANGUAGES, LANG_NAMES, LICENSES_LABELS, LICENSES_PHRASES)
- `scripts/gen_wortliste.py`: TA + PA konfiguriert, ACTIVE_LANGS erweitert
- `package.json`: NODE_OPTIONS=--max-old-space-size=8192 für Build-Skript
- Übersetzungs-Jobs gestartet:
  - TA + PA: `python3 -u scripts/lan_translate.py --lang ta,pa` (läuft)
  - ES: `python3 -u scripts/lan_translate.py --lang es` (läuft)

### Technische Entscheidungen
- Übersetzungsmodell: mlx-community/Qwen3.6-35B-A3B-4bit auf nyx.local:8000
- Build benötigt ≥8 GB Node.js Heap (3 neue Sprachen × 135 Seiten = ~400 Seiten mehr)
- Wortliste: nach Übersetzung via `gen_wortliste.py` generieren (kein LLM nötig)
- Build-Gate: `npm run docs:build` muss nach allen Übersetzungen erfolgreich sein

### Sprach-Konfiguration PA (Punjabi)
- Lang-Code: `pa-IN` (Gurmukhi)
- Locale: `docs/.vitepress/locales/pa.mjs` — vollständig konfiguriert
- Sidebar-Labels: ਪਾਠ (Lektion), ਲਿਪੀ (Schrift), ਅਭਿਆਸ (Übung)
- Suche: ਖੋਜ

### Sprach-Konfiguration TA (Tamil)
- Lang-Code: `ta-IN`
- Locale: `docs/.vitepress/locales/ta.mjs` — bereits vorhanden
- Sidebar-Labels: பாடம் (Lektion), எழுத்து (Schrift), பயிற்சி (Übung)
- Suche: தேடு

### Claude's Discretion
- Reihenfolge der Lektionen-Übersetzung: sequenziell (ta zuerst, dann pa)
- Retry-Logik bei Server-Timeouts: bereits in lan_translate.py eingebaut
- Wortlisten-Generierung: erst nach vollständiger Übersetzung via gen_wortliste.py

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Pipeline-Skripte
- `scripts/lan_translate.py` — Hauptübersetzungsskript (LANGUAGES, LANG_NAMES, LICENSES-Konfigurationen)
- `scripts/gen_wortliste.py` — Wortlisten-Generator (LANG_CONFIG, ACTIVE_LANGS)
- `scripts/sync_layouts.py` — Layout-Synchronisation zwischen Sprachen

### VitePress-Konfiguration
- `docs/.vitepress/config.mjs` — Locales, Sidebar-Konfiguration, Search-Filter
- `docs/.vitepress/locales/pa.mjs` — Neue Punjabi-Locale
- `docs/.vitepress/locales/ta.mjs` — Tamil-Locale (bereits vorhanden)
- `docs/.vitepress/locales/es.mjs` — Spanisch-Locale (bereits vorhanden)

### Projektanweisungen
- `CLAUDE.md` — Hard Rules (Build Gate, Zero-HTML, German immutable)
- `AGENTS.md` — Design System, QA-Checklisten

</canonical_refs>

<specifics>
## Specific Ideas

### Ausstehende Übersetzungen (per 2026-05-31)

**Spanisch (ES):**
- ✅ lektion01-61.md (61 Dateien, aus V1.2)
- ✅ inhaltsverzeichnis.md
- ✅ index.md, grammatik.md, impressum.md
- ⏳ schrift01-11.md (11 Dateien — Job läuft)
- ⏳ uebung01-61.md (61 Dateien — Job läuft)
- ⏳ wortliste.md (via gen_wortliste.py nach Übersetzung)
- ⏳ licenses.md (via generate_licenses())

**Tamil (TA):**
- ⏳ lektion01-61.md (61 Dateien — Job läuft)
- ⏳ schrift01-11.md (11 Dateien)
- ⏳ uebung01-61.md (61 Dateien)
- ⏳ index.md, grammatik.md, impressum.md, themen.md
- ⏳ inhaltsverzeichnis.md (Stub vorhanden)
- ⏳ wortliste.md (via gen_wortliste.py)
- ⏳ licenses.md (via generate_licenses())

**Punjabi (PA):**
- ⏳ lektion01-61.md (61 Dateien — Job läuft nach TA)
- ⏳ schrift01-11.md (11 Dateien)
- ⏳ uebung01-61.md (61 Dateien)
- ⏳ index.md, grammatik.md, impressum.md, themen.md
- ⏳ inhaltsverzeichnis.md (Stub vorhanden)
- ⏳ wortliste.md (via gen_wortliste.py)
- ⏳ licenses.md (via generate_licenses())

</specifics>

<deferred>
## Deferred Ideas

- Lateinisch (LA), Rätoromanisch (RM): für später (Phase 16 oder weiter)
- ES: Schriften-Übungen (schrift-) inhaltlich prüfen (maschinell übersetzt, evtl. manuelle QA nötig)
- TA/PA: Grammatik-Index (grammatik.md) — maschinelle Übersetzung, Qualität muss nach Abschluss geprüft werden

</deferred>

---

*Phase: 12-automated-internationalization-it-es*
*Kontext gesammelt: 2026-05-31 — in-session nach direkter Implementierung*
