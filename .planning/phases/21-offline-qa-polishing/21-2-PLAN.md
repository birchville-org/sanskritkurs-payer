---
phase: 21-offline-qa-polishing
plan: 2
type: execute
wave: 1
depends_on: [21-1]
files_modified:
  - docs/public/images/
  - docs/.vitepress/dist/assets/
autonomous: true

must_haves:
  truths:
    - "WebP conversion reduces total image size by >= 30%"
    - "All image references in markdown files remain valid"
    - "Build still succeeds after conversion"
  artifacts:
    - path: ".planning/phases/21-offline-qa-polishing/image-audit.md"
      provides: "Image size comparison before/after"
      contains: "total size, file count, largest files"
  key_links:
    - from: "docs/public/images/*.jpg"
      to: "docs/public/images/*.webp"
      via: "markdown image references"
      pattern: "!\[.*\]\(.*\.jpg\)"
---

# Plan 21-2: Performance Optimization (Image Conversion)

**Phase**: 21 Offline QA & Polishing
**Status**: Pending
**Dependencies**: Plan 21-1 ✅

## Objective

Audit and optimize images. Convert large JPG/PNG files to WebP for reduced bandwidth. Measure impact on build size.

## Tasks

### Task 21-2.1: Image Audit

<task type="auto">
<name>Audit all images in docs/</name>
<files>
  - docs/public/images/
  - docs/**/*.md
</files>
<read_first>
- docs/public/images/ (directory listing)
</read_first>
<action>
1. Count images by type:
   ```bash
   find docs -name '*.jpg' -o -name '*.jpeg' | wc -l
   find docs -name '*.png' | wc -l
   find docs -name '*.webp' | wc -l
   find docs -name '*.svg' | wc -l
   ```
2. Find largest images:
   ```bash
   find docs -name '*.jpg' -o -name '*.png' | xargs du -k | sort -rn | head -20
   ```
3. Identify images referenced in markdown files:
   ```bash
   grep -rl '\.jpg\|\.png\|\.webp' docs/**/*.md | head -30
   ```
4. Document findings in image-audit.md
</action>
<verify>
Image audit complete with counts, sizes, and references documented.
</verify>
<acceptance_criteria>
- Total image count by type recorded
- Top 20 largest images identified
- Image references in markdown mapped
- image-audit.md created
</acceptance_criteria>
</task>

### Task 21-2.2: WebP Conversion

<task type="auto">
<name>Convert large JPG/PNG images to WebP</name>
<files>
  - docs/public/images/
</files>
<read_first>
- docs/public/images/ (current files)
</read_first>
<action>
1. Check if cwebp is available: `which cwebp` or `brew list webp`
2. For images > 50KB, convert to WebP at quality 80:
   ```bash
   # Install if needed: brew install webp
   for f in docs/public/images/*.jpg; do
     base="${f%.jpg}"
     cwebp -q 80 "$f" -o "${base}.webp" 2>/dev/null
   done
   ```
3. For PNG images with transparency, convert to WebP:
   ```bash
   for f in docs/public/images/*.png; do
     base="${f%.png}"
     cwebp -q 80 "$f" -o "${base}.webp" 2>/dev/null
   done
   ```
4. Update markdown references from .jpg/.png to .webp
5. Keep originals as fallback (serve via conditional logic or keep both)
</action>
<verify>
WebP files created. Markdown references updated. Originals preserved.
</verify>
<acceptance_criteria>
- WebP files exist for all large images
- Markdown references point to .webp files
- Build still succeeds
- Images render correctly in preview
</acceptance_criteria>
</task>

### Task 21-2.3: Build Size Comparison

<task type="auto">
<name>Measure build size before and after</name>
<files>
  - docs/.vitepress/dist/
</files>
<action>
1. Record current dist size:
   ```bash
   du -sh docs/.vitepress/dist/
   du -sh docs/.vitepress/dist/assets/
   du -sh docs/.vitepress/dist/images/
   ```
2. Rebuild: `npm run docs:build`
3. Record new dist size
4. Calculate reduction percentage
</action>
<verify>
Size comparison documented.
</verify>
<acceptance_criteria>
- Before/after sizes recorded
- Reduction >= 20% target
- No broken image references
</acceptance_criteria>
</task>

## Verification

```bash
# Build check
npm run docs:build

# Image count
find docs -name '*.webp' | wc -l

# Dist size
du -sh docs/.vitepress/dist/
```

## Success Criteria

- [ ] Image audit complete with findings documented
- [ ] Large images converted to WebP
- [ ] Markdown references updated
- [ ] Build size reduced by >= 20%
- [ ] All images render correctly
- [ ] `npm run docs:build` successful
