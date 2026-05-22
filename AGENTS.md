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
  - Format exactly on one line, without line breaks (e.g., `Abb.: ऊहापोहः`).
  - Primary label in pure Devanāgarī (if applicable). All German translations or descriptions must be stripped from the visible markdown caption.
  - Compact attribution: `(Bildquelle: [Details](/licenses#lektXXXX))` directly under the caption (replace XXXX with image ID).
- **Metadata**:
  - Removed German translations/descriptions from captions MUST be preserved and copied to the corresponding image entry in `licenses.md`.
  - Full bibliographic data (URL, License, Access date) MUST be moved to a `::: deleteme-box` at the END of the document under `### Quellen` AS WELL AS maintained in `licenses.md`.
  - No raw metadata blocks are allowed directly under images.

## 6. Migration & Build Integrity Rules
- **The Build Gate**: Every session MUST conclude with a successful `npm run docs:build`. A task is only "Done" if the build passes.
- **Zero-HTML Invariant**: No raw HTML (tables, br, div, etc.) in Markdown. Use `scripts/purge_html.py` to sanitize content.
- **Metadata Invisibility**: All scholarly metadata (citations, copyright) must be wrapped in `::: deleteme-box` containers.
- **Locale Sync**: Image links in translations must match the root German files. Use `scripts/sync_images.py` to ensure consistency.
- **Multi-Language Layout Synchronization**: To propagate layout, table, header, and container updates from German master files to translated target language files without invoking the LLM, run `python3 scripts/sync_layouts.py <lesson_number>` (or `all`).
- **No Parentheses for Devanāgarī in Tables**: Never enclose Devanāgarī script in round parentheses `()` inside tables. Instead, write them cleanly (e.g. `**dveṣṭi**[[br]]द्वेष्टि` instead of `**dveṣṭi**[[br]](द्वेष्टि)`).
- **Table Empty Headers**: If a table has an empty first row `| | | |` (due to having no header in the original HTML layout), wrap the table inside the `::: grammar-box` in a `::: no-header` container so the empty table header is completely hidden from the user.
- **No Superfluous Roman Transliteration in Tables**: Do not add redundant IAST/Roman bold transliterations (e.g. `**yajan**`) at the beginning of table cells if Payer only wrote Devanagari in the original HTML table cells. Keep only the exact original text structure.
- **Strict Table Cell Content Parity**: Never add external, logically assumed, or standardized translations, grammatical labels, genders (e.g., `m.`, `f.`, `n.`, `maskulinum`), case indices (e.g., `1. Nominativ / प्रथमा` if the original had only `प्रथमा`), or transliterations to any table cell unless they were explicitly written in that specific table's cell or header in Payer's original HTML. The exact historical text structure of Payer's tables takes absolute priority over logical enhancements.
- **No Italics inside Tables**: Do not italicize parenthetical comments or grammatical/morphological explanation text inside table cells (e.g. write `(aus yaja-nt-s)` instead of `*(aus yaja-nt-s)*`).
- **Devanāgarī Over Pure IAST in Tables**: For cross-references to other paradigms inside table cells (like `wie devī`), always include the Devanāgarī form alongside it (`wie **devī**[[br]]देवी`) rather than presenting Roman script in isolation.
- **Absolute Table Integrity**: Never tear, split, or corrupt table lines during markdown editing or migration. Multi-line table cell inputs MUST use clean markdown syntax with `[[br]]` for line breaks, ensuring that every table row remains exactly on a single markdown line `| cell1 | cell2 | ... |`.
- **No Manual Port/Nav**: Use default port 5173. Use `PayerDocFooter.vue` for navigation; no manual links in content.

## 7. Final QA Checklist (Schlussüberprüfung)
Before concluding a lesson migration, verify:
- **Image Captions**: Are all image captions strictly one line, using pure Devanāgarī? (e.g. `Abb.: ऊहापोहः`)
- **License Integrity**: Have all image descriptions and accompanying text (German or English) that were stripped from the markdown been safely appended to the `licenses.md` file?
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