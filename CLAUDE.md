# Sanskritkurs Pipeline — Claude Instructions

> Full design system, typography rules, and QA checklists: see [AGENTS.md](AGENTS.md)
> Translation rules: see [TRANSLATION_GUIDE.md](TRANSLATION_GUIDE.md)

## Hard Rules (always apply)

- **Build Gate**: Every session ends with `npm run docs:build`. A task is only done if the build passes.
- **Zero-HTML**: No raw HTML in Markdown. Use `scripts/purge_html.py` to sanitize.
- **German is immutable**: Files in `docs/lektionen/` are the reference. Never modify them via automation.
- **Devanāgarī is always red**: The CSS renders all `.sanskrit-dev` spans in `#ff0000`. This applies everywhere — inside tables, grammar-boxes, plain text. Never add a CSS rule that overrides Devanāgarī color to `inherit` or any non-red value.
- **No Parentheses for Devanāgarī in tables**: Write `**dveṣṭi**[[br]]द्वेष्टि`, not `**dveṣṭi**[[br]](द्वेष्टि)`.
- **Single-line image captions**: `Abb.: ऊहापोहः` — pure Devanāgarī, no line breaks.
- **Table rows = single markdown line**: Use `[[br]]` for in-cell line breaks. Never split a row across lines.
- **Strict table cell parity**: Never add content (labels, genders, IAST) not explicitly in Payer's original HTML.

## Key Scripts

| Task | Command |
|------|---------|
| Translate lessons | `python3 scripts/lan_translate.py` |
| Sync layouts across languages | `python3 scripts/sync_layouts.py <lesson_num\|all>` |
| Sync image links | `python3 scripts/sync_images.py` |
| Purge raw HTML | `python3 scripts/purge_html.py` |

## Grammar-Box Quick Reference

- `::: grammar-box` → `:::: grammar-box` when it contains nested containers.
- Examples (`Beispiel:`) always go **outside** grammar-box, wrapped in `::: indent`.
- Tables inside grammar-box with empty header row → wrap in `::: no-header`.
- Metadata/citations → `::: deleteme-box` at end of document.
