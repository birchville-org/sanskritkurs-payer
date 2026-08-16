# Project Design System: The Scholarly Synthesis

> [!IMPORTANT]
> Always adhere to the [Translation & Localization Guide](TRANSLATION_GUIDE.md) when working on non-German content.

## 1. Visual Identity, Color & Typography
- **Mood & Core**: High-end editorial, scholarly, authoritative, minimalist ("The Illuminated Manuscript of the Future").
- **Color Palette**: Primary `#03192e` (Deep Ink), Secondary `#48626e` (Slate Grey), Tertiary `#241500` (Burnt Umber), Parchment `#fcf9f2` (Background), Parchment Dark `#f1eee7` (Surface).
- **Typography**: Serif (*Newsreader*) for body/quotes/headlines; Sans-Serif (*Inter*) for nav/labels/data.
- **Sanskrit Colors**: Red (`⟪...⟫`) and signal red (`sig[...]`) MUST ONLY apply to Devanāgarī text. IAST and Latin letters MUST ALWAYS be black. No italics for Devanāgarī/Sanskrit.

## 2. Layout & Scholarly Image Standard
- **Layout**: 12-column grid, background shifts instead of 1px lines. Absolute lesson numbering (`60.1.`). Main titles strictly `Lektion X` for German master files (`docs/lektionen/*.md`); target locales use localized titles (`# Lesson X`, `# Ders X`, etc.). No redundant TOC overviews.
- **Wortlisten**: Parent entries as unindented running text. Sub-entries inside `::: indent` without bullets (`*` or `-`).
- **Images**: Wrap in `::: media` blocks. Captions strictly 1 line: `(Bildquelle: [Details](/licenses#lektXXXX))` directly under caption.
- **Bibliographic Data**: Move full metadata to `::: deleteme-box` under `### Quellen` at document end AND maintain in `licenses.md`.

## 3. Migration & Build Integrity Rules
- **TOTALBREMSE**: DE Master files (`docs/lektionen/*.md`) and 100% completed languages (**136/136 Sauber, 0 Fallbacks, len(get_translation_queue(lang)) == 0**) are under **absolute write lock**.
- **The Build Gate**: Markdown/layout edits MUST pass `npm run docs:build`. Python scripts MUST be tested via `python3 -m py_compile` without triggering full site builds during active translation runs.
- **Zero-HTML Invariant**: No raw HTML. Use `scripts/purge_html.py` to sanitize.
- **Metadata Invisibility**: `### Quellen` heading MUST be placed strictly inside `::: deleteme-box`.
- **Locale & Layout Sync**: Sync images via `scripts/sync_images.py`. Propagate layout updates via `python3 scripts/sync_layouts.py <lesson>`.
- **Strict Table Integrity**: No parentheses for Devanāgarī in tables. Wrap empty headers in `::: grammar-box` + `::: no-header`. No superfluous Roman transliteration or external translations/genders/cases. No italics inside tables. Multi-line table cell inputs MUST use `:br` on a single markdown line.
- **QA Dropdown Parity**: `#left-lang` and `#right-lang` in `docs/public/qa_viewer.html` must match `config.mjs` locales (enforced by `scripts/pre_push_check.py`).

## 4. Grammar-Box Boundaries
- Mirror original HTML indentation. No blockquotes (`>`) for tables or examples.
- Direct authorial speech stays outside `grammar-box`.
- Examples ("Beispiel:") stay outside `grammar-box` inside `::: indent`.
- Fragmented rules get separate `grammar-box` containers. Nested custom containers increment colon count (`:::: grammar-box`).

