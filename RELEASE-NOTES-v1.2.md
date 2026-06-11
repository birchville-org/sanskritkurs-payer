# Release Notes — v1.2 «Search, Index & I18n Expansion»

**Veröffentlicht:** 2026-05-xx  
**Vorherige Version:** v1.1 (2026-04-19)  
**Phasen:** 10–14

---

## Suche & Infrastruktur (Phase 10)

**IAST-Suche mit Diakritikafolding**  
Die integrierte VitePress-Suche (MiniSearch) erkennt nun IAST-Transliterationen auch ohne diakritische Zeichen. Eine Suche nach `samskrta` findet `Saṃskṛta`, `deva` findet `devā` usw. Devanāgarī-Zeichen bleiben von der Normalisierung unberührt.

**Modulare VitePress-Konfiguration**  
`config.mjs` wurde in sprachspezifische Dateien unter `docs/.vitepress/locales/` aufgeteilt (`de.mjs`, `en.mjs`, `it.mjs`, `es.mjs`, `bg.mjs`, `ru.mjs`, `uk.mjs`). Die Konfiguration ist damit wartbar und skalierbar für weitere Sprachen.

---

## Thematischer Index & Related Lessons (Phase 11)

**Automatischer Themen-Index**  
Ein neuer VitePress Data Loader (`topics.data.mjs`) extrahiert zur Build-Zeit alle Grammatik- und Themenüberschriften aus den 61 Lektionen. Die Seite `/themen` listet alle Themen alphabetisch mit Links zu den entsprechenden Lektionen.

**«Verwandte Lektionen»-Komponente**  
Am Ende jeder Lektion erscheint die neue `PayerRelatedLessons`-Komponente mit bis zu 3 thematisch verwandten Lektionen. Die Komponente folgt dem «Scholarly Synthesis»-Designsystem (Newsreader, Pergament-Hintergrund).

---

## Sechssprachige Erweiterung (Phase 12)

**Neu: Ukrainisch und Russisch**  
Zu den bestehenden Sprachen Englisch, Italienisch, Spanisch und Bulgarisch kommen Ukrainisch (`/uk/`) und Russisch (`/ru/`) hinzu. Alle 61 Lektionen sind nun in 6 Übersetzungssprachen plus Deutsch verfügbar.

**Sprachauswahl auf der Homepage**  
Die Startseite bietet alle 7 Sprachversionen direkt zur Auswahl an.

---

## QA-Viewer-Integration (Phase 13)

**Neue Route `/qa/viewer`**  
Der QA-Viewer ist jetzt als vollwertiger VitePress-Inhalt unter `/qa/viewer` erreichbar (bisherige Standalone-HTML-Datei entfernt). Navigations-404-Fehler sind damit behoben.

**Pro-Sync-Scrolling**  
Bidirektionales, prozentbasiertes Scroll-Sync zwischen Markdown-Quellpane und gerendertem HTML: Beide Panes bleiben positionssynchron.

**Visuelle Parität mit dem Designsystem**  
Der Viewer verwendet nun dieselben Schriften (Source Serif 4, Inter) und Farben wie die übrigen Seiten des Kurses.

---

## Quelltreue & Inhaltsqualität (Phase 14 + laufend)

**Fidelity-Audit aller 61 Lektionen**  
Systematische Überarbeitung aller Lektionen auf 1:1-Quelltreue gegenüber dem Original-HTML von Alois Payer:

- Paradigmentabellen mit korrekten Zeilen- und Spalten-Spannungen (`||`, `^^`), insbesondere für die komplexen Deklinations- und Konjugationstabellen in L27, L39, L40 und L61
- Alle `<br>` und Raw-HTML entfernt (`purge_html.py`); Zero-HTML in allen Dateien
- Bildunterschriften vereinheitlicht: einzeilig, reines Devanāgarī, `(Bildquelle: [Details](/licenses#...))` für alle Bilder
- Grammatik-Box-Hierarchie bereinigt: `:::: grammar-box` nur bei tatsächlich verschachtelten Containern, sonst `:::`. Alle `::: center`-Trümmer um Bilder entfernt, `::: indent` für `<blockquote>`-Inhalte eingesetzt
- Wortlisten-Formatierung vereinheitlicht: `-` statt `*`, Devanāgarī ohne Klammern, blockquotierte Einträge in `::: indent`

**Übersetzungspipeline verbessert**  
- IAST-Schutz: Zeilen mit reinen IAST-Transliterationen werden vor dem LLM mit `⟨IAST_L_N⟩`-Platzhaltern geschützt und nach der Übersetzung exakt wiederhergestellt
- Devanāgarī-Schutz mit Post-Translation-Warnung bei verlorenen Platzhaltern
- Inkrementelle Übersetzung basierend auf `mtime` (nur geänderte Dateien werden neu übersetzt)
- `wortliste.md`, `inhaltsverzeichnis.md` und `lektionen/index.md` werden nun ebenfalls in alle 6 Zielsprachen übersetzt
- Timeout auf 600 s erhöht für vollständige Generierung mit dem 35B-Modell

**Devanāgarī immer rot**  
CSS-Regel kodifiziert: Alle `.sanskrit-dev`-Spans erscheinen in `#ff0000`, auch in Tabellen und Grammar-Boxes. Eine überschreibende `color: inherit`-Regel in Grammar-Box-Tabellen wurde entfernt und die Regel explizit in `CLAUDE.md` verankert.

---

## Bruch mit v1.1

- Die Standalone-Datei `docs/public/qa/viewer.html` wurde entfernt; bestehende Bookmarks müssen auf die neue VitePress-Route `/qa/viewer` zeigen — die URL bleibt gleich, die Implementierung wechselt.
- Die monolithische `config.mjs` wurde in Locale-Dateien aufgeteilt; direkte Importe von `config.mjs`-Interna müssen über die neuen `locales/*.mjs` erfolgen.
