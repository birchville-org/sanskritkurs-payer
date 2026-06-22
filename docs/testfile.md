---
title: Markdown Extension Test
---

# Payer Markdown Extension Test

Dieses Dokument demonstriert alle benutzerdefinierten Markdown-Erweiterungen (Container und Inline-Elemente), die im Payer-Projekt konfiguriert sind.

## 1. Inline-Syntax (Neu vs. Alt)

Hier testen wir den Zeilenumbruch und die Einrückungen:

| Syntax | Beispiel in der Tabelle |
| --- | --- |
| Alte Syntax `:br` | Erste Zeile:brZweite Zeile |
| Neue Syntax `:br` | Erste Zeile:brZweite Zeile |
| Alte Syntax `[[indent]]` | Normal:br[[indent]]Eingerückt |
| Neue Syntax `:indent` | Normal:br:indentEingerückt |

## 2. Devanagari Auto-Styling

- **Normales Devanagari (wird automatisch mit einer Klasse versehen):**
  ⟪योगश्चित्तवृत्तिनिरोधः⟫ 
- **Explizit markiertes Sanskrit (mit speziellen Klammern):**
  ⟪योगश्चित्तवृत्तिनिरोधः⟫

## 3. Container-Erweiterungen

:::grammar-box
**Grammatik-Box (`grammar-box`)**
Standard-Container für grammatikalische Erklärungen und Paradigmen.
::::::grammar-box2
**Alternative Grammatik-Box (`grammar-box2`)**
Zweite Variante für Grammatik-Boxen.
::::::media
**Media-Container (`media`)**
Abb.: ⟪चित्रम्⟫
(Bildquelle: [Details](#))
::::::center
**Zentrierter Text (`center`)**
Dieser Text sollte zentriert angezeigt werden.
::::::metrik-schema
**Metrik-Schema (`metrik-schema`)**
⏑ ⏑ ⏑ ⏒
::::::important
**Wichtig (`important`)**
Eine Hervorhebung für besonders wichtige Informationen.
::::::deleteme-box
**Delete-Me-Box (`deleteme-box`)**
Dieser Container wird im Frontend normalerweise unsichtbar gemacht oder enthält Metadaten/Quellen.
::::::note-box
**Notiz (`note-box`)**
Ein Container für Anmerkungen oder Fußnoten.
::::::laut-table
**Laut-Tabelle (`laut-table`)**
Ein Container speziell für Phonetik-Tabellen.
::::::indent
**Einrückung (`indent`)**
Dieser Block sollte komplett als Block eingerückt dargestellt werden (Beispiele etc.).
::::::compact
**Kompakt (`compact`)**
Ein Container mit verringertem Margin/Padding.
::::::grammar-box
:::no-header
| | |
| --- | --- |
| Tabellen in `no-header` | verbergen den Kopfbereich. |
::::::