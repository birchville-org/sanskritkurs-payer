# Phase 15: VitePress-aware Markdown Editor - Research

**Researched:** 2026-05-31
**Domain:** Client-side Markdown rendering, split-pane editor UI, VitePress plugin parity
**Confidence:** HIGH

---

## Summary

Phase 15 builds a split-pane Markdown editor with a live preview that accurately replicates
the VitePress production rendering. The key technical challenge is that VitePress uses
`markdown-it` with several custom plugins (containers, multimd-table, scholarly_fixes) that
no generic preview tool supports. The solution is to load the exact same packages client-side
via CDN (esm.sh), reproduce the `scholarly_fixes` core rule in JavaScript, and inject the
project's CSS into a scoped preview pane.

The editor integrates into `qa_viewer.html` as a third tab/mode alongside "Rendered" and
"Raw Source". This is the lowest-risk integration path because the viewer already has the
tab button-group pattern, the resizer, pane HTML, and theme toggle — all reusable.

The `[[br]]` substitution and Devanagari auto-wrapping are handled inside a single
`md.core.ruler` pass (`scholarly_fixes`) in `config.mjs`. This logic must be translated
verbatim to the client-side script. It is not complex (one regex split + Unicode range
test) but must be exact to match production output.

A `<textarea>` editor with 300 ms debounce is the lowest-complexity starting point.
CodeMirror 6 adds syntax highlighting and is available via esm.sh, but it is a
significantly larger dependency tree and should be treated as an optional upgrade.

**Primary recommendation:** Implement the editor as a new "Editor" tab injected into
`qa_viewer.html`. Use a `<textarea>` for the editor pane and a `<div>` for the preview pane.
Load `markdown-it`, `markdown-it-container`, and `markdown-it-multimd-table` from esm.sh
at the pinned versions already installed in the project. Replicate `scholarly_fixes` inline.
Inject the project's `custom.css` into the preview `<div>` via a `<style>` block.

---

## Architectural Responsibility Map

| Capability | Primary Tier | Secondary Tier | Rationale |
|------------|-------------|----------------|-----------|
| Markdown parsing | Browser / Client | — | All rendering is client-side; no server round-trip needed |
| Live preview rendering | Browser / Client | — | Instant feedback requires synchronous in-page re-render |
| Editor input | Browser / Client | — | `<textarea>` or CodeMirror widget in the left pane |
| Container plugin config | Browser / Client | — | Mirrors config.mjs logic, but runs entirely in browser JS |
| `[[br]]` substitution | Browser / Client | — | Part of scholarly_fixes core rule — replicated client-side |
| CSS for containers | Browser / Client | — | Subset of custom.css injected into preview scope |
| Tab/mode switching | Browser / Client | — | Existing qa_viewer.html JS pattern extended |
| File loading | Browser / Client | — | `fetch()` for .md files (same as existing Raw Source mode) |

---

<phase_requirements>
## Phase Requirements

| ID | Description | Research Support |
|----|-------------|------------------|
| EDIT-01 | Client-side Markdown renderer with markdown-it + VitePress container plugins (grammar-box, indent, deleteme-box, media, no-header) | All three packages available via esm.sh at pinned versions; container plugin config is 12 identical `md.use(container, name, render)` calls from config.mjs |
| EDIT-02 | Split-pane UI: Editor (CodeMirror/Textarea) left, live preview right | qa_viewer.html already has the pane/resizer HTML and CSS; the editor tab reuses `#left-pane` for the textarea and `#right-pane` for the preview div |
| EDIT-03 | `[[br]]` line-break substitution in renderer | Logic is a single `split('[[br]]')` producing `hardbreak` tokens; can be replicated as a plain JS string replacement before `md.render()` or as a core rule |
| EDIT-04 | MultiMD-Table rendering (markdown-it-multimd-table) | Package available via esm.sh; options (multiline, rowspan, headerless, multiscript, colspans) are documented in config.mjs and must be passed identically |
| EDIT-05 | Integration into qa_viewer.html as new tab/mode | Third button added to `#view-controls` btn-group; editor tab hides iframes and shows textarea + preview div |
</phase_requirements>

