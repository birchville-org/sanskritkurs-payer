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
- **No Redundant Overviews**: Omit static "Übersicht" (TOC) sections at the start of lessons; the VitePress sidebar provides this functionality.
- **Absolute Content & Structure Fidelity**: Except for the "Übersicht" (TOC), no content from the original HTML may be shortened, summarized, or omitted. The original didactic structure (e.g., highlighting via tables or colored boxes) must be preserved 1:1 using the `grammar-box` container. Every example, note, and exercise must be transferred 1:1.