# Research: Pitfalls to Avoid in v1.2

## 1. Search Precision vs. Recall
- **Over-folding**: Mapping `ś`, `ṣ`, and `s` all to `s` increases "recall" (finding things) but might overwhelm the user with irrelevant results if they are looking for a specific phoneme.
- **Solution**: Keep the original terms in the index but add the folded versions as "boosted" or "alternative" terms if MiniSearch allows, or accept the trade-off for ease of use.

## 2. i18n Sync Drifting
- **Problem**: Updating a lesson in German but forgetting to re-translate the Italian version.
- **Solution**: Implement a simple audit script (like `audit_translations.py`) that checks for existence and potentially modification dates across all locale folders.

## 3. Sidebar Maintenance
- **Problem**: Hand-rolling sidebars for 4 languages leads to copy-paste errors.
- **Solution**: Use the `getSidebarItems` helper function (already in `config.mjs`) consistently for all languages.

## 4. Frontmatter Inconsistency
- **Problem**: Different tags for the same concept (e.g., "Sandhi" vs "sandhi-rules").
- **Solution**: Create a controlled vocabulary for tags in a central `tags.json` and validate against it during build or planning.
