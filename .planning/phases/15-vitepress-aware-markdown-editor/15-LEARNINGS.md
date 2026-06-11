---
phase: 15
phase_name: "VitePress-aware Markdown Editor"
project: "Payer Sanskrit Course"
generated: "2026-06-04"
counts:
  decisions: 8
  lessons: 5
  patterns: 6
  surprises: 5
missing_artifacts:
  - "15-UAT.md"
---

# Phase 15 Learnings: VitePress-aware Markdown Editor

## Decisions

### Token-API statt Post-Render-Regex für scholarly_fixes
scholarly_fixes wurde als `md.core.ruler.after('linkify', ...)` mit Token-API implementiert, nicht als Post-Render-Regex auf dem fertigen HTML.

**Rationale:** `[[br]]` innerhalb von Tabellenzellen muss nach dem Block-Parsing behandelt werden, nicht davor — sonst entstehen defekte Tabellenzeilen (Pitfall 4 aus RESEARCH.md). Die Token-API erlaubt saubere Hardbreak-Einfügung zwischen Segmenten.
**Source:** 15-01-SUMMARY.md, 15-01-PLAN.md

---

### html_inline-Token für Devanagari-Spans
Devanagari-Spans und `[[indent]]`-Spans werden als `html_inline`-Token eingefügt (direktes HTML-String), nicht als verschachtelte `span_open`/`span_close`-Token-Paare.

**Rationale:** Da `html: true` gesetzt ist, ist `html_inline` einfacher zu warten (kein Token-Nesting erforderlich) und funktional äquivalent zur config.mjs-Implementierung auf Browserseite.
**Source:** 15-01-SUMMARY.md

---

### Kein separater editor-renderer.js
Alles bleibt in `qa_viewer.html` — kein neuer Datei-Output durch das Editor-Renderer-Modul.

**Rationale:** RESEARCH.md Architecture Patterns dokumentiert "no new files required". Single-file HTML-Tools sind wartungsärmer und benötigen keinen Build-Step.
**Source:** 15-01-PLAN.md, 15-01-SUMMARY.md

---

### window.buildRenderer als Brücke zwischen ESM-Modul und klassischem Script
Das buildRenderer()-Modul läuft als `<script type="module">`; der Editor-Tab-Code läuft im klassischen `<script>`-Block. `window.buildRenderer = buildRenderer` am Ende des Modul-Blocks überbrückt die zwei Script-Kontexte.

**Rationale:** ESM-Module haben keinen direkten Zugriff aus klassischen Scripts. Die window-Exposition ist das einzige portable Pattern ohne zusätzliche Bundler.
**Source:** 15-01-PLAN.md, 15-02-SUMMARY.md

---

### Lazy-Initialisierung von window.md in renderPreview()
`window.md` wird nicht beim Seitenload initialisiert, sondern lazy beim ersten Aufruf von `renderPreview()`.

**Rationale:** `window.buildRenderer` steht erst nach dem ESM-Modul-Block zur Verfügung. Ein `type=module`-Block läuft asynchron — direkter Aufruf beim Script-Load würde Race Condition riskieren.
**Source:** 15-02-SUMMARY.md

---

### Kein Save-Button
`loadEditorContent()` lädt Markdown-Dateien read-only per `fetch()` in die Textarea. Es gibt keine Schreib-Funktion.

**Rationale:** CLAUDE.md Hard Rule: `docs/lektionen/` sind unveränderlich. Automatisiertes Schreiben in Quelldateien wäre eine Hard-Rule-Verletzung.
**Source:** 15-02-SUMMARY.md, 15-02-PLAN.md

---

### CSS-Farbe #b22222 statt #ff0000 für .sanskrit-dev
Der Editor-Preview-CSS-Block verwendet `color: #b22222` für `.editor-preview .sanskrit-dev`.

**Rationale:** CLAUDE.md nennt `#ff0000` in der Beschreibung, aber `custom.css` (die maßgebliche CSS-Quelle) verwendet `#b22222` (Scholastic Red). Der tatsächliche Wert in custom.css gewinnt gegenüber der Beschreibung in CLAUDE.md.
**Source:** 15-03-SUMMARY.md

---

### CSS-Scope-Präfix .editor-preview auf allen Container-Regeln
Alle Container-CSS-Regeln im `<style id="editor-preview-styles">`-Block sind mit `.editor-preview`-Präfix gescoped.

**Rationale:** Ohne Scoping würden Container-Styles die gesamte qa_viewer.html-UI (Raw-Viewer, Diff-Tabs) beeinflussen (Pitfall 3 aus RESEARCH.md).
**Source:** 15-03-PLAN.md, 15-03-SUMMARY.md

