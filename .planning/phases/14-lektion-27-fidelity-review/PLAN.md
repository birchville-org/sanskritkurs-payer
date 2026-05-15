# Phase Plan: 14 - Lektion 27 Fidelity & Review

## Context
High-fidelity manual reconstruction and validation of Sanskrit Lesson 27 following the "Scholarly Synthesis" design system and "Zero-HTML" policy.

## Requirements
- [x] 1:1 structural parity with original L27 HTML.
- [x] Zero-HTML in all sections.
- [x] Paradigm tables correctly formatted with all script entries (Case-first).
- [x] Standardized media captions and license links.
- [x] Devanāgarī exercise numbering.

## Plans

### Plan 14.1: Restoration of Core Structure & Media
- **Objective**: Restore the "Gold Standard" framework for Lesson 27.
- **Steps**:
    1. Restore YAML frontmatter (lesson_id: 27).
    2. Restore `::: deleteme-box` scholarly metadata.
    3. Convert all 18 image callouts to `::: media` containers with minimalist captions.
    4. Apply Devanāgarī numbering to Exercise 27.6 B.

### Plan 14.2: Paradigm Reconstruction & HTML Purge
- **Objective**: Rebuild linguistic paradigms and eliminate legacy HTML.
- **Steps**:
    1. Reconstruct tables for tad, etad, idam, yad, and kim in Section 27.7.12–14 using case-first layout.
    2. Ensure all Devanāgarī entries are accurate.
    3. Purge all `<br>` tags and other raw HTML syntax.

### Plan 14.3: Final Verification
- **Objective**: Ensure build stability and content parity.
- **Steps**:
    1. Audit against `original/lektion27.htm` for any dropped content.
    2. Run `npm run docs:build`.

## Verification
- [ ] Visual parity check in dev server.
- [ ] Build passes without Vue compiler errors.
