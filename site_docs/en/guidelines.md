# 📐 Developer & Author Guidelines

## 1. Typography, Layout & Color Palette

The visual design of the Sanskrit course reflects traditional philological editions coupled with modern web standards:

- **Typography:**
  - Body Text: `Newsreader` (serif font engineered for extended reading of complex grammar treatises).
  - UI & Navigation: `Inter` (clean, contemporary sans-serif typeface).
- **Color Palette:**
  - Primary: `#03192e` (Deep Navy Blue).
  - Background: `#fcf9f2` (Warm Ivory Paper).
  - Signal Red: `:sig[...]` (Exclusively reserved for highlighting inflectional morphemes in Devanāgarī).
- **Layout:**
  - 12-column responsive layout grid.
  - Absolute lesson numbering (e.g., `60.1.`).
  - Strict prohibition of raw HTML elements in Markdown sources (`scripts/purge_html.py`).

---

## 2. Sanskrit & Devanāgarī Typographical Standards

To eliminate ambiguity and visual clutter, strict orthographical conventions are enforced:

1. **No Italics:**
   Sanskrit terms and IAST transliterations are **never** italicized (`*...*`).
2. **Signal Red for Devanāgarī Only:**
   The `:sig[...]` syntax must never be applied to Latin text or IAST transliterations.
3. **Protection Wrappers:**
   Devanāgarī tokens must be enclosed in `⟪...⟫` tags to shield them against unintended LLM translation drift.
4. **Table Cell Formatting:**
   No parentheses around Devanāgarī text inside table cells.
   Multi-line table cells use `:br` on a single line instead of broken newline rows.

---

## 3. Grammar Box Architecture (`grammar-box`)

Grammatical rules, inflection tables, and notes follow a rigid encapsulation structure:

- **Mirroring HTML Indentation:**
  Tables and formal rules must never be wrapped in Markdown blockquotes (`>`).
- **Externalizing Examples:**
  Direct speech, contextual glosses, and translation examples remain **outside** grammar boxes (formatted inside `::: indent`).
- **Box Nesting:**
  Subordinate boxes increment the colon delimiter:
  ```markdown
  ::: grammar-box
  Primary Sandhi rule governing vocalic finals...
  
  :::: grammar-box
  Subordinate exception for Vedic archaisms...
  ::::
  :::
  ```

---

## 4. QA Gates & Code Governance

1. **Totalbremse (Hard Stop):**
   Master German lessons (`docs/lektionen/*.md`) and 100% completed language suites are read-only.
2. **Status Truth:**
   Exclusively use `get_translation_queue` from `scripts/translation_qa.py`. Never duplicate status or queue determination logic.
3. **Verification Gate:**
   All Python script updates must pass `python3 -m py_compile` and execute with Exit Code 0 before reporting completion.
