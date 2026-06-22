# Guide für Co-Autoren (Cheat-Sheet)

Dieses Dokument hilft dabei, Inhalte für den Sanskritkurs korrekt zu erstellen, damit sie auf der Webseite richtig angezeigt werden.

## 1. Special-Boxen (Custom Container)
Um bestimmte Inhalte hervorzuheben, nutzen wir "Container". Diese beginnen und enden immer mit drei Doppelpunkten `:::`.

| Container | Zweck | Beispiel |
| :--- | :--- | :--- |
| `::: center` | Zentriert den Text (z.B. für Verse) | `::: center`<br>`Sanskrit-Text`<br>`Übersetzung`<br>`:::` |
| `::: media` | Bilder mit Bildunterschrift | `::: media`<br>`![](/images/bild.jpg)`<br>`Abb.: Beschreibung des Bildes`<br>`:::` |
| `::: grammar-box` | Für Grammatikregeln und Tabellen | `::: grammar-box`<br>**Regel:** Das Verb steht am Ende...<br>`:::` |
| `::: note-box` | Für längere Anmerkungen oder Zitate | `::: note-box`<br>`Hier steht ein interessanter Fakt...`<br>`:::` |
| `::: laut-table` | Spezielle Tabellen für die Aussprache | `::: laut-table`<br>`| Laut | Beschreibung |`<br>`| :--- | :--- |`<br>`:::` |
| `::: tip` | Kurze Tipps oder wichtige Hinweise | `::: tip Titel`<br>`Kleine Hilfe zwischendurch...`<br>`:::` |

---

## 2. Sanskrit-Eingabe
Du musst keine speziellen Codes verwenden, um Sanskrit-Zeichen darzustellen.

- **Devanagari:** Schreibe die Zeichen einfach direkt (z.B. `⟪अ⟫`, `Sanskrit-Wörter`). Das System erkennt sie automatisch und formatiert sie korrekt.
- **Umschrift (IAST):** Nutze für die wissenschaftliche Umschrift die korrekten Sonderzeichen (Diakritika), zum Beispiel: `ā`, `ī`, `ū`, `ṛ`, `ṝ`, `ḷ`, `ṁ`, `ṃ`, `ḥ`, `ṅ`, `ñ`, `ṭ`, `ḍ`, `ṇ`, `ś`, `ṣ`.

---

## 3. Kopfzeilen (Frontmatter)
Jede Datei beginnt mit einem Block zwischen zwei `---`. Dieser Block steuert, wie die Seite im Menü erscheint.

**Beispiel für eine Lektion:**
```markdown
---
title: Lektion 1
subtitle: "Die Laute des Sanskrit"
lesson_id: 1
category: "Grammatik"
status: "stable"
last_reconstructed: 2026-04-30
---
```
- **Pflicht:** `title` (Titel der Seite).
- **Optional:** `subtitle` (Untertitel), `lesson_id` (Nummer der Lektion), `category` (Kategorie), `status` (z.B. "stable" oder "draft").

---

## 4. Mehrsprachigkeit
Die Dateien sind nach Sprachen in Ordnern organisiert. Wenn du eine Lektion übersetzt, lege die Datei in den entsprechenden Sprachordner:

- **Deutsch (Hauptsprache):** `docs/lektionen/`
- **Englisch:** `docs/en/lektionen/`
- **Spanisch:** `docs/es/lektionen/`
- **Italienisch:** `docs/it/lektionen/`
- **Bulgarisch:** `docs/bg/lektionen/`
- **Russisch:** `docs/ru/lektionen/`
- **Ukrainisch:** `docs/uk/lektionen/`

---

## 5. Tabellen-Syntax
Wir verwenden ein erweitertes Tabellen-Format. Besonders wichtig ist der Zeilenumbruch innerhalb einer Zelle.

- **Zeilenumbruch in Zellen:** Nutze `:br`, um innerhalb einer Tabellenzelle eine neue Zeile zu beginnen.
- **Beispiel:**
```markdown
| Begriff | Erklärung |
| :--- | :--- |
| **Sanskrit** | Eine alte Sprache:braus Indien. |
| **Veda** | Die heiligen:brSchriften. |
```

---

## 6. Häufige Fehler (Vermeidung)
- **Container nicht schließen:** Achte darauf, dass jede Box, die mit `::: name` beginnt, auch mit `:::` am Ende geschlossen wird.
- **Falscher Ordner:** Prüfe genau, ob du dich im richtigen Sprachordner befindest (z.B. `/en/lektionen/` statt `/lektionen/`).
- **Einfache Umbrüche in Tabellen:** Drücke in Tabellenzellen nicht einfach die Enter-Taste, sondern nutze immer `:br`.
- **Frontmatter löschen:** Die `---` Blöcke am Anfang der Datei dürfen nicht entfernt werden, da sonst die Seite im Menü verschwindet.