---

## Standard Stack

### Core

| Library | Version | Purpose | Why Standard |
|---------|---------|---------|--------------|
| markdown-it | 14.2.0 | Markdown-to-HTML parser | Already used by VitePress; exact same instance config = production parity [VERIFIED: npm registry] |
| markdown-it-container | 4.0.0 | Block-level custom containers (`::: grammar-box` etc.) | Already a project dependency; all 12 container types defined in config.mjs [VERIFIED: npm registry] |
| markdown-it-multimd-table | 4.2.3 | MultiMarkdown table extensions (colspan, rowspan, headerless) | Already a project dependency; same options flags required [VERIFIED: npm registry] |

### Supporting

| Library | Version | Purpose | When to Use |
|---------|---------|---------|-------------|
| esm.sh CDN | — | Serve the above as ES modules via `import` in a `<script type="module">` | Avoids a build step; all three packages resolve correctly at exact version pins |
| CodeMirror 6 | 6.x | Syntax-highlighted editor with line numbers | Only if plain `<textarea>` proves insufficient for UX requirements (EDIT-02 says "CodeMirror/Textarea") |

### Alternatives Considered

| Instead of | Could Use | Tradeoff |
|------------|-----------|----------|
| esm.sh CDN | Local bundle (esbuild/rollup) | Bundle avoids CDN dependency and works offline; adds a build step and maintenance burden. CDN is simpler for a single HTML file |
| esm.sh CDN | unpkg or jsdelivr | All three CDNs serve ESM; esm.sh is confirmed working for these packages |
| `<textarea>` | CodeMirror 6 | CodeMirror adds ~200 KB of JS, requires 5+ `import` statements from `@codemirror/*`, and has a steeper integration curve; textarea works for the stated requirements |

**Installation:**

No new packages need to be installed — `markdown-it`, `markdown-it-container`, and
`markdown-it-multimd-table` are already in `package.json`. The editor uses them via CDN
import only (no npm install step for the HTML file).

**Version verification:**

```bash
# Already installed in the project:
# markdown-it           14.2.0  (node_modules/markdown-it)
# markdown-it-container  4.0.0  (node_modules/markdown-it-container)
# markdown-it-multimd-table 4.2.3 (node_modules/markdown-it-multimd-table)
npm view markdown-it version           # -> 14.2.0
npm view markdown-it-container version # -> 4.0.0
npm view markdown-it-multimd-table version # -> 4.2.3
```

---

## Package Legitimacy Audit

| Package | Registry | Age | Downloads | Source Repo | slopcheck | Disposition |
|---------|----------|-----|-----------|-------------|-----------|-------------|
| markdown-it | npm | ~12 yrs (2014) | 22.6M/wk | github.com/markdown-it/markdown-it | [OK] | Approved |
| markdown-it-container | npm | ~11 yrs (2015) | 449K/wk | github.com/markdown-it/markdown-it-container | [OK] | Approved |
| markdown-it-multimd-table | npm | ~8 yrs (2017) | 32K/wk | github.com/redbug312/markdown-it-multimd-table | [OK] | Approved |

**Packages removed due to slopcheck [SLOP] verdict:** none

**Packages flagged as suspicious [SUS]:** none

All three packages are already installed in the project and passed slopcheck verification.
No new packages are introduced by this phase.

---

## Architecture Patterns

### System Architecture Diagram

