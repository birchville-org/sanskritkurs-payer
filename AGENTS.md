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
- **Zero-HTML Invariant**: No raw HTML (tables, br, div, etc.) in Markdown. Use `scratch/purge_html.py` to sanitize content.
- **Metadata Invisibility**: All scholarly metadata (citations, copyright) must be wrapped in `::: deleteme-box` containers.
- **Locale Sync**: Image links in translations must match the root German files. Use `scratch/sync_images.py` to ensure consistency.
- **No Manual Port/Nav**: Use default port 5173. Use `PayerDocFooter.vue` for navigation; no manual links in content.

## 7. Final QA Checklist (Schlussüberprüfung)
Before concluding a lesson migration, verify:
- **Image Captions**: Are all image captions strictly one line, using pure Devanagari? (e.g. `Abb.: ऊहापोहः`)
- **License Integrity**: Have all image descriptions and accompanying text (German or English) that were stripped from the markdown been safely appended to the `licenses.md` file?
- **Grammar Boxes**: Are all pedagogical rules enclosed in `::: grammar-box` without internal tables using the `no-header` class improperly?
- **Zero-HTML**: Are all blockquotes rendered purely with `>` and properly formatted without legacy HTML tags?

## 8. Grammar-Box Boundaries (Structural Parity)
- **Strict Visual Mapping**: The `::: grammar-box` must strictly mirror the *indentation* in Payer's original HTML. Do not group elements logically into a single box if they were separated by unindented text in the original.
- **Authorial Asides**: Direct speech from the author to the student (e.g., "Jetzt erkennen Sie den Grund...", "Beachten Sie:") is almost always unindented in the original and MUST remain **outside** the `grammar-box`.
- **Headings & Introductions**: Introductory phrases (e.g., "Frage-, Relativ- und Demonstrativpronomina:", "1. Relativsätze") must be outside the box unless they were explicitly indented in the original.
- **Examples**: The headings "Beispiel:" / "Beispiele:" and the blockquoted examples that follow them MUST ALWAYS be included **inside** the `grammar-box` of the grammatical rule they illustrate. Never close a box before its examples.
- **Fragmented Elements**: If a rule, a paradigm, and a table are separated by unindented text, they each get their **own separate** `grammar-box`. Do not merge them.