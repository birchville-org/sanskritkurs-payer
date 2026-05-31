---
phase: 15-vitepress-aware-markdown-editor
reviewed: 2026-05-31T00:00:00Z
depth: standard
files_reviewed: 1
files_reviewed_list:
  - docs/public/qa_viewer.html
findings:
  critical: 3
  warning: 5
  info: 4
  total: 12
status: issues_found
---

# Phase 15: Code Review Report

**Reviewed:** 2026-05-31
**Depth:** standard
**Files Reviewed:** 1 (`docs/public/qa_viewer.html`)
**Status:** issues_found

## Summary

`qa_viewer.html` is a client-side tool: a side-by-side VitePress QA viewer with an embedded Markdown editor/preview. The implementation covers iframe sync, scroll-header matching, a debounced editor, and a markdown-it renderer with scholarly custom rules. The majority of the file is well-structured, but three critical issues were found, the most dangerous of which is the `postMessage` origin wildcard that allows any cross-origin page to drive scroll behavior inside the iframes. Two additional issues represent real logic bugs in the `norm()` function and the `setViewMode('editor')` branch that causes the display to degrade silently. Five warnings address error handling, correctness, and reliability.

---

## Critical Issues

### CR-01: `postMessage` sent and received with wildcard origin `'*'`

**File:** `docs/public/qa_viewer.html:545-546, 758, 870, 897`

**Issue:** `syncThemeToFrames()` sends theme messages using `postMessage(msg, '*')`. The injected sender/receiver scripts (lines 863, 887) also listen to `window.addEventListener('message', ...)` without validating `e.origin`. Any page loaded in an iframe — or any page on any domain that can navigate/open the parent — can dispatch a `setScroll` or `setTheme` message and have it acted on. More critically, the receiver script at line 888-891 executes `window.scrollTo()` based on arbitrary `e.data.pct` values from untrusted sources; with `html: true` in markdown-it, a crafted lesson file could inject an inline script that posts arbitrary messages.

Combined with `html: true` (see CR-02), this creates a two-step escalation: injected HTML in a lesson file fires a script that posts a `setTheme` or `setScroll` message which the viewer obeys without verifying origin.

**Fix:** Replace the wildcard target origin with the known application origin when sending:
```js
// In syncThemeToFrames — use baseUrl (already defined) as the target origin
leftFrame.contentWindow.postMessage(msg, window.location.origin);
rightFrame.contentWindow.postMessage(msg, window.location.origin);
```
In the injected receiver/sender scripts, validate before acting:
```js
window.addEventListener('message', (e) => {
    if (e.origin !== window.location.origin) return; // guard
    // ... rest of handler
});
```

---

### CR-02: `innerHTML` assignment with `html: true` in markdown-it — no sanitization

**File:** `docs/public/qa_viewer.html:584-587, 942`

**Issue:** `renderPreview()` does:
```js
let html = window.md.render(editorInput.value);
html = html.replace(/\[\[br\]\]/g, '<br>');
editorPreview.innerHTML = html;
```
The markdown-it instance is created with `{ html: true }`, which passes raw HTML blocks in the Markdown source straight through to output. Any raw `<script>` tag, `<img onerror="…">`, or event-handler attribute present in the `.md` source file will execute in the page context when `innerHTML` is set. Even if this is intentionally an "author-only" tool, the Markdown files are fetched from the server at runtime via `fetch()` (line 605-608) — if any upstream file is compromised, XSS executes immediately in the QA viewer's document.

The `html.replace(/\[\[br\]\]/g, '<br>')` post-processing step (line 586) shows the code is already doing string manipulation after rendering, adding another surface for injection if `[[br]]` appears inside an HTML attribute value that markdown-it passes through verbatim.

**Fix (minimal):** Pass rendered HTML through DOMPurify before assignment:
```js
// Add to <head>:
// <script src="https://unpkg.com/dompurify@3/dist/purify.min.js"></script>
editorPreview.innerHTML = DOMPurify.sanitize(html, { ADD_TAGS: ['br'], FORCE_BODY: true });
```
Alternatively set `html: false` and rely solely on the custom container/token pipeline, which already handles the project-specific constructs.