```
User types in <textarea> (left pane)
        |
        | oninput event (300ms debounce)
        v
scholarly_fixes(rawText)
  ├── replace [[br]] -> \n (or hardbreak token)
  └── wrap Devanagari runs in <span class="sanskrit-dev">
        |
        v
md.render(processedText)
  using: markdown-it 14.2.0
       + markdown-it-multimd-table (options from config.mjs)
       + markdown-it-container × 12 (grammar-box, grammar-box2, media,
         center, metrik-schema, important, deleteme-box, note-box,
         laut-table, indent, compact, no-header)
        |
        v
HTML string
        |
        v
preview <div> innerHTML = html
  with: scoped CSS (grammar-box, sanskrit-dev, etc.)
        (subset of custom.css injected as <style> in the pane)
```

### Recommended Project Structure

The editor is a self-contained addition to the existing `docs/public/` file. No new
directories are needed:

```
docs/public/
├── qa_viewer.html          # Extended: new "Editor" tab added
└── (no new files required for Phase 15)
```

All editor logic lives inside `qa_viewer.html` as a `<script type="module">` block.

### Pattern 1: ESM import of markdown-it from CDN

**What:** Load markdown-it and plugins as ES modules in a `<script type="module">` block,
bypassing any build pipeline.

**When to use:** Single-file HTML tools like qa_viewer.html where adding a bundler is
disproportionate overhead.

**Example:**

```javascript
// Source: verified working via curl https://esm.sh/markdown-it@14.2.0
<script type="module">
import markdownit from 'https://esm.sh/markdown-it@14.2.0';
import container  from 'https://esm.sh/markdown-it-container@4.0.0';
import multimd    from 'https://esm.sh/markdown-it-multimd-table@4.2.3';

const md = markdownit({ html: false, breaks: true, linkify: false });
md.use(multimd, { multiline: true, rowspan: true, headerless: true, multiscript: true, colspans: true });

// Register all containers (same pattern, 12 times)
const containers = [
  'grammar-box', 'grammar-box2', 'media', 'center', 'metrik-schema',
  'important', 'deleteme-box', 'note-box', 'laut-table', 'indent', 'compact', 'no-header'
];
for (const name of containers) {
  md.use(container, name, {
    render(tokens, idx) {
      return tokens[idx].nesting === 1
        ? `<div class="${name} custom-block">\n`
        : '</div>\n';
    }
  });
}
</script>
```

### Pattern 2: scholarly_fixes client-side translation

**What:** The `scholarly_fixes` core rule in config.mjs does two things:
1. Splits text tokens on `[[br]]` and inserts `<br>` between segments
2. Wraps any Devanagari codepoint range (U+0900–U+097F) in `<span class="sanskrit-dev">`
   (or `hindi-dev` for hi/ pages — irrelevant for the editor which only handles one file at a time)
3. Wraps `⟨...⟩` explicitly-marked Sanskrit (U+27EA/U+27EB wrappers) the same way
4. Converts `[[indent]]` to `<span class="indent-inline"></span>`

**When to use:** Applied to the raw Markdown string before calling `md.render()`.

**Approach:** The cleanest client-side equivalent is a pre-processing function on the raw
text rather than a `md.core.ruler` insertion (which requires the Token API and is harder
to debug in a browser context). However, because `[[br]]` only occurs inside inline text
nodes (not at the block level), a simple string substitution replacing `[[br]]` with
`<br>` works when `md` is initialized with `html: true` in the editor.

The Devanagari wrapping is more nuanced. The core rule wraps at the token level, which
means it works even inside bold/italic spans. A simpler client-side approach: after
`md.render()` produces an HTML string, apply a regex pass to wrap bare Devanagari runs:

```javascript
function applyScholarlyFixes(html) {
  // Wrap Devanagari runs not already inside a span.sanskrit-dev
  return html.replace(/([ऀ-ॿ]+)/g, (match, p1) => {
    return `<span class="sanskrit-dev">${p1}</span>`;
  });
}
```

**Caveat:** This post-render regex approach may double-wrap if the Devanagari was already
inside a span from an earlier pass. The core rule approach from config.mjs is more precise
but requires porting the Token manipulation logic. The planner should decide which approach
to implement — both achieve EDIT-03 parity. [ASSUMED]