---

## Lessons

### multimd muss vor allen Container-Plugins registriert werden
Die Registrierungsreihenfolge ist: `prevent_br_link → multimd → 12 Container-Plugins → scholarly_fixes`. multimd darf nicht nach den Container-Plugins registriert werden.

**Context:** Pitfall 2 aus RESEARCH.md. Die Reihenfolge ist identisch zu `docs/.vitepress/config.mjs` und muss exakt eingehalten werden, da die Plugins aufeinander aufbauen.
**Source:** 15-01-PLAN.md, 15-01-SUMMARY.md

---

### Worktree-Pfade müssen explizit verwendet werden
Beim Ausführen von Edits im Worktree muss der absolute Worktree-Pfad angegeben werden, nicht der Haupt-Repo-Pfad.

**Context:** Der erste Edit-Versuch in Plan 15-01 schlug fehl, weil der Pfad auf das Haupt-Repo zeigte statt auf den Worktree unter `/Volumes/.../worktrees/agent-ab43a3da68dea9076/`. Fehler wurde erkannt und korrigiert.
**Source:** 15-01-SUMMARY.md

---

### Worktree-Branches müssen vor Ausführung auf aktuelle main gerebaset werden
Ein Worktree-Branch, der vor mehreren Phase-Commits erstellt wurde, enthält diese Commits nicht automatisch.

**Context:** In Plan 15-03 enthielt der Worktree noch `qa_viewer.html` ohne die Editor-Elemente aus Plan 15-02. Fix: `git rebase b7929ad` auf den letzten merge-Commit von Plan 15-02. Kein Datei-Commit nötig, nur git-Metadaten-Update.
**Source:** 15-03-SUMMARY.md

---

### Plan-Spezifikationen lassen CSS-Details für neue Elemente weg
Wenn ein Plan ein neues HTML-Element einführt (z.B. `div#editor-preview`), fehlen oft die zugehörigen Basis-CSS-Regeln in der Spec.

**Context:** Plan 15-02 spezifizierte CSS nur für `.editor-input`, nicht für `.editor-preview`. Ohne Styling wäre der Preview-Div ohne sichtbaren Hintergrund und Padding geblieben. Erkannt und spontan ergänzt (`.editor-preview` mit display:none/width/height/padding/background).
**Source:** 15-02-SUMMARY.md (Deviation 1)

---

### esm.sh und unpkg.com verhalten sich unterschiedlich für UMD-Pakete
`markdown-it-multimd-table` ließ sich nicht sauber via ESM von esm.sh laden — es wurde auf UMD-Global via unpkg.com (`window.markdownitMultimdTable`) umgestellt.

**Context:** RESEARCH.md hatte ESM-Import via esm.sh für alle drei Pakete vorgesehen. Nur multimd benötigte einen CDN-Wechsel. Fix-Commit `dc3ac02`. Versions-Pinning (@4.2.3) wurde dabei beibehalten.
**Source:** 15-04-SUMMARY.md, 15-VERIFICATION.md (Ergänzende Befunde)

---

## Patterns

### ESM-Import mit gepinnten Versionen in Single-File-HTML-Tools
Für Browser-seitige Markdown-Rendering in einer einzigen HTML-Datei: CDN-Imports mit exakten Versionsnummern (z.B. `esm.sh/markdown-it@14.2.0`).

**When to use:** Wenn ein lokales Werkzeug (kein Build-Step) Markdown-Bibliotheken benötigt, die nicht via npm installiert werden sollen. Versionspinning verhindert silent upgrades durch CDN-Änderungen.
**Source:** 15-01-SUMMARY.md

---

### Token-API für inline-Transformationen in markdown-it
scholarly_fixes-Logik (und ähnliche Inline-Transformationen wie `[[br]]` → hardbreak) als `md.core.ruler.after('linkify', ...)` implementieren — nicht als Post-Render-Regex.

**When to use:** Immer wenn Inline-Transformationen innerhalb von Tabellenzellen oder anderen Block-Strukturen korrekt funktionieren müssen. Post-Render-Regex kann Tabellenstruktur zerbrechen.
**Source:** 15-01-PLAN.md, 15-01-SUMMARY.md

---

### Lazy-Renderer-Initialisierung via window-Global
Schwere Renderer-Objekte (markdown-it-Instanz mit allen Plugins) beim ersten Aufruf initialisieren, nicht beim Seitenload.

**When to use:** Wenn ein ESM-Modul eine Funktion bereitstellt, die von klassischem Script-Code aufgerufen wird. Vermeidet Race Conditions und spart Initialisierungszeit beim Seitenload.
**Source:** 15-02-SUMMARY.md