---

### CR-03: Double registration of the `input` debounce listener — guaranteed duplicate fires

**File:** `docs/public/qa_viewer.html:615-632`

**Issue:** The `input` event listener on `editor-input` is registered **twice**: once inside a `DOMContentLoaded` handler (line 615-621) and once in an immediately-invoked function that runs before `DOMContentLoaded` fires (lines 623-632). The comment calls the second registration a "fallback", but this logic is flawed:

1. When the page loads normally, `DOMContentLoaded` has not yet fired when the IIFE runs, so the IIFE registers the listener. Then `DOMContentLoaded` fires and registers a second listener on the same element.
2. The `_debounceRegistered` flag on line 625 only guards the IIFE path; it does not prevent the `DOMContentLoaded` handler from adding a second listener.
3. Result: every keystroke fires `renderPreview` twice (two separate `setTimeout(renderPreview, 300)` calls are cleared and re-set independently, so the last one wins — this is actually benign in practice). However if the `clearTimeout` semantics ever change or the code is refactored, it becomes a double-render bug.

More importantly: this dual-registration pattern indicates a logic misunderstanding. Inline `<script>` blocks inside `<body>` always run *after* the DOM elements above them are parsed (the `editor-input` textarea is in the DOM at line 508), so the `DOMContentLoaded` wrapper is unnecessary and the "fallback" is the only path that would ever be needed.

**Fix:** Remove the `DOMContentLoaded` wrapper entirely and keep only the IIFE:
```js
// Remove lines 615-621 entirely.
// The IIFE (lines 623-632) is sufficient and executes after the textarea exists.
```

---

## Warnings

### WR-01: `norm()` object literal contains duplicate keys — several IAST mappings silently dropped

**File:** `docs/public/qa_viewer.html:682`

**Issue:** The `MAP` object literal (never used in the function body) and the replace map inside the `norm()` function both contain duplicate keys. In the replace map:
```js
{ 'ā':'a','ī':'i','ū':'u','ṛ':'r','ṝ':'r','ḷ':'l','ṅ':'n','ñ':'n','ṭ':'t','ḍ':'d','ṇ':'n','ś':'s','ṣ':'s','ḥ':'h' }
```
The key `'n'` appears three times (`ṅ→n`, `ñ→n`, `ṇ→n` all map FROM different characters, so the target-side is fine), but more critically the `MAP` object at line 682 has `r`, `n`, `s` each defined multiple times as keys:
```js
const MAP = {a:'ā',i:'ī',u:'ū',r:'ṛ',r:'ṝ',l:'ḷ',n:'ṅ',n:'ñ',t:'ṭ',d:'ḍ',n:'ṇ',s:'ś',s:'ṣ',h:'ḥ'};
```
`r` is defined twice (values `ṛ` and `ṝ`), `n` three times, `s` twice. In strict mode this is a syntax error; in sloppy mode the last value wins and all prior bindings are silently lost. `MAP` is declared but **never referenced** anywhere in the function body, so it has no runtime effect today — but it signals intent to use it, and when that wiring is added the dead code will silently misbehave.

**Fix:** Remove the unused `MAP` object entirely (lines 682, col 12-80). The actual working map in the `.replace()` call uses the correct direction (diacritic→ascii) and has no duplicate source keys.

---

### WR-02: `setViewMode('editor')` hides raw viewers but never resets `viewMode` for `updateFrames`

**File:** `docs/public/qa_viewer.html:641-657`

**Issue:** When `setViewMode('rendered')` or `setViewMode('raw')` is called after editor mode, `updateFrames()` is called (line 655). Inside `updateFrames()`, the branch at line 805 checks `if (viewMode === 'raw')`. Because `viewMode` is set at line 636 before the branching logic, this is correct. However, when transitioning *from* `editor` back to `rendered`, `updateFrames()` calls:
```js
leftFrame.contentWindow.location.replace(lUrl);
```
at line 811, but the iframes were hidden (`display: none`) during editor mode. They are made visible again at lines 810-811 only in the `else` branch of `updateFrames`, which is correct. The bug is subtler: on line 641-650, when entering editor mode, `leftFrame.style.display = 'none'` and `rightFrame.style.display = 'none'` are set directly on the element's `style` attribute. When exiting, `updateFrames()` sets `leftFrame.style.display = 'block'` (line 810). This works.