**[[br]] substitution:** The `prevent_br_link` core rule in config.mjs first transforms
`[[br]](` to `[[br]] (` to prevent link parsing. Then `scholarly_fixes` splits text
tokens on `[[br]]` and inserts `hardbreak` tokens. Client-side equivalent:

```javascript
// Pre-process before md.render():
const processed = raw
  .replace(/\[\[br\]\]\(/g, '[[br]] (')   // mirror prevent_br_link
  .replace(/\[\[br\]\]/g, '  \n');         // two spaces + newline = hard break in markdown-it
```

This works because markdown-it with `breaks: true` treats two trailing spaces before a
newline as a `<br>`. [VERIFIED: markdown-it docs — breaks:true enables soft line breaks;
two-space trick is standard Markdown hard-break syntax]

### Pattern 3: Editor tab integration in qa_viewer.html

**What:** Add a third button to the existing `#view-controls` btn-group. When active, the
tab hides both iframes and shows a textarea (left) + preview div (right) instead.

**Current view-controls HTML (from qa_viewer.html lines 364-368):**

```html
<div class="btn-group" id="view-controls">
  <button class="control-btn active" onclick="setViewMode('rendered')" id="btn-rendered">Rendered</button>
  <button class="control-btn"        onclick="setViewMode('raw')"      id="btn-raw">Raw Source</button>
</div>
```

**Addition:**

```html
<button class="control-btn" onclick="setViewMode('editor')" id="btn-editor">Editor</button>
```

**In `setViewMode('editor')`:**
- Hide both `<iframe>` and `<textarea class="raw-viewer">` elements
- Show a new `<textarea id="editor-input">` in the left pane
- Show a new `<div id="editor-preview">` in the right pane
- Wire `editor-input` oninput to debounced `renderPreview()`

The resizer, theme toggle, and header controls work unchanged because they operate on
the pane containers, not on what's inside them.

**Loading a lesson into the editor:** When the user switches to Editor mode with a lesson
selected, optionally pre-populate the textarea by fetching the `.md` source (same as
`fetchRaw()` already does in Raw Source mode).

### Anti-Patterns to Avoid

- **Injecting VitePress CSS by linking to the built dist file:** The built VitePress CSS
  (`.vitepress/dist/`) references fonts and assets by relative path that break in a
  standalone HTML context. Copy only the relevant rule blocks from `custom.css` as an
  inline `<style>` block inside the editor preview div.

- **Using `marked.js` instead of `markdown-it`:** marked.js has no concept of
  `:::container` blocks and would require a separate parser for those. The requirement
  is explicit: use the same markdown-it stack as config.mjs.

- **Loading `markdown-it` without pinning the version:** CDN paths like
  `https://esm.sh/markdown-it` (no version) will silently upgrade on future requests.
  Always pin to `@14.2.0` to match the installed version.

- **Running `md.render()` synchronously on every keystroke:** For lessons with 200+ KB of
  Markdown, synchronous re-render on every character input will stutter. Always debounce
  by at least 200–300 ms.

- **Modifying `docs/lektionen/` files from the editor:** CLAUDE.md states "German is
  immutable: Files in `docs/lektionen/` are the reference. Never modify them via
  automation." The editor must be read-only with respect to actual files — it is a preview
  tool, not a file editor. Do not add a "Save" button that writes to the filesystem.

---

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| Markdown parsing | Custom regex parser | markdown-it 14.2.0 | markdown-it handles all CommonMark edge cases (escaped chars, nested inlines, list continuation, etc.) |
| MultiMD tables | Custom colspan/rowspan logic | markdown-it-multimd-table | colspan tracking across merged cells requires state machine; already solved |
| Custom container blocks | Custom `::: name` parser | markdown-it-container | Handles nesting, marker validation, and open/close token pairing |
| Resizable panes | Custom mouse drag logic | Existing resizer in qa_viewer.html | The resizer is already implemented and tested — reuse it |
| Theme toggle | New switch | Existing theme toggle in qa_viewer.html | The existing VPSwitch and `toggleTheme()` already toggle `.dark` on `documentElement` |