---

### CSS-Scope-Präfix für Preview-Isolierung
Alle CSS-Regeln für einen Preview-Container mit einem Scope-Präfix (z.B. `.editor-preview .grammar-box`) versehen, nie global.

**When to use:** Wenn Container-Styles (grammar-box, tables etc.) nur innerhalb eines bestimmten Preview-Divs gelten sollen und nicht die umgebende UI beeinflussen dürfen.
**Source:** 15-03-PLAN.md, 15-03-SUMMARY.md

---

### Debounce 300ms für Input-Events auf Markdown-Textareas
`clearTimeout`/`setTimeout(renderPreview, 300)` für `oninput`-Events auf der Editor-Textarea.

**When to use:** Bei jedem Live-Preview-Editor. 300ms ist ausreichend für Tipp-Pausen; kürzere Werte führen zu unnötigen Re-Renders, längere zu spürbarer Latenz.
**Source:** 15-02-SUMMARY.md

---

### 7-Punkt-Integrations-Checkpoint als End-to-End-Gate
Vor Phasenabschluss eine strukturierte Prüfliste mit konkreten visuellen/funktionalen Tests (grammar-box, [[br]] in Tabelle, MultiMD-colspan, Devanagari-Farbe, deleteme-box, Resizer, Dark Mode) durch den User abgenommen.

**When to use:** Bei UI-Features in HTML-Werkzeugen, die nicht automatisiert getestet werden können. Der Checkpoint ersetzt formale Probe-Skripte.
**Source:** 15-04-SUMMARY.md, 15-VERIFICATION.md

---

## Surprises

### multimd ESM-Import schlug fehl — UMD-Fallback via unpkg.com nötig
`markdown-it-multimd-table` ließ sich nicht wie geplant via esm.sh als ESM-Modul laden. Stattdessen musste auf den UMD-Global-Namen `window.markdownitMultimdTable` via unpkg.com ausgewichen werden.

**Impact:** Zusätzlicher Fix-Commit (`dc3ac02`) nötig. RESEARCH.md hatte diesen CDN-Kompatibilitätsfehler nicht antizipiert. Versions-Pinning blieb jedoch intakt.
**Source:** 15-04-SUMMARY.md, 15-VERIFICATION.md

---

### scholarly_fixes war beim ersten Versuch korrekt implementiert
Plan 15-04 Task 1 war ein reiner Verifikations-Pass — keine Korrekturen nötig. Die Token-API-Implementierung aus Plan 15-01 funktionierte bereits korrekt für alle [[br]]-Szenarien inkl. Tabellenzellen.

**Impact:** Positiv: Phase-Abschluss schneller als erwartet. Zeigt, dass die detaillierte Spec in PLAN.md (mit explizitem Verweis auf Pitfall 4) Fehlimplementierungen verhinderte.
**Source:** 15-04-SUMMARY.md

---

### Worktree-Rebase-Bedarf in Plan 15-03 nicht antizipiert
Der Worktree-Branch für Plan 15-03 wurde vor den Plan-15-02-Commits erstellt und enthielt deshalb die Editor-Elemente nicht.

**Impact:** Unerwarteter Aufwand für `git rebase`; kein Datei-Commit nötig, aber Zeitverlust bei der Diagnose. In zukünftigen Phasen: Worktree immer unmittelbar vor Ausführung erstellen oder explizit auf den letzten Commit rebasen.
**Source:** 15-03-SUMMARY.md

---

### Plan 15-02 hatte zwei unspezifizierte CSS/JS-Details
Zwei Abweichungen in Plan 15-02 wurden erst bei der Ausführung entdeckt: (1) fehlende `.editor-preview`-Basis-CSS-Regel, (2) fehlender `_debounceRegistered`-Guard für Event-Listener-Doppelregistrierung.

**Impact:** Beide Lücken wurden während der Ausführung spontan geschlossen. Kein Blocker, aber zeigt, dass Plan-Specs für neue HTML-Elemente oft CSS-Details auslassen.
**Source:** 15-02-SUMMARY.md (Deviations 1 und 2)

---

### Doppelte Event-Listener-Registrierung als implizites Risiko
Der klassische Script-Block enthält sowohl einen `DOMContentLoaded`-Handler als auch eine direkte IIFE — ohne `_debounceRegistered`-Guard würde der Event-Listener doppelt registriert.

**Impact:** Info-Level-Befund (kein Fehler, Guard verhindert das Problem). Zeigt, dass Event-Listener-Management in inkrementell gewachsenen Single-File-Tools sorgfältig dokumentiert werden muss.
**Source:** 15-VERIFICATION.md (Ergänzende Befunde)