## 5. Agent & Execution Rules
- **Verlässliche Berechnungen & Queue-Invariante**: Statusberichte MÜSSEN ausnahmslos via `python3 scripts/generate_report.py` erzeugt werden. Alle Metriken basieren strikt auf der kanonischen Funktion `get_translation_queue` in `scripts/translation_qa.py` (`sauber = 136 - len(todo_queue)`). Eine Datei ist unfertig (in der Queue), wenn sie fehlt, veraltet ist (`mtime < master_mtime`) oder `is_file_fallback` True liefert. Veraltete Dateien dürfen NIEMALS als sauber schönberechnet werden.
- **Autonome Optimierung & Verification Gate**: Der Agent stellt proaktiv sicher, dass alle Steuerdateien, Berichte und Hintergrundprozesse fehlerfrei laufen. Jede Skript-Änderung oder Fehlerbehebung MUSS jedoch zwingend das Verification Gate (`python3 -m py_compile <file>` UND ein realer Testaufruf mit Exit 0) durchlaufen, bevor sie als abgeschlossen gemeldet wird.
- **Ununterbrochene Übersetzung & Priorität**: Übersetzungs-Pipeline läuft ununterbrochen, bis alle Sprachen 100% fertig sind. Priorität hat ausnahmslos die unfertige Sprache mit dem höchsten Prozentsatz. Strikte Vollständigkeit (100% sauber, 0 Fallbacks) vor Sprachenwechsel.
- **Übersetzungs-Strategie (Weg B & Resumption)**: Neue Sprachen werden von Grund auf neu übersetzt (Weg B). Bei einem Systemunterbruch (Reboot, Crash) MUSS die Arbeit jedoch ohne `-f` exakt an der Abbruchstelle fortgesetzt werden, um bereits fertig übersetzte Lektionen nicht zu überschreiben.
- **Kostenbremse & Einzelprozess-Zwang**: Massenübersetzungen laufen 100% kostenlos über `http://nyx.local:8000`. Es darf IMMER NUR EIN EINZIGER Prozess Anfragen an `nyx.local:8000` senden (`ps aux | grep lan_translate`). Sollte ein Chunk/Datei lokal unlösbar sein, wird dies gemeldet — externe API-Fallbacks (Gemini/Sonnet) werden ausschließlich auf expliziten Befehl des Users aktiviert.
- **Single Source of Truth & Modular Hygiene**: Wortlisten, Term-Definitionen, Queue-Logik und QA-Prüfungen dürfen NIEMALS in mehreren Skripten dupliziert werden. Sie MÜSSEN zentral in modularen Bibliotheken (`scripts/translation/terms.py` und `scripts/translation_qa.py`) gebündelt sein. Sämtliche Prüfungen auf Datei- und Übersetzungsstatus (`get_translation_queue`, `is_file_fallback`, `check_has_de_phrases`) greifen auf diese Single Source of Truth zurück.
- **Absolute Non-Destructive QA Invariante**: QA-, Audit- und Report-Skripte sind ausnahmslos rein lesend (Read-Only). Sie dürfen unter keinen Umständen Zieldateien verändern oder `<!-- TODO: Fallback translation -->`-Tags in Dateien schreiben. Dateimodifikationen finden ausschließlich über die Kern-Pipeline (`lan_translate.py`) statt.
- **LLM Server Timeouts**: Bei echten Timeouts/Deadlocks darf `mlx_lm server` über SSH neugestartet werden (Cooldown: 300s).
- **No LaTeX Math Delimiters & No Backslash Commands**: Mathematische Formeln, Pfeile und Berechnungen MÜSSEN IMMER in reinem Unicode/ASCII-Klartext gerendert werden (z.B. `->`, `=>`, `∑`, `√`). NIEMALS LaTeX-Syntax wie `$`, `$$`, `\rightarrow`, `\frac`, `\approx` oder `\(` verwenden, da das Chat-UI kein LaTeX unterstützt und unformatierten Quelltext anzeigt.

## 6. Translation Pipeline Invariants
1. **Chunking**: `MAX_CHUNK` = 1500 Zeichen (Standard, optimal für lokale LLM-Kontexte & Token-Throughput). Trennungen nur VOR Sektionsgrenzen (`## `), Container-Markern (`:::`) oder Tabellenzeilen (`|`).
2. **Single-Pass Frontmatter**: YAML-Frontmatter Übersetzung in genau einem LLM-Aufruf.
3. **Fehler-Isolierung**: `ERROR:` oder API-Fehlermeldungen dürfen NIEMALS in den TM-Cache (`.payer/tm/`) gelangen.
4. **Überschriften-Lokalisierung**: Lektionsüberschriften (`# Урок 1`, `# Lesson 1`, `# Ders 1`) bleiben in Zielsprache.
5. **Prompt-Caching**: Keine dynamischen Runtime-Tokens in System-Prompts.
6. **Container-Sanitisierung**: Nur leere Container & Glossar-Maps bereinigen.
7. **Verbot von TPS-Neustarts**: Server-Neustarts NIEMALS wegen TPS-Werten, sondern NUR bei physischem Verbindungsabbruch.

## 7. Release & Metatext Invariants
- **Rumantsch (rm) Fallback**: Fallback für unübersetzbare Wörter in Rätoromanisch ist Deutsch (DE).
- **Release Workflow**: Auf expliziten Release-Befehl (z.B. "publish release" oder "release vX.Y.Z"): `git commit -m "..."` (mit Versionsnummer und Buildnummer in Klammern z.B. `1.6.1 (596)`), `git tag`, `git push`, `git push --tags` und `gh release create` mit Version und Buildnummer im Titel z.B. `Release v1.6.1 (596)`.
- **Language**: Sämtlicher öffentlicher Metatext (README, Release Notes, Commit-Messages) MUSS auf Englisch verfasst werden.

<!-- GSD Configuration — managed by gsd-core installer -->
# Instructions for GSD

- Use the gsd-core skill when the user asks for GSD or uses a `gsd-*` command.
- Treat `/gsd-...` or `gsd-...` as command invocations and load the matching file from `.github/skills/gsd-*`.
- When a command says to spawn a subagent, prefer a matching custom agent from `.github/agents`.
- Do not apply GSD workflows unless the user explicitly asks for them.
- After completing any `gsd-*` command (or any deliverable it triggers: feature, bug fix, tests, docs, etc.), ALWAYS: (1) offer the user the next step by prompting via `ask_user`; repeat this feedback loop until the user explicitly indicates they are done.
<!-- /GSD Configuration -->
