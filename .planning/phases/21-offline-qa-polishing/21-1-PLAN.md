---
phase: 21-offline-qa-polishing
plan: 1
type: execute
wave: 1
depends_on: []
files_modified:
  - docs/.vitepress/dist/offline.html
  - docs/public/offline.html
autonomous: true

must_haves:
  truths:
    - "Lighthouse PWA score >= 90, Performance >= 80"
    - "Offline navigation works without JS errors"
    - "Offline fallback page renders correctly for all locales"
  artifacts:
    - path: ".planning/phases/21-offline-qa-polishing/lighthouse-report.md"
      provides: "Lighthouse audit results for DE, EN, IT"
      contains: "PWA score, Performance score, Accessibility, Best Practices"
  key_links:
    - from: "sw.js networkFirst"
      to: "offline.html fallback"
      via: "document request destination check"
      pattern: "request.destination === 'document'"
---

# Plan 21-1: Offline Testing (Lighthouse + Manual E2E)

**Phase**: 21 Offline QA & Polishing
**Status**: Pending
**Dependencies**: Phase 20 ✅

## Objective

Run Lighthouse audit against production build, perform manual offline E2E testing, and document results. Fix any issues found.

## Tasks

### Task 21-1.1: Build Production Bundle

<task type="auto">
<name>Build production bundle</name>
<files>
  <file>package.json</file>
  <file>docs/.vitepress/dist/</file>
</files>
<read_first>
- package.json (scripts section)
- docs/.vitepress/config.mjs (base, outDir)
</read_first>
<action>
Run `npm run docs:build` from project root. Verify exit code 0. Check dist/ size.
</action>
<verify>
Build succeeds, dist/ exists with all locale directories.
</verify>
<acceptance_criteria>
- npm run docs:build exits 0
- docs/.vitepress/dist/ contains de/, en/, it/, bg/, ru/, uk/, hi/, fr/, es/, ta/, pa/, la/, rm/, ro/, icons/, assets/, offline.html, sw.js, manifest.json
</acceptance_criteria>
</task>

### Task 21-1.2: Lighthouse Audit

<task type="auto">
<name>Run Lighthouse on DE, EN, IT homepages + Settings</name>
<files>
  - docs/.vitepress/dist/
</files>
<read_first>
- docs/.vitepress/dist/index.html (DE homepage)
- docs/.vitepress/dist/en/index.html (EN homepage)
- docs/.vitepress/dist/it/index.html (IT homepage)
</read_first>
<action>
1. Start preview server: `npm run docs:preview &`
2. Run Lighthouse via CLI for DE, EN, IT:
   ```
   npx lighthouse http://localhost:4173/ --only-categories=pwa,performance,accessibility,best-practices --output html --output-path .planning/phases/21-offline-qa-polishing/lighthouse-de.html
   npx lighthouse http://localhost:4173/en/ --only-categories=pwa,performance,accessibility,best-practices --output html --output-path .planning/phases/21-offline-qa-polishing/lighthouse-en.html
   npx lighthouse http://localhost:4173/it/ --only-categories=pwa,performance,accessibility,best-practices --output html --output-path .planning/phases/21-offline-qa-polishing/lighthouse-it.html
   ```
3. Also audit Settings page: `npx lighthouse http://localhost:4173/de/settings --only-categories=pwa,performance,accessibility,best-practices --output html --output-path .planning/phases/21-offline-qa-polishing/lighthouse-settings.html`
4. If Lighthouse CLI unavailable, use Chrome DevTools Lighthouse panel via browser automation.
</action>
<verify>
Lighthouse reports generated for DE, EN, IT, Settings.
</verify>
<acceptance_criteria>
- PWA category >= 90 on all locales
- Performance category >= 80 on all locales
- Accessibility >= 90
- Best Practices >= 90
- No critical errors
</acceptance_criteria>
</task>

### Task 21-1.3: Manual Offline E2E Test

<task type="auto">
<name>Manual offline testing via Chrome DevTools</name>
<files>
  - docs/.vitepress/dist/
</files>
<read_first>
- docs/public/offline.html
- docs/public/sw.js
</read_first>
<action>
1. Start preview: `npm run docs:preview`
2. Open in Chrome, navigate to /de/
3. Visit 3-5 lessons to populate cache
4. Open DevTools → Network tab → select "Offline" throttling
5. Test:
   a. Reload current page → should show cached version
   b. Navigate to previously visited lesson → should load from cache
   c. Navigate to unvisited page → should show offline.html
   d. Check Console for JS errors
   e. Toggle back to "No throttling" → page should reload
6. Repeat for /en/ and /it/
</action>
<verify>
All navigation works offline. No JS errors. Offline fallback renders correctly.
</verify>
<acceptance_criteria>
- Cached pages load instantly offline
- Unvisited pages show offline.html (not Chrome error page)
- Zero JS errors in Console during offline navigation
- Online restoration works (page reloads when network returns)
</acceptance_criteria>
</task>

### Task 21-1.4: Document Results

<task type="auto">
<name>Create Lighthouse results summary</name>
<files>
  - .planning/phases/21-offline-qa-polishing/lighthouse-report.md
</files>
<action>
Create lighthouse-report.md with:
- Score table: DE/EN/IT × (PWA, Performance, Accessibility, Best Practices)
- List of issues found (if any)
- Manual test pass/fail per locale
- Any bugs found and fixes applied
</action>
<verify>
Report file exists with structured results.
</verify>
<acceptance_criteria>
- All scores documented
- Issues listed with severity
- Manual test results recorded
</acceptance_criteria>
</task>

## Verification

```bash
# Build check
npm run docs:build

# Lighthouse (if installed)
npx lighthouse --version

# Dist size
du -sh docs/.vitepress/dist/
```

## Success Criteria

- [ ] Lighthouse PWA >= 90 on DE, EN, IT
- [ ] Lighthouse Performance >= 80 on DE, EN, IT
- [ ] Manual offline test: all cached pages load, offline fallback works, zero JS errors
- [ ] lighthouse-report.md created with results
- [ ] `npm run docs:build` successful
