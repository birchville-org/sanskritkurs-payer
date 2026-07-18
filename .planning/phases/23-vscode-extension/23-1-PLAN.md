# Plan 23-1: VSCode Extension (Payer Markdown) [Status: Complete]

## Goal
Entwicklung einer projektspezifischen VSCode Extension (`vscode-payer-markdown`), die als Template für selbstdefinierte Markdown Extensions dient. Die Extension klinkt sich in den Standard-Markdown-Parser von VSCode ein und liefert Syntax-Highlighting, Snippets und (in Stufe 2) Preview-Rendering für die Payer-spezifischen Elemente.

## Scope (Milestone v1.6)

### Stufe 1: Syntax Highlighting & Snippets
Die Extension besteht aus einem neuen Ordner im Root-Verzeichnis: `/vscode-payer-markdown/`.

1. **Extension Gerüst**
   - `package.json`: Definiert die Extension, Contribution Points für Grammatiken (`contributes.grammars`) und Snippets (`contributes.snippets`).

2. **Syntax Highlighting (TextMate Grammar)**
   - `syntaxes/payer-markdown.tmLanguage.json`:
     Injected neue Regeln in die Standard `text.html.markdown` Grammatik von VSCode:
     - **Container**: Erkennt `::: grammar-box`, `::: media`, `::: deleteme-box`, `::: indent` etc. und färbt die Tags als Keywords ein.
     - **Inline**: Erkennt `⟪...⟫` (färbt es als speziellen Entity/Markup-String) und `sig[...]` (als rot/wichtig).
     - **Table Breaks**: Erkennt `:br` als Control-Keyword.

3. **Autocomplete Snippets**
   - `snippets/markdown.json`:
     Erlaubt extrem schnelles Tippen:
     - `gbox` + Tab ➔ `::: grammar-box \n ... \n :::`
     - `media` + Tab ➔ `::: media \n ![Caption](path) \n :::`
     - `delbox` + Tab ➔ `::: deleteme-box \n ... \n :::`
     - `table` + Tab ➔ Generiert eine saubere MultiMD-Tabelle mit Header-Skip.

### Stufe 2: Preview Rendering (Erweitert)
- Integration von `markdown-it` Plugins in den nativen VSCode-Preview (via `markdown.markdownItPlugins` Contribution Point).
- Sicherstellen, dass die VitePress Container auch im VSCode Vorschaufenster korrekt gerendert werden, um den "Payer QA Viewer" als Extension zur Verfügung zu stellen.

## Verification Plan
1. Die Extension wird lokal im Projekt-Verzeichnis unter `/vscode-payer-markdown` entwickelt.
2. Build der Extension via `npx vsce package`.
3. Installation der `.vsix` in VSCode.
4. Manuelle Prüfung in einer Payer-Lektion (z.B. `lektion01.md`), dass Syntax-Highlighting greift, Snippets triggern und die Live-Vorschau (Stufe 2) funktioniert.
