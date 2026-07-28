# Project Design System: The Scholarly Synthesis

> [!IMPORTANT]
> Always adhere to the [Translation & Localization Guide](file:///Volumes/SanDisk1TB/proj/Payer/TRANSLATION_GUIDE.md) when working on non-German content.

## 1. Visual Identity & Mood
- **Mood**: High-end editorial, scholarly, authoritative, and minimalist.
- **Core Principle**: "The Illuminated Manuscript of the Future."
- **Whitespace**: Treat whitespace as a luxury material.

## 2. Color Palette
- **Primary**: `#03192e` (Deep Ink)
- **Secondary**: `#48626e` (Slate Grey)
- **Tertiary**: `#241500` (Burnt Umber)
- **Parchment**: `#fcf9f2` (Background)
- **Parchment Dark**: `#f1eee7` (Surface)

## 3. Typography
- **Serif (Newsreader)**: Body text, quotes, headlines.
- **Sans-Serif (Inter)**: Navigation, labels, technical data.
- **Hierarchy**: Large sans-serif headlines paired with italic serif subheaders.
- **Sanskrit Colors**: The colors red (`⟪...⟫`) and signal red (`sig[...]`) MUST ONLY be applied to Devanāgarī text. IAST (Latin transliteration) and standard Latin letters MUST ALWAYS be black (unformatted).

## 4. Layout Patterns
- **Grid**: 12-column grid, intentional asymmetry.
- **No Borders**: Use background color shifts (e.g., `bg-parchment` to `bg-parchment-dark`) instead of 1px lines.
- **Header Numbering**: Always use absolute lesson-prefixed numbering (e.g., `60.1.`) for digital consistency.
- **Main Lesson Titles**: The main title (Frontmatter `title` and `#` H1) must be strictly `Lektion X` (e.g., `# Lektion 41`), matching the sidebar navigation. Avoid redundant prefixes like `# 41. Lektion 41`.
- **No Redundant Overviews**: Omit static "Übersicht" (TOC) sections at the start of lessons; the VitePress sidebar provides this functionality.
- **Wortlisten Layout (Vocabulary Lists)**:
  - Parent/main vocabulary entries MUST be formatted as standard unindented paragraphs (no `::: indent` wrapper).
  - All sub-entries, derivations, and indented items (originally in `<blockquote>` in Payer's HTML) MUST be enclosed inside a `::: indent` container but must contain **no bullets** (`*` or `-`). They should be rendered cleanly as standard running text paragraphs.
## 5. Scholarly Image Standard (L16-Ref)
- **Container**: Always wrap images in `::: media` blocks.
- **Captions**:
  - Format exactly on one line, without line breaks.
  - Explanatory text, titles, and translations of the Devanāgarī label are explicitly desired and should be kept within the markdown caption (they will be translated). Do NOT strip them out.
  - Compact attribution: `(Bildquelle: [Details](/licenses#lektXXXX))` directly under the caption (replace XXXX with image ID).
- **Metadata**:
  - Full bibliographic data (URL, License, Access date) MUST be moved to a `::: deleteme-box` at the END of the document under `### Quellen` AS WELL AS maintained in `licenses.md`.
  - No raw metadata blocks are allowed directly under images.

## 6. Migration & Build Integrity Rules
- **TOTALBREMSE (DE Source Integrity Invariant)**: Schreibzugriff auf die DE Masterfiles (`docs/lektionen/*.md`) sind nur mit ausdrücklicher Genehmigung erlaubt. Das gilt auch für Skripten und Programme. Jeder Agent muss vor einer geplanten Änderung an diesen Dateien stoppen, den Plan präsentieren und die Erlaubnis einholen. All translations must branch from this protected master without touching it.
- **The Build Gate**: Every session MUST conclude with a successful `npm run docs:build`. A task is only "Done" if the build passes.
- **Zero-HTML Invariant**: No raw HTML (tables, br, div, etc.) in Markdown. Use `scripts/purge_html.py` to sanitize content.
- **Metadata Invisibility**: All scholarly metadata (citations, copyright) must be wrapped in `::: deleteme-box` containers.
- **Locale Sync**: Image links in translations must match the root German files. Use `scripts/sync_images.py` to ensure consistency.
- **Multi-Language Layout Synchronization**: To propagate layout, table, header, and container updates from German master files to translated target language files without invoking the LLM, run `python3 scripts/sync_layouts.py <lesson_number>` (or `all`).
- **No Parentheses for Devanāgarī in Tables**: Never enclose Devanāgarī script in round parentheses `()` inside tables. Instead, write them cleanly (e.g. `**dveṣṭi**:brद्वेष्टि` instead of `**dveṣṭi**:br(द्वेष्टि)`).
- **Table Empty Headers**: If a table has an empty first row `| | | |` (due to having no header in the original HTML layout), wrap the table inside the `::: grammar-box` in a `::: no-header` container so the empty table header is completely hidden from the user.
- **No Superfluous Roman Transliteration in Tables**: Do not add redundant IAST/Roman bold transliterations (e.g. `**yajan**`) at the beginning of table cells if Payer only wrote Devanagari in the original HTML table cells. Keep only the exact original text structure.
- **Strict Table Cell Content Parity**: Never add external, logically assumed, or standardized translations, grammatical labels, genders (e.g., `m.`, `f.`, `n.`, `maskulinum`), case indices (e.g., `1. Nominativ / प्रथमा` if the original had only `प्रथमा`), or transliterations to any table cell unless they were explicitly written in that specific table's cell or header in Payer's original HTML. The exact historical text structure of Payer's tables takes absolute priority over logical enhancements.
- **No Italics inside Tables**: Do not italicize parenthetical comments or grammatical/morphological explanation text inside table cells (e.g. write `(aus yaja-nt-s)` instead of `*(aus yaja-nt-s)*`).
- **Devanāgarī Over Pure IAST in Tables**: For cross-references to other paradigms inside table cells (like `wie devī`), always include the Devanāgarī form alongside it (`wie **devī**:brदेवी`) rather than presenting Roman script in isolation.
- **Absolute Table Integrity**: Never tear, split, or corrupt table lines during markdown editing or migration. Multi-line table cell inputs MUST use clean markdown syntax with `:br` for line breaks, ensuring that every table row remains exactly on a single markdown line `| cell1 | cell2 | ... |`.
- **No Manual Port/Nav**: Use default port 5173. Use `PayerDocFooter.vue` for navigation; no manual links in content.
- **QA Viewer Dropdown Parity**: The dropdown menus (`#left-lang` and `#right-lang`) in `docs/public/qa_viewer.html` MUST ALWAYS contain exactly the same languages. Furthermore, they must strictly reflect ONLY the actively configured languages in `docs/.vitepress/config.mjs` (in the `allLocales` array). This is automatically enforced by `scripts/pre_push_check.py`.

## 7. Final QA Checklist (Schlussüberprüfung)
Before concluding a lesson migration, verify:
- **Image Captions**: Are all image captions strictly one line? Do they contain the desired explanatory text without being overly stripped?
- **License Integrity**: Have all raw bibliographic data been safely appended to the `licenses.md` file and removed from the main lesson view?
- **Grammar Boxes**: Are all pedagogical rules enclosed in `::: grammar-box` without internal tables using the `no-header` class improperly?
- **Zero-HTML**: Are all blockquotes rendered purely with `>` and properly formatted without legacy HTML tags?
- **Broken Table Audit**: Are all legacy/broken table residues (like empty cells `|`, dashed lines `| --- |`, or orphaned separators) completely purged from the markdown? Complex layout boxes must be converted into a unified `:::: grammar-box` containing clean Markdown blocks.
- **Header Invisibility**: Is the `### Quellen` heading itself placed strictly **inside** the `::: deleteme-box` container (e.g. `::: deleteme-box \n ### Quellen`), ensuring that no stray metadata headings are visible in the frontend?
- **Taxonomy Bolding**: Are list elements representing primary grammatical taxonomies or structural options inside a `grammar-box` fully bolded (e.g. `* **attributiv**`) to capture Payer's original typographical emphasis?

## 8. Grammar-Box Boundaries (Structural Parity)
- **Strict Visual Mapping**: The `::: grammar-box` must strictly mirror the *indentation* in Payer's original HTML. Do not group elements logically into a single box if they were separated by unindented text in the original.
- **No Blockquotes for Tables**: Never wrap paradigm or grammatical tables in standard markdown blockquotes (`>`). They must be placed directly inside a `::: grammar-box` (or `::: no-header` nested inside a `::: grammar-box`) without any `>` prefix.
- **Authorial Asides**: Direct speech from the author to the student (e.g., "Jetzt erkennen Sie den Grund...", "Beachten Sie:") is almost always unindented in the original and MUST remain **outside** the `grammar-box`.
- **Headings & Introductions**: Introductory phrases (e.g., "Frage-, Relativ- und Demonstrativpronomina:", "1. Relativsätze") must be outside the box unless they were explicitly indented in the original.
- **Examples**: The headings "Beispiel:" / "Beispiele:" and the examples that follow them MUST ALWAYS be placed **outside** any `grammar-box` and wrapped in a `::: indent` container. Do not use standard markdown blockquotes (`>`) for examples, as VitePress styles them with borders and backgrounds that look like boxes.
- **Fragmented Elements**: If a rule, a paradigm, and a table are separated by unindented text, they each get their **own separate** `grammar-box`. Do not merge them.
- **Nested Container Colons**: If a `grammar-box` container contains nested custom containers (such as `::: indent`), the outer container **MUST** use exactly **four colons** (`:::: grammar-box` and `::::`) instead of three to prevent parsing conflicts. If there is an even deeper level of nesting, increment the colon count by one for each level.

## 9. Session Cache Optimization (Agent Rules)

These rules preserve OpenRouter prompt-cache hits. The agent MUST follow them; they are not negotiable.

- **Skill Preloading**: Do NOT load skills mid-session with `skill_view()` unless absolutely unavoidable. Instead, identify needed skills at session start and the user will launch with `hermes -s <skills>`. If a skill becomes needed mid-session, batch multiple `skill_view()` calls into a single turn to minimize cache-breaking prefix changes. Prefer loading the skill's content via `read_file` on `SKILL.md` if only a specific section is needed.

- **Memory Writes**: Do NOT call `memory()` during an active session. Accumulate all new facts, preferences, and corrections mentally. Write them in a single batch at session end or immediately at the start of the next session. Mid-session memory writes change the injected MEMORY block → OpenRouter cache miss on the next turn.

- **Toolset Stability**: Do not enable/disable toolsets mid-session. Hermes already enforces this (changes only apply on `/reset`), but the agent must not suggest or attempt it.

- **AGENTS.md Stability**: Do not edit this file mid-session except for explicit, user-requested rule changes. Routine edits break the project context prefix and cause cache misses.

- **Session Duration**: For complex multi-step tasks (lesson migrations, code reviews), prefer longer focused sessions over many short ones. The system message cache persists across turns; each new session pays the full cache-fill cost.

- **LLM Server Timeouts**: Bei LLM-Timeouts (oder offensichtlichen Deadlocks) auf dem exklusiven Server `nyx.local` darf der Agent immer sofort und ohne Rückfrage eingreifen und den `mlx_lm server` über SSH neustarten.

- **Ununterbrochene Übersetzung**: Die Übersetzungs-Pipeline darf niemals gestoppt werden oder vorzeitig aufhören, bis alle Sprachen im Kurs vollständig übersetzt sind.

- **Strikte Kostenbremse für Cloud-APIs (OpenRouter / Externe APIs)**: Es ist dem Agenten und allen Skripten strengstens verboten, kostenpflichtige Cloud-APIs (wie OpenRouter, Gemini Pro, Claude) als primären Verarbeitungs- oder Übersetzungsmotor einzusetzen oder in Shell-Befehlen explizit zu erzwingen (`--api openrouter.ai`). Alle Massen- und Erstübersetzungen MÜSSEN ausnahmslos über den kostenlosen lokalen Server (`http://nyx.local:8000`) gestartet werden. Cloud-APIs dürfen ausschließlich als automatische Fallback-Ebene für vereinzelte Qualitätskorrekturen verwendet werden.

- **Standardisiertes Statusreport-Format**: Bei allen Übersetzungsberichten oder Cronjobs MUSS der Agent ausnahmslos `python3 scripts/generate_report.py` ausführen. Das Format ist strikt vorgegeben (137-Dateien-Masterbasis, aktive Prozess-PID + CPU-Time, aktive Datei + Chunk-Fortschritt z.B. `Sektion X von Y Chunks`, Anzahl Fallbacks in eigener Spalte, und Sortierung der unfertigen Sprachen streng nach der höchsten Prozentzahl absteigend).

- **Strikter Einzelprozess-Zwang für nyx.local:8000 (Absolutes Verbot von Parallelläufen)**: Es darf im gesamten System ausnahmslos IMMER NUR EIN EINZIGER Prozess gleichzeitig existieren, der Anfragen an http://nyx.local:8000 sendet. Bevor der Agent ein neues Skript oder einen Befehl startet, MUSS er mit `ps aux | grep lan_translate` prüfen, ob bereits ein Prozess läuft. Zudem erzwingt `lan_translate.py` diesen Einzelprozess-Schutz hardwarenah über `fcntl.flock` auf `/tmp/payer_translation_nyx.lock`. Jeder Versuch, einen zweiten Prozess zu starten, wird auf Betriebssystemebene sofort abgewiesen.

- **Strikte Vollständigkeit pro Sprache**: Eine Sprache muss ausnahmslos zu 100% fertig übersetzt und frei von Fallbacks (0 Fallbacks) sein, bevor mit der nächsten Sprache begonnen wird.