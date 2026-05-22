# Markdown Extensions & Dependencies

This document outlines the technical extensions to the standard Markdown specification used in this project. The system transforms Markdown from a simple formatting tool into a structured layout language for scholarly Sanskrit texts.

## 1. Plugin Dependencies

### `markdown-it-multimd-table` (Complex Tables)
Used to implement the "Grid Integrity" required for linguistic paradigms.
- **Rowspans (`^^`):** Vertical merging of cells (pulls content from the cell above).
- **Colspans (`||`):** Horizontal merging of cells.
- **Multiline Cells:** Allows actual line breaks within a single table cell.
- **Headerless Tables:** Support for tables without a formal header row.

### `markdown-it-container` (Custom Layout Blocks)
Implements semantical containers using the `::: name` $\rightarrow$ `Content` $\rightarrow$ `:::` syntax.

| Container | Purpose | Visual/Functional Effect |
| :--- | :--- | :--- |
| `::: grammar-box` / `grammar-box2` | Didactic rules | Yellow-background highlighted boxes |
| `::: media` | Images & Captions | Centered media with associated metadata |
| `::: center` | Alignment | Center-aligns the entire block content |
| `::: important` | Key Highlights | Purple/Strong emphasis boxes |
| `::: note-box` | Supplementary notes | Standardized note styling |
| `::: laut-table` | Sandhi/Phonetics | Specialized layout for phonetic laws |
| `::: indent` | Block Indentation | Indents the entire block content |
| `::: compact` | Density | Reduces vertical spacing within the block |
| `::: no-header` | TOC Control | Prevents anchor/header generation for the block |
| `::: metrik-schema` | Metrics | Specific layout for poetic meters |
| `::: deleteme-box` | Machine Metadata | Hidden in frontend; used for internal tracking |

---

## 2. Proprietary Custom Logic (Hard-coded in `config.mjs`)

Beyond plugins, the project employs custom `markdown-it` rulers to handle linguistic and formatting requirements.

### Specialized Inline Tags
The following patterns are intercepted and replaced during the parsing phase:
- `[[br]]` $\rightarrow$ Converted to a hard `<br>` tag to force line breaks within text blocks.
- `[[indent]]` $\rightarrow$ Converted to `<span class="indent-inline">` for word-level indentation.

### Automated Sanskrit Detection
A regex-based filter for Devanagari characters (`[ऀ-ॿ]+`) is applied globally:
- **Auto-wrapping:** Any text segment containing Devanagari is automatically wrapped in `<span class="sanskrit-dev">`.
- **Result:** Ensures consistent "Scholarly Red" styling and specific font rendering without requiring manual tagging by the author.

---

## Summary Syntax Reference

| Element | Syntax | Mechanism | Result |
| :--- | :--- | :--- | :--- |
| **Rowspan** | `^^` | `multimd-table` | Vertical cell merge |
| **Colspan** | `||` | `multimd-table` | Horizontal cell merge |
| **Custom Box** | `::: name` | `container` | Styled thematic block |
| **Line Break** | `[[br]]` | Custom Ruler | Forced `<br>` |
| **Sanskrit** | `अ` | Custom Ruler | Automatic `.sanskrit-dev` span |
| **Inline Indent**| `[[indent]]` | Custom Ruler | `.indent-inline` span |
