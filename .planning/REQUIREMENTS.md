# Anforderungen (Requirements) - Milestone v1.3

## 1. VitePress-aware Markdown Editor (EDIT) ⭐ PRIORITY
- [x] **EDIT-01**: Client-seitiger Markdown-Renderer mit markdown-it + VitePress-Container-Plugins (grammar-box, indent, deleteme-box, media, no-header).
- [x] **EDIT-02**: Split-Pane UI: Editor (CodeMirror/Textarea) links, Live-Vorschau rechts.
- [x] **EDIT-03**: `[[br]]` Line-Break-Substitution im Renderer.
- [x] **EDIT-04**: MultiMD-Table-Rendering (markdown-it-multimd-table).
- [x] **EDIT-05**: Integration in QA-Viewer (`qa_viewer.html`) als eigener Tab/Modus.

## 2. Internationale Expansion (I18N) — sekundär
- [ ] **I18N-06**: Einrichtung der spanischen Sprachversion (`/es/`) inkl. Sidebar-Struktur.
- [ ] **I18N-07**: Einrichtung der lateinischen Sprachversion (`/la/`) inkl. Sidebar-Struktur.
- [ ] **I18N-08**: Einrichtung der rätoromanischen Sprachversion (`/rm/`) inkl. Sidebar-Struktur.
- [ ] **I18N-09**: Einrichtung der tamilischen Sprachversion (`/ta/`) inkl. Sidebar-Struktur.
- [ ] **I18N-10**: Massenübersetzung aller 61 Lektionen via lan_translate.py → nyx.local:8000.
- [ ] **I18N-11**: Einrichtung der Punjabi-Sprachversion (`/pa/`) inkl. Gurmukhi-Locale und Sidebar-Struktur.

## 3. Scholarly Polish & Developer Tools (POLISH) — sekundär
- [ ] **POLISH-01**: Standardisierung aller Bildunterschriften auf L16-Ref Format (einzeilig, Devanāgarī, Lizenzlink).
- [ ] **POLISH-02**: Vollständiges Audit der licenses.md für alle 61 Lektionen.
- [ ] **POLISH-03**: Historical Comparison Mode — Side-by-Side Legacy-HTML vs Modern-Markdown im QA-Viewer.

## Rückverfolgbarkeit (Traceability)

| ID | Beschreibung | Phase | Status |
|----|--------------|-------|--------|
| EDIT-01 | Client Renderer | 15 | Done |
| EDIT-02 | Split-Pane UI | 15 | Done |
| EDIT-03 | [[br]] Handling | 15 | Done |
| EDIT-04 | MultiMD Tables | 15 | Done |
| EDIT-05 | QA-Viewer Integration | 15 | Done |
| I18N-06 | Spanish Setup | 16 | Pending |
| I18N-07 | Latin Setup | 16 | Pending |
| I18N-08 | Romansh Setup | 16 | Pending |
| I18N-09 | Tamil Setup | 16 | Pending |
| I18N-10 | Mass Translation | 16 | Pending |
| I18N-11 | Punjabi Setup | 12 | Pending |
| POLISH-01 | Image Captions | 17 | Pending |
| POLISH-02 | License Audit | 17 | Pending |
| POLISH-03 | Comparison Mode | 17 | Pending |

---
*Historie (v1.2 Anforderungen wurden mit Milestone-Abschluss am 2026-05-27 erfüllt)*
