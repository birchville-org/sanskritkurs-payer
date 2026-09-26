# 📐 Entwickler- & Autoren-Richtlinien

## 1. Typografie, Layout & Farbwelt

Das Design des Sanskritkurses orientiert sich an klassischen philologischen Druckwerken, kombiniert mit moderner Web-Ästhetik:

- **Schriftarten:**
  - Fließtext: `Newsreader` (Serifenschrift für optimale Lesbarkeit längerer Grammatikpassagen).
  - Benutzeroberfläche & Navigation: `Inter` (moderne serifenlose Schrift).
- **Farbpalette:**
  - Primärfarbe: `#03192e` (Tiefes Dunkelblau).
  - Hintergrund: `#fcf9f2` (Warmes Elfenbein/Papier-Weiß).
  - Signalrot: `:sig[...]` (Ausdrücklich reserviert für morphologische Devanāgarī-Hervorhebungen).
- **Layout:**
  - 12-Spalten-Raster.
  - Lektionsnummern sind absolut formatiert (z.B. `60.1.`).
  - Keine rohen HTML-Tags im Markdown (`scripts/purge_html.py`).

---

## 2. Sanskrit- & Devanāgarī-Regeln

Um linguistische Verwirrung und visuelle Unruhe auszuschließen, gelten strikte typografische Konventionen:

1. **Keine Kursivschrift:**
   Sanskrit-Wörter und IAST-Transliterationen werden **niemals** kursiv (`*...*`) gesetzt.
2. **Signalrot nur für Devanāgarī:**
   Die Auszeichnung `:sig[...]` darf ausschließlich auf Devanāgarī-Zeichen angewendet werden, keinesfalls auf lateinische Buchstaben.
3. **Schutzklammern:**
   Devanāgarī-Wörter werden in `⟪...⟫` eingeschlossen, um sie vor unbedachten LLM-Übersetzungen zu schützen.
4. **Tabellenformatierung:**
   Keine runden Klammern für Devanāgarī-Text in Tabellenzellen.
   Mehrzeilige Tabellenzellen verwenden `:br` auf einer einzigen Zeile.

---

## 3. Grammatik-Boxen (`grammar-box`)

Grammatische Leitsätze, Flexionstabellen und Erläuterungen folgen einer festen Kapselungshierarchie:

- **Echtes Mirroring der HTML-Einrückung:**
  Tabellen und grammatikalische Definitionen dürfen nicht in Blockquotes (`>`) gepackt werden.
- **Beispiele außerhalb von Boxen:**
  Direkte Rede und illustrative Beispiele stehen **außerhalb** der `grammar-box`. Beispiele werden in `::: indent` formatiert.
- **Box-Verschachtelung:**
  Verschachtelte Boxen inkrementieren die Anzahl der Doppelpunkte:
  ```markdown
  ::: grammar-box
  Hauptregel der Sandhi-Verbindung...
  
  :::: grammar-box
  Ausnahmeregel für vokalische Anlaute...
  ::::
  :::
  ```

---

## 4. QA-Gates & Qualitätssicherung

1. **Totalbremse:**
   Die deutschen Master-Lektionen (`docs/lektionen/*.md`) sowie alle zu 100 % fertiggestellten Sprachen sind schreibgeschützt und dürfen von automatischen Skripten nicht überschrieben werden.
2. **Queue-Wahrheit:**
   Ausschließliche Nutzung von `get_translation_queue` aus `scripts/translation_qa.py`. Keine redundanten Status-Prüfungen.
3. **Verifikations-Gate:**
   Alle Skriptänderungen müssen `python3 -m py_compile` und einen erfolgreichen Testlauf (Exit-Code 0) passieren, bevor sie als abgeschlossen gemeldet werden.