**Key insight:** All the hard UI infrastructure (resizer, theme, pane layout) already exists
in qa_viewer.html. The editor phase is primarily a *rendering integration* problem, not a
UI engineering problem.

---

## Common Pitfalls

### Pitfall 1: markdown-it `html` option

**What goes wrong:** The editor initializes `markdownit({ html: false })` (the default),
which causes raw HTML in the Markdown source (e.g., from legacy files) to be escaped and
shown as text instead of rendered. Alternatively, `html: true` enables XSS vectors if
user-supplied content is rendered in an iframe-less div.

**Why it happens:** The production VitePress config does not set `html:` explicitly, which
means it uses VitePress's own default (VitePress enables `html: true` internally).

**How to avoid:** For the editor preview — a tool used by the single project author, not
public users — `html: true` is acceptable and matches VitePress behavior. Document this
clearly. [ASSUMED — VitePress internally enables html:true; not independently verified]

**Warning signs:** Images, tables with raw HTML, or `<br>` tags appear as escaped text in
the preview.

### Pitfall 2: Container plugin registration order

**What goes wrong:** Registering `markdown-it-container` before
`markdown-it-multimd-table` or vice versa causes the multimd table parser to not
recognize certain row formats inside containers.

**Why it happens:** Both plugins manipulate block-level rules; order affects rule
priority in markdown-it's ruler chain.

**How to avoid:** Register `multimd_table` first, then all `container` plugins — exactly
as in config.mjs lines 226–347.

**Warning signs:** Multimd tables inside `::: grammar-box` render as plain text or
malformed HTML.

### Pitfall 3: CSS scope collision between preview div and qa_viewer styles

**What goes wrong:** CSS rules injected for the preview pane (e.g., `.grammar-box`,
`.sanskrit-dev`) leak into the outer qa_viewer.html UI, or vice versa.

**Why it happens:** qa_viewer.html has its own `.container`, `.pane`, button styles.
If the preview `<div>` is not scoped, class names collide.

**How to avoid:** Wrap the preview div in a `<div class="vp-doc">` or a unique wrapper
class (e.g., `editor-preview`), and prefix all injected CSS rules with that wrapper.
The `custom.css` rules already use `.vp-doc` as a prefix on most rules — use that.

**Warning signs:** qa_viewer header buttons change color; pane background changes
unexpectedly when Editor tab is active.

### Pitfall 4: `[[br]]` inside table cells

**What goes wrong:** `[[br]]` inside a table cell (which is already an inline context)
gets split into two lines, but the table parser requires each row to be a single line.
The two-space-newline approach breaks multimd table parsing if the newline falls inside
a cell.

**Why it happens:** config.mjs handles `[[br]]` at the token level *after* block parsing
is complete. A pre-processing string replacement happens *before* block parsing, which
breaks the multimd table parser's row detection.

**How to avoid:** Do the `[[br]]` replacement as a `md.core.ruler.after('linkify', ...)`
rule (same position as config.mjs), operating on `inline` token children — not as a
raw string substitution. The config.mjs approach (Token API) is the correct one. [ASSUMED]

**Alternative:** Replace `[[br]]` with `<br>` (literal HTML) in pre-processing,
which works if `html: true` is set and does not affect block parsing. Test carefully
against lessons that use `[[br]]` inside multimd table cells.

**Warning signs:** Table cells with `[[br]]` show as broken rows or missing content.

### Pitfall 5: Devanagari font not loading in preview div

**What goes wrong:** `<span class="sanskrit-dev">` is red (from CSS) but renders in a
fallback serif font, not in "Sanskrit2003" / "ITR Vijay" as in the VitePress build.

**Why it happens:** `custom.css` references `"Sanskrit2003"` and `"ITR Vijay"` — fonts
that are served by the VitePress dev server from `docs/public/fonts/` (if they exist) or
by the user's OS. In a standalone HTML context, the font may not be available.

