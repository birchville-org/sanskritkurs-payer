# Migration & Structural Fidelity Guide: The Payer Method

> [!IMPORTANT]
> Dieses Dokument definiert die Regeln für die Transformation von Alois Payers HTML-Originalen in das "Gold Standard" VitePress-Markdown. Ziel ist die Erschaffung des "Illuminated Manuscript of the Future" bei absoluter inhaltlicher Parität.

## 1. Das "Zero-Omission" Protokoll (Audit-Verfahren)

Um das Übersehen von Texten oder Boxen (wie in Lektion 12 geschehen) zu verhindern, ist bei jeder Migration folgendes Verfahren zwingend:

1.  **Full Source Slurping**: Es wird grundsätzlich die **gesamte** HTML-Quelle eingelesen (`cat`), bevor mit der Migration begonnen wird. Die Arbeit mit Ausschnitten (`sed`, `head`) ist nur für Detailkorrekturen zulässig.
2.  **Top-Down Sequential Verification**: Die Migration erfolgt strikt von Zeile 1 bis zum Ende. Jeder Paragraph (`<p>`), jede Liste (`<ul>`) und jede Tabelle (`<table>`) muss im Markdown eine Entsprechung finden.
3.  **Meta-Text & Footer Audit**:
    - **Intro**: Texte *vor* der ersten H1-Überschrift (Einführungen, Vorbemerkungen) müssen in das MD übernommen werden.
    - **Footer**: Verweise auf Folgelektionen oder abschließende Notizen am Ende der Datei dürfen nicht weggelassen werden.
4.  **Verification Loop**: Nach der Migration muss im `qa_viewer.html` ein visueller Abgleich (Side-by-Side) durchgeführt werden. Ein Springen oder Auseinanderlaufen der Seiten deutet auf strukturelle Lücken hin.

## 2. Strukturelles Mapping (HTML -> Markdown)

Das Design-System nutzt CSS-Klassen statt Borders. Folgende Zuordnungen sind verbindlich:

| HTML Element / Stil | VitePress Container | Rationale |
| :--- | :--- | :--- |
| Gelbe Hintergrundboxen (`bgcolor="#FFFFCC"`) | `:::: grammar-box` | Didaktische Kerninhalte und Regeln. |
| Zentrierte Bilder mit Bildunterschrift | `::: media` | Konsolidierung von Bild und Metadaten. |
| Zentrierte Texte / Überschriften | `::: center` | Layout-Treue ohne HTML-Tags. |
| Violette / Wichtige Hinweise | `::: important` | Hervorhebung pädagogischer Schwerpunkte. |
| Metadaten / Zitierweise | `::: deleteme-box` | Maschinenlesbar, aber im Frontend ausgeblendet. |

## 3. Tabellen-Konventionen

In Abweichung von einfachen Listen im Original sind für Grammatik-Inhalte **Markdown-Tabellen** zwingend erforderlich, wenn:
- Lautgesetze (Sandhi) erklärt werden.
- Verb-Paradigmen oder Stammbildungen gelistet werden.
- Vergleiche zwischen verschiedenen Formen (z.B. aniṭ/seṭ) gezogen werden.

**Regel**: Wenn das Original eine HTML-Tabelle nutzt, muss das MD eine Markdown-Tabelle nutzen. Eine Umwandlung in einfache Listen ist eine "unzulässige Verkürzung".

## 4. Nummerierung & Konsistenz

1.  **Absolute Nummerierung**: Jede Überschrift muss das Lektions-Präfix tragen (z.B. `12.1.`, `12.1.1.`).
2.  **Überschriften-Cleaning**: Original-Überschriften wie "4. Lektion 4" werden in "4. Lektion" (bzw. `X.Y. Titel`) umgewandelt. Die didaktische Hierarchie bleibt erhalten.
3.  **Keine Redundanz**: Das "Inhaltsverzeichnis" am Anfang einer Lektion wird weggelassen, da die VitePress-Sidebar diese Funktion übernimmt.

## 5. Typografie & Skript-Handling

- **Sanskrit (Devanāgarī)**: Muss immer in Unicode vorliegen. Das automatische Rendering sorgt für das "Scholarly Red" Styling.
- **Transliteration (IAST)**: Muss präzise nach den wissenschaftlichen Standards (Newsreader Italic) gesetzt werden.
- **Whitespace**: Abstände sind ein Gestaltungsmittel. "Pompöse" Leerflächen sind zu vermeiden, aber die Trennung von Gedankengängen durch horizontale Linien (`---`) ist erwünscht.

### 5. Integrity Checklist (Mandatory)

Bevor eine Lektion als "Gold Standard" deklariert wird, MÜSSEN folgende Prüfungen durchgeführt werden:

1.  **Element-Zählung**: Stimmt die Anzahl der Bilder (`media`-Blöcke) und der `grammar-boxen` exakt mit der HTML-Quelle überein?
2.  **Verbal-Audit**: Wurden alle Verben in Wortlisten und Tabellen (1. und letzte Spalte) stichprobenartig gegen das HTML-Grep geprüft?
3.  **Cross-Check Halluzinationen**: Wurden Begriffe, die nicht im Original-HTML vorkommen, versehentlich eingefügt (z.B. durch KI-Vorwissen)?
4.  **Browser-Verifikation**: Der QA-Viewer muss genutzt werden, um Omissionen in Listen und Tabellen visuell zu bestätigen.
5.  **Null-HTML-Check**: Ein finaler `grep "<"` im Markdown darf keine Legacy-Tags (außer erlaubten Containern) finden.
