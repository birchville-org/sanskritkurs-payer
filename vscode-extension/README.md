# Payer Sanskrit Tools

Eine kleine, hochspezialisierte VSCode-Erweiterung für die Editoren und Maintainer des Payer Sanskritkurs-Projekts.

## Features

Diese Extension rüstet Visual Studio Code mit nativen Snippets für das komplexe Projekt-Markdown (VitePress) aus. Dies erspart Tipparbeit und stellt sicher, dass die Container-Hierarchie nach den AGENTS.md Regeln strikt eingehalten wird.

### Snippets für Markdown-Dateien

Tippe die folgenden Kürzel in eine `.md`-Datei und drücke `Tab`:

- **`sbox`**: Erstellt eine Standard `::: grammar-box` für Regeln und Paradigmen.
- **`sbox4`**: Erstellt eine verschachtelte `:::: grammar-box`, z.B. wenn darin ein weiterer `::: indent` Block platziert wird.
- **`sindent`**: Erstellt einen `::: indent` Block (z.B. für eingerückte Beispiele oder Unter-Vokabulare).
- **`smedia`**: Erstellt einen fertigen `::: media`-Block inklusive Placeholder für Bildpfad und korrekt formatierter Bildquellenangabe.
- **`sdel`**: Erstellt eine `::: deleteme-box` für alte HTML-Metadaten, die später gelöscht werden sollen.
- **`snohead`**: Erstellt einen `::: no-header`-Container, ideal um leere Tabellenköpfe auszublenden.
- **`sred`**: Erstellt ein `sig[...]`-Tag, um Devanāgarī-Schriftzeichen leuchtend rot hervorzuheben, ohne Markdown-Kursivdruck zu missbrauchen.
- **`sbr`**: Setzt einen `<br>`-Ersatz (`:br`) in Tabellenzellen, ohne die Markdown-Tabellenzeile umzubrechen.

## Installation

Diese Extension ist lokal im Repository verlinkt. Um sie in deinem VSCode zu aktivieren:

```bash
# Im Root des Payer-Projekts ausführen:
ln -s $(pwd)/vscode-extension ~/.vscode/extensions/payer-sanskrit-tools
```
Oder verpacke sie per `vsce package` zu einer `.vsix` Datei.

---
*Gebaut gemäß den Projektregeln "The Scholarly Synthesis".*