**How to avoid:** Check whether the fonts exist in `docs/public/fonts/`. If so, inject
a `@font-face` rule using `url('/fonts/...')` in the preview CSS block. Otherwise, the
fallback `serif` still makes the text legible; the color rule works regardless.

**Warning signs:** Devanagari glyphs look different between the preview and the VitePress
build.

---

## Code Examples

### Minimal Working Renderer

```javascript
// Source: config.mjs (config pattern) + esm.sh CDN loading (verified working)
import markdownit from 'https://esm.sh/markdown-it@14.2.0';
import container  from 'https://esm.sh/markdown-it-container@4.0.0';
import multimd    from 'https://esm.sh/markdown-it-multimd-table@4.2.3';

function buildRenderer() {
  const md = markdownit({ html: true, breaks: true, linkify: false });

  md.use(multimd, {
    multiline: true, rowspan: true, headerless: true,
    multiscript: true, colspans: true
  });

  const CONTAINERS = [
    'grammar-box', 'grammar-box2', 'media', 'center', 'metrik-schema',
    'important', 'deleteme-box', 'note-box', 'laut-table',
    'indent', 'compact', 'no-header'
  ];
  for (const name of CONTAINERS) {
    md.use(container, name, {
      render(tokens, idx) {
        return tokens[idx].nesting === 1
          ? `<div class="${name} custom-block">\n`
          : '</div>\n';
      }
    });
  }

  // scholarly_fixes: [[br]] and Devanagari (post-render approach)
  const originalRender = md.render.bind(md);
  md.render = (src, env) => {
    // Pre-process: prevent [[br]] from being parsed as a link
    let processed = src.replace(/\[\[br\]\]\(/g, '[[br]] (');
    // Replace [[br]] with hard-break (two spaces + newline)
    processed = processed.replace(/\[\[br\]\]/g, '  \n');
    let html = originalRender(processed, env);
    // Post-process: wrap Devanagari in sanskrit-dev spans
    html = html.replace(/(<[^>]+>)|([^ -ࣿﬀ-￿]*[ऀ-ॿ][^ -ࣿﬀ-￿]*)/g,
      (match, tag, devanagari) => {
        if (tag) return tag; // don't touch HTML tags
        if (devanagari) return `<span class="sanskrit-dev">${devanagari}</span>`;
        return match;
      });
    return html;
  };

  return md;
}
```

### Editor Tab Integration Skeleton

```javascript
// Source: qa_viewer.html existing setViewMode pattern (lines 459-464)
function setViewMode(mode) {
  viewMode = mode;
  document.querySelectorAll('#view-controls .control-btn').forEach(b => b.classList.remove('active'));
  document.getElementById('btn-' + mode).classList.add('active');

  const editorInput   = document.getElementById('editor-input');
  const editorPreview = document.getElementById('editor-preview');

  if (mode === 'editor') {
    leftFrame.style.display = 'none';   rightFrame.style.display = 'none';
    leftRaw.style.display = 'none';     rightRaw.style.display = 'none';
    editorInput.style.display = 'block';
    editorPreview.style.display = 'block';
    // Optionally pre-load current lesson .md into textarea
  } else {
    editorInput.style.display = 'none';
    editorPreview.style.display = 'none';
    updateFrames(); // existing function handles rendered/raw
  }
}
```

### CSS injection for preview pane