The actual defect: `editorInput.style.display = 'block'` at line 648, but the CSS class `.editor-input` has `display: none` as default. Inline styles take precedence, so this is fine — *except* when `updateFrames()` is called from `setViewMode('raw')` or `setViewMode('rendered')` after exiting editor mode, `editorInput.style.display = 'none'` is set (line 653). However `editorPreview.style.display = 'none'` is also correctly set at line 654. So far coherent.

The real bug: inside `setViewMode`, the `else` branch (line 651) calls `updateFrames()`, and `updateFrames()` at line 809 unconditionally sets `leftRaw.style.display = 'none'` and `rightRaw.style.display = 'none'` — even if the new mode is `'raw'`. Looking at line 805: `if (viewMode === 'raw')` — since `viewMode` is already set at line 636, this check runs correctly. So raw mode is handled. BUT: the `else` branch of `updateFrames()` (lines 809-812) sets `leftFrame.style.display = 'block'` and `rightFrame.style.display = 'block'` unconditionally before checking whether `viewMode === 'raw'`. If `viewMode === 'raw'`, control flow enters the `if` block at line 806 and the `else` block is skipped — so the iframes are not shown. This is correct.

Revised finding: there is a real missing-mode bug when the user is in editor mode and the lesson number changes via `updateLesson()` (line 912). `updateLesson()` calls `updateFrames()` directly without going through `setViewMode`. If `viewMode === 'editor'` at that point, `updateFrames()` enters the `else` branch (since `viewMode !== 'raw'`) and sets `leftFrame.style.display = 'block'`, overlapping the editor textarea visually, because both the editor elements and the iframes end up visible.

**Fix:**
```js
function updateFrames() {
    if (viewMode === 'editor') return; // editor manages its own state
    // ... rest of function
}
```

---

### WR-03: `loadEditorContent` silently swallows fetch errors, leaving stale content in editor

**File:** `docs/public/qa_viewer.html:604-611`

**Issue:** The catch block sets `editorInput.value = ''` (empty string) on any fetch failure (network error, 404, etc.). If the user had previously typed content in the editor, a failed lesson switch silently wipes it. There is no user-visible feedback that the fetch failed.

```js
} catch(_) {
    editorInput.value = '';
}
```

The error is fully consumed and discarded. A user switching lessons while offline, or switching to a lesson that has no `.md` file yet, loses whatever they had typed.

**Fix:** Display an error message to the user instead of silently clearing:
```js
} catch(e) {
    editorInput.value = '<!-- Fehler beim Laden: ' + mdUrl + ' -->';
    renderPreview(); // Show the error in preview too
}
```

---

### WR-04: CDN dependency on `unpkg.com` UMD script loaded without Subresource Integrity (SRI)

**File:** `docs/public/qa_viewer.html:933`

**Issue:**
```html
<script src="https://unpkg.com/markdown-it-multimd-table@4.2.3/dist/markdown-it-multimd-table.min.js"></script>
```
This script is fetched from `unpkg.com` with no `integrity` attribute. If unpkg.com is compromised or the package is tampered with on the CDN, the injected script runs with full page privileges. The `esm.sh` imports on lines 937-938 have the same problem. Given that `html: true` is also set, a compromised CDN script could inject arbitrary HTML that then renders in the preview.

**Fix:** Compute and add SRI hashes:
```html
<script src="https://unpkg.com/markdown-it-multimd-table@4.2.3/dist/markdown-it-multimd-table.min.js"
        integrity="sha384-<hash>"
        crossorigin="anonymous"></script>
```
For ESM imports from esm.sh, SRI is not directly supported in dynamic `import` statements — consider bundling these dependencies locally via `npm` and serving from `/public/` instead.

---

