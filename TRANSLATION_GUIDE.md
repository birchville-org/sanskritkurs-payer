# Translation & Localization Guide

This document contains the guidelines and standard operating procedures for adding new languages and managing translations via the automated LLM scripts.

## Adding a New Language (Workflow)

When adding a new language to the Payer Sanskrit course, **never manually pre-fill or copy placeholder files** (e.g., `cp -r docs/en docs/he`). Doing so will cause the translation script to assume the files are already up-to-date and skip them!

The correct, fully automated workflow is:

1. **Configure VitePress Navigation:** Add the new language code and its navigation/sidebar settings to `docs/.vitepress/config.mjs`.
2. **Update the Translation Script:** Add the language code and its full name to the `LANGUAGES` and `LANG_NAMES` dictionaries in `scripts/lan_translate.py`. Also, add the UI translations for `LICENSES_LABELS` and `LICENSES_PHRASES` inside the script.
3. **Run the Translation:** Execute the script directly from the project root. The script will automatically create the required directories (`docs/[lang]/lektionen/` etc.) and generate the translated files from the German source (`docs/lektionen/`):
   ```bash
   python3 scripts/lan_translate.py --lang [code] all
   ```