```html
<!-- Injected as a <style> block inside qa_viewer.html -->
<style id="editor-preview-styles">
/* Scoped to .editor-preview to avoid leaking into qa_viewer UI */
.editor-preview { font-family: 'Source Serif 4', serif; font-size: 1.1rem;
  line-height: 1.55; color: var(--color-ink); background: var(--color-parchment);
  padding: 2rem; overflow-y: auto; height: 100%; }
.editor-preview .grammar-box {
  background-color: #fefce8; border-left: 5px solid #eab308;
  padding: 1.25rem; margin: 1.5rem 0; border-radius: 0 8px 8px 0; }
.editor-preview .grammar-box2 {
  background-color: #ffedd5; border-left: 5px solid #ea580c;
  padding: 1.25rem; margin: 1.5rem 0; border-radius: 0 8px 8px 0; font-weight: 600; }
.editor-preview .deleteme-box { display: none !important; }
.editor-preview .no-header table thead { display: none !important; }
.editor-preview .indent { padding-left: 2.5rem; margin: 0; }
.editor-preview .media { display: flex; flex-direction: column; align-items: center; margin: 2.5rem 0; }
.editor-preview .sanskrit-dev { color: #b22222; font-size: 1.15em; font-weight: 600; }
.editor-preview table { border-collapse: collapse; border: 1px solid #94a3b8; margin: 1rem 0; }
.editor-preview td, .editor-preview th { padding: 0.6rem 0.8rem; border: 1px solid #94a3b8; }
.editor-preview tr:nth-child(even) { background-color: #f1eee7; }
</style>
```

---

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| textarea + marked.js (basic) | markdown-it + same plugins as VitePress | Phase 15 | Accurate container rendering |
| Full CodeMirror integration | `<textarea>` with debounce as baseline | Phase 15 | Lower complexity first; CodeMirror optional |

**Deprecated/outdated:**

- Using `marked.js` for this project's preview: no support for `:::container` blocks or
  multimd table extensions. Do not use.

---

## Assumptions Log

| # | Claim | Section | Risk if Wrong |
|---|-------|---------|---------------|
| A1 | VitePress internally enables `html: true` in its markdown-it instance | Pitfall 1 | If false, `html: true` in editor diverges from production; but the risk is low (editor is a preview tool, not a content processor) |
| A2 | Post-render regex for Devanagari wrapping is sufficient vs. Token-level rule | Pattern 2 / Pitfall 4 | If Devanagari appears inside already-wrapped HTML (e.g., inside `<strong>`), the regex may produce double-wrapped or malformed output; test required |
| A3 | `[[br]]` as two-space-newline pre-processing is correct for multimd table cells | Pitfall 4 | If it breaks table parsing, need to switch to Token-level approach; plan should include a fallback task |
| A4 | Devanagari fonts ("Sanskrit2003", "ITR Vijay") are not present in docs/public/fonts/ | Pitfall 5 | If they exist, the editor can load them; if not, fallback serif is acceptable |

---

## Open Questions (RESOLVED)

1. **Load lesson file into editor on tab switch?**
   - What we know: `fetchRaw()` already fetches `.md` content for the Raw Source mode
   - What's unclear: Should the Editor tab auto-populate from the currently selected lesson, or start blank?
   - Recommendation: Auto-populate from the lesson selector (same as Raw Source) — this makes the editor immediately useful as a preview-QA tool

2. **Should the editor support saving changes?**
   - What we know: CLAUDE.md forbids modifying `docs/lektionen/` via automation
   - What's unclear: Whether a "copy to clipboard" or "download as .md" button is wanted
   - Recommendation: Read-only preview (no save); add clipboard copy as a low-cost enhancement

3. **Hindi locale detection in scholarly_fixes?**
   - What we know: The `scholarly_fixes` rule uses `state.env?.relativePath?.startsWith('hi/')` to switch between `sanskrit-dev` and `hindi-dev` classes
   - What's unclear: Whether the editor needs to support the hi/ locale distinction
   - Recommendation: Default to `sanskrit-dev` for all Devanagari; add a locale toggle checkbox only if requested

---

## Environment Availability

| Dependency | Required By | Available | Version | Fallback |
|------------|------------|-----------|---------|----------|
| esm.sh CDN | markdown-it ESM import | ✓ (verified via curl) | — (CDN service) | Local bundle via esbuild |
| markdown-it | EDIT-01 | ✓ | 14.2.0 | — |
| markdown-it-container | EDIT-01 | ✓ | 4.0.0 | — |
| markdown-it-multimd-table | EDIT-04 | ✓ | 4.2.3 | — |
| npm run docs:build | Build gate | ✓ | VitePress 1.1.4 | — |