### WR-05: `scrollToMatch` releases `isSyncing` in a `finally` block with a 700 ms timeout, but `isSyncing = false` in `setTimeout` is not inside `finally`

**File:** `docs/public/qa_viewer.html:693-739`

**Issue:** The `isSyncing` flag is set to `true` at line 692 to prevent re-entrant scroll sync. It is reset via `setTimeout(() => { isSyncing = false; }, 700)` inside a `finally` block (line 737). If `scrollToMatch` is called while `isSyncing` is still `true` (within the 700 ms window), the call returns early at line 691. However:

1. If `scrollToMatch` throws *before* reaching `isSyncing = true`, the flag is not set — this is fine.
2. If `scrollToMatch` throws *after* line 692 sets `isSyncing = true`, the `finally` block runs and schedules the reset — this is correct.
3. The real issue: the `isSyncing = true` at line 692 is set *before* the `try` block opens. If an exception occurs between line 692 and the `try` block entry, `isSyncing` is permanently locked to `true` and scroll sync is broken for the session.

In the current code, lines 692-693 are:
```js
isSyncing = true;
try {
```
There is nothing between them, so the exception window is effectively zero. However, if the code is extended (e.g., a synchronous cross-origin access check), this becomes a real lock-up risk.

**Fix:** Move `isSyncing = true` to the first line inside the `try` block to guarantee the `finally` handler always runs when the flag is set:
```js
try {
    isSyncing = true;
    const doc = targetWin.document;
    // ...
```

---

## Info

### IN-01: Devanāgarī color in editor preview uses `#b22222` (firebrick), not `#ff0000` as required by CLAUDE.md

**File:** `docs/public/qa_viewer.html:389`

**Issue:** CLAUDE.md hard rule: "Devanāgarī is always red: The CSS renders all `.sanskrit-dev` spans in `#ff0000`." The editor preview stylesheet overrides this with:
```css
.editor-preview .sanskrit-dev { color: #b22222; font-size: 1.15em; font-weight: 600; }
```
`#b22222` is firebrick, a noticeably darker red. This creates a visible inconsistency between the editor preview and the live VitePress site. This is an Info finding rather than a Critical because it only affects the QA tool's preview styling, not the production output, but it violates a project hard rule.

**Fix:**
```css
.editor-preview .sanskrit-dev { color: #ff0000; font-size: 1.15em; font-weight: 600; }
```

---

### IN-02: Dead variable `MAP` in `norm()` function — declared but never referenced

**File:** `docs/public/qa_viewer.html:682`

**Issue:** `const MAP = {a:'ā', ...}` is declared at the start of `norm()` but the function body never references `MAP`. It is also constructed in the wrong direction (latin→diacritic, whereas the actual replace map goes diacritic→latin). This is dead code that will confuse future maintainers.

**Fix:** Delete line 682 entirely.

---

### IN-03: `postMessage` sent to `'*'` in `injectReceiver` quotes the wrong parent origin inside the injected script string

**File:** `docs/public/qa_viewer.html:886`

**Issue:** `window.parent.postMessage({ type: 'getTheme' }, '*')` inside the injected receiver script (line 886) sends to `'*'`. Since the parent is always the QA viewer itself (same origin), this should use `window.location.origin` of the parent — but that value is not available inside the injected string without being passed in. This is a minor secondary instance of the CR-01 wildcard origin issue.

---

### IN-04: `console.log` and `console.warn` left in production scroll-sync code

**File:** `docs/public/qa_viewer.html:730, 733`

**Issue:**
```js
console.log('[QA] "' + searchText + '" -> "' + best.innerText.trim() + '" (score ' + bestScore + ')');
console.warn('[QA] No match for "' + searchText + '" (best ' + bestScore + ')');
```
These are informational during development but will appear in every user's browser console. The `console.warn` in particular can appear alarming. For a shipped tool, these should be removed or guarded by a debug flag.

**Fix:** Remove or gate behind a `const DEBUG = false` flag.

---

_Reviewed: 2026-05-31_
_Reviewer: Claude (gsd-code-reviewer)_
_Depth: standard_