**Missing dependencies with no fallback:** none

**Missing dependencies with fallback:** esm.sh CDN (fallback: local bundle, adds build step)

---

## Validation Architecture

The editor is a standalone HTML file with no server-side logic. Automated testing of a
`<textarea>` + `innerHTML` update loop is possible with Playwright/Puppeteer but would
be disproportionate for this phase. Manual QA is the primary validation method.

### Phase Requirements → Test Map

| Req ID | Behavior | Test Type | Automated Command | File Exists? |
|--------|----------|-----------|-------------------|-------------|
| EDIT-01 | grammar-box container renders with gold border | manual | open qa_viewer.html, type `::: grammar-box` | n/a |
| EDIT-02 | Resizer between textarea and preview works | manual | drag resizer bar | n/a |
| EDIT-03 | `[[br]]` in a table cell produces a line break | manual | paste `cell1 [[br]] cell2` in a table row | n/a |
| EDIT-04 | MultiMD colspan `|` syntax renders merged cell | manual | paste multimd table with `||` | n/a |
| EDIT-05 | Editor tab appears in qa_viewer.html view-controls | manual | open qa_viewer, click Editor button | n/a |

**Build gate:** `npm run docs:build` must pass after qa_viewer.html modifications. Because
qa_viewer.html is in `docs/public/` (static files), the build will not process it — but
the build confirms no other files were inadvertently broken.

### Wave 0 Gaps

- None — no new test files are needed. Manual QA against the lesson corpus is sufficient.

---

## Security Domain

The editor is a local development tool served from the VitePress dev server or preview
server. It is not exposed to the public internet and does not handle user authentication,
sessions, or server-side persistence. ASVS categories V2, V3, V4, V6 do not apply.

| ASVS Category | Applies | Standard Control |
|---------------|---------|-----------------|
| V2 Authentication | no | — |
| V3 Session Management | no | — |
| V4 Access Control | no | — |
| V5 Input Validation | partial | The preview renders arbitrary Markdown; `html: true` in md enables raw HTML. Acceptable for a single-author local tool; document explicitly in code comments. |
| V6 Cryptography | no | — |

---

## Sources

### Primary (HIGH confidence)

- `docs/.vitepress/config.mjs` (read directly) — container plugin configuration, scholarly_fixes rule, multimd options, prevent_br_link rule
- `docs/.vitepress/theme/custom.css` (read directly) — all CSS rules for containers, sanskrit-dev, hindi-dev, dark mode
- `docs/public/qa_viewer.html` (read directly) — existing tab/view-mode pattern, pane HTML, resizer, theme toggle, fetchRaw()
- `package.json` (read directly) — installed package versions

### Secondary (MEDIUM confidence)

- `https://esm.sh/markdown-it@14.2.0` — HTTP 200 confirmed; ESM export verified
- `https://esm.sh/markdown-it-container@4.0.0` — HTTP 200 confirmed
- `https://esm.sh/markdown-it-multimd-table@4.2.3` — HTTP 200 confirmed
- `api.npmjs.org/downloads/point/last-week/markdown-it` — 22.6M weekly downloads confirmed

### Tertiary (LOW confidence)

- None

---

## Metadata

**Confidence breakdown:**

- Standard stack: HIGH — all packages already installed; CDN loading verified
- Architecture: HIGH — based directly on reading config.mjs and qa_viewer.html
- scholarly_fixes translation: MEDIUM — post-render Devanagari regex (A2/A3 assumptions)
- Pitfalls: HIGH — derived from actual code analysis of config.mjs and CSS

**Research date:** 2026-05-31
**Valid until:** 2026-08-31 (stable packages; markdown-it is slow-moving)
