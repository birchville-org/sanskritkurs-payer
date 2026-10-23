# Methodik und Standard des Payer-Boxensystems
*Birchville Scholarly Synthesis · Typografie- und Layout-Architektur*

---

## 1. Ausgangsbefund & Historische Quellanalyse

### 1.1. Das HTML-Original von Prof. Alois Payer (`original/*.htm`)
Der historische Ursprung des Lehrgangs (133 HTML-Dateien) wurde zwischen 2000 und 2010 schrittweise verfasst. Die Analyse zeigt, dass Prof. Payer HTML primär als **visuelle Textverarbeitung** (FrontPage) und nicht als semantisches Auszeichnungssystem einsetzte.

| HTML-Konstrukt im Original | Vorkommen | Historische Praxis / Intention |
| :--- | :--- | :--- |
| `<table bgcolor="#FFFFCC">` | 525 | Gelber Kasten für Kernstoff: Regeln, Schemata, Flexionstabellen. |
| `<table border="1">` (ohne Farbe) | 338 | Spontane, unformatierte Tabellen (in späten Lektionen L30–L61 oft Paradigmentabellen). |
| `<table bgcolor="#FFCCCC">` | 38 | Rosa Zellen für einzelne unregelmäßige Formen. |
| `<blockquote>` | > 1.200 | Visuelle Einrückung: Beispiele (`z.B.`), abgesetzte Übersetzungen, Literaturhinweise. |
| `lekt1001.jpg` (Verkehrsschild) | 6 | Dringende didaktische Warnungen (z.B. Passiv-Verbot). |
| `<div align="center">` | > 400 | Zentrierung von Ślokas, Mantras, Bildern und Tabellen. |
| `<font color="#FF0000">` | 487 | Signalrot für grammatische Endungen und Devanāgarī. |

### 1.2. Payer-spezifische Strukturbrüche
1. **Das Flexionstabellen-Paradox:** In L2–L25 wurden Paradigmen als gelbe Tabellen (`#FFFFCC`) angelegt. Ab L30 (z.B. Optativ in L30, Perfekt in L34, Wurzelflexion in L46/L58–L61) wurden identische Flexionsparadigmen als nackte Tabellen ohne Hintergrund eingefügt.
2. **Die Willkür bei Beispielen (`z.B.`):** In L2 stehen von 16 Belegen 3 in gelben Tabellen, 1 in `<blockquote>` und 12 im Fließtext. In L10 stehen 1 in einer gelben Tabelle, 4 in `<blockquote>` und 7 im Fließtext.
3. **1-Zellen-Tabellen als Textmarker:** Zusammengehörige Teilregeln wurden in FrontPage durch mehrfaches Einfügen von 1x1-Tabellen realisiert. Bei der Konvertierung entstanden daraus isolierte, gestapelte Mini-Boxen.
4. **Ad-hoc Einweglösungen:** Für lokale Layoutwünsche erfand Payer temporäre Konstrukte, die bei der Konvertierung zu Einweg-Containern wurden (`laut-table` in L1, `compact` in L32, `metrik-schema` in L53/L54).

---

## 2. Status Quo im VitePress-Markdown (`docs/lektionen/*.md`)

Die quantitative Bestandsaufnahme über alle 136 deutschen Lektionsdateien dokumentiert die Folgen der unbereinigten 1:1-Konvertierung:

| Container | Vorkommen (DE) | Vorkommen (Gesamt) | Bewertung / Defizit |
| :--- | :--- | :--- | :--- |
| `::: grammar-box` | 775 | 36.395 | Häufig fragmentiert; 3–4 Kästen direkt untereinander gestapelt. |
| `::: indent` | 721 | 34.318 | Regelkonform für Beispiele, aber unvollständig genutzt. |
| `::: media` | 662 | 30.986 | Stabil für zentrierte Abbildungen mit Bildlegende. |
| `::: no-header` | 30 | 1.413 | Hilfskonstrukt zum Ausblenden von `thead` bei tabellarischen Daten. |
| `::: note-box` | 26 | 1.314 | Gute Schiefer-Optik, jedoch uneinheitlich befüllt. |
| `::: center` | 14 | 658 | Zwitter: Teils für Verse, teils unnötigerweise um Tabellen gewickelt. |
| `::: metrik-schema` | 14 | 649 | Spezialcontainer für Monospace-Metrik in nur 2 Lektionen. |
| `::: literatur-box` | 7 | 327 | **Defekt:** In `config.mjs` registriert, in `custom.css` ungestylt. |
| `::: important` | 6 | 287 | **Stilbruch:** Grelle violette Box mit rotem SVG-Verkehrsschild. |
| `::: laut-table` | 1 | 47 | **Redundant:** Nur in L1 für `white-space: nowrap`. |
| `::: compact` | 1 | 47 | **Redundant:** Nur in L32 für enge Zeilenhöhe. |
| `::: grammar-box2` | 0 | 0 | **Code-Leiche:** Ungenutzt in CSS/Config. |
| `::: gaga-box` | 0 | 0 | **Code-Leiche:** Ungenutzt in Config. |
| `> blockquote` | 289 Zeilen | – | Regelwidrig für Beispiele, Zitate und Vokabeln genutzt. |

---

## 3. Didaktische Textsorten-Taxonomie

Statt Payers HTML-Artefakte nachzubilden, basiert die Neugestaltung auf den **5 didaktischen Informationsebenen** eines philologischen Lehrwerks:

```
Didaktische Ebenen eines Sanskrit-Lehrgangs
│
├── 1. Normative Grammatik (System)      ──► ::: grammar-box
│      Regeln, Lautgesetze, Paradigmen, Flexionstabellen
│
├── 2. Didaktische Führung (Warnung)     ──► ::: warning-box
│      Interferenz Sanskrit-Deutsch, Übersetzungsverbote, Ausnahmen
│
├── 3. Philologischer Kontext (Apparat)  ──► ::: note-box
│      Realien, Religionsgeschichte, Textnachweise, Literaturzitate
│
├── 4. Primärtext & Metrik (Praxis)      ──► ::: verse-box
│      Ślokas, Mantras, Lektüretexte, Versmaßschemata
│
└── 5. Empirische Belege (Substruktur)   ──► ::: indent
       Eingerückte Beispielsätze, Ableitungen, Formenreihen
```

---

## 4. Das konsolidierte Minimal-Set der Boxen

### 4.1. Semantische Inhalts-Boxen

#### 1. `::: grammar-box` (Normative Grammatik)
* **Zweck:** Verbindliche grammatische Regeln, Bildungsgesetze und Flexionstabellen.
* **Typografie & Farbgebung:**
  * Hintergrund Light: `#fefce8` (Warm Ivory / Hellgelb)
  * Rand Light: 4px Solid `#eab308` (Warm Amber Gold)
  * Hintergrund Dark: `#241500` (Tiefes Umbra)
  * Rand Dark: 4px Solid `#eab308`
* **Gestaltungsregeln:**
  * Mehrere zusammenhängende Teilregeln werden in **einer** Box zusammengefasst.
  * Flexionstabellen stehen **innerhalb** der Box, nicht nackt oder in Hilfscontainern.

#### 2. `::: warning-box` (Didaktische Warnung)
* **Zweck:** Signalisierung von Interferenzfehlern, Übersetzungsverboten und gefährlichen Stolperfallen.
* **Typografie & Farbgebung:**
  * Hintergrund Light: `#fff7ed` (Warm Peach)
  * Rand Light: 4px Solid `#ea580c` (Scholarly Terracotta / Rostrot)
  * Hintergrund Dark: `#361e04`
  * Rand Dark: 4px Solid `#ea580c`
  * Text: Primäre Schriftfarbe, kein grelles Lila, kein SVG-Verkehrszeichen.
* **Gestaltungsregeln:**
  * Wird extrem sparsam dosiert (nur bei echten didaktischen Veto-Hinweisen).

#### 3. `::: note-box` (Philologischer & Kultureller Apparat)
* **Zweck:** Realienkunde (Kastenwesen, Gottheiten, Rituale), Zitate historischer Philologen, Buchempfehlungen und Literaturangaben.
* **Typografie & Farbgebung:**
  * Hintergrund Light: `rgba(72, 98, 110, 0.04)` (Dezentes Schiefer)
  * Rand Light: 3px Solid `#475569` (Slate Navy)
  * Hintergrund Dark: `rgba(232, 224, 211, 0.04)`
  * Rand Dark: 3px Solid `#64748b`
  * Schriftgröße: 0.95–1.0rem (leicht zurückhaltender Leseton).
* **Gestaltungsregeln:**
  * Ersetzt die ungestylte `literatur-box` sowie freischwebende `> blockquote`-Zitate.

#### 4. `::: verse-box` (Sanskrit-Primärtext & Metrik)
* **Zweck:** Sakrale Sprüche, Mantras, Ślokas, metrische Schemata und zusammenhängende Lesetexte.
* **Typografie & Farbgebung:**
  * Zentrierter oder rhythmisch abgesetzter Block.
  * Optimierte Zeilenhöhe (1.5) für Devanāgarī mit Signalrot, IAST-Transliteration und Versübersetzung.
* **Gestaltungsregeln:**
  * Ersetzt `::: center` bei Texten, `::: compact` (L32) und `::: metrik-schema` (L53/54).

---

### 4.2. Strukturelle Hilfs-Container

#### 5. `::: indent` (Strukturierte Einrückung)
* **Zweck:** Unmittelbar unter einer Regel stehende Belege, Einzelformen, Ableitungen und Unterlisten.
* **Eigenschaften:** Kein Rahmen, reiner linker Einzug (`padding-left: 2.5rem`), vertikales Rhythmus-Kompaktmaß.

#### 6. `::: media` (Multimediale Abbildungen)
* **Zweck:** Vollständige Kapselung von Bild, Legende und Lizenznachweis.
* **Eigenschaften:** Zentrierte Flexbox-Spalte mit Bildunterschrift in 0.95rem Slate.

---

## 5. Bereinigungs- und Migrationsregeln

1. **Eliminierung redundanter Container:**
   * `literatur-box` → `::: note-box`
   * `laut-table` → Standard-Markdown-Tabelle
   * `compact` → `::: verse-box` oder Standardabsatz
   * `metrik-schema` → `::: verse-box` mit Monospace-Auszeichnung
   * `center` (um Tabellen) → Entfällt, Tabellen wandern direkt in `grammar-box`
   * `grammar-box2` und `gaga-box` → Aus Codebase löschen
2. **Tabellen-Konsolidierung:** Jedes Paradigma gehört zwingend in eine `grammar-box`. Nackte Flexionstabellen aus L30–L61 werden nachqualifiziert.
3. **Blockquote-Bereinigung:** `> blockquote` wird nicht mehr für Beispielsätze genutzt (dafür gilt `::: indent`).
4. **Schutz des Produktivbestands:** Bestehende Sprachversionen und das Original unter `docs/lektionen/*.md` unterliegen der `TOTALBREMSE` und dürfen erst nach erfolgreicher Staging-Validierung migriert werden.

---

## 6. Unantastbarkeit der Lehrgangsinhalte (Integritätsgebot)

1. **Absoluter Inhalts- und Textschutz:**
   * Der Text von Prof. Alois Payer (inklusive sämtlicher Realien, kulturhistorischer Exkurse wie Max Weber oder der europäischen Ständeordnung, Zitate, philologischer Nachweise, vollständiger Vokabellisten und aller Übungsaufgaben) ist zu **100 % unverändert zu erhalten**.
2. **Reine Struktur- und Formtransformation:**
   * Die Straffung der grafischen Mittel und das Minimal-Set der Markdown-Boxen dienen ausschließlich der **semantischen Kapselung, Leseführung und typografischen Eleganz**.
   * Eine inhaltliche Straffung, Textkürzung, Zusammenfassung oder Paraphrasierung von Payers Originaltext ist **strikt unzulässig**.
3. **Strenger Genehmigungsprozess für inhaltliche Straffungen (Opt-in Gate):**
   * Sollten sich im Einzelfall gut begründete Anlässe für eine inhaltliche Straffung, Bereinigung oder Korrektur ergeben (z. B. redundante Doppelungen, obsolete Links, nachweisliche Fehler):
   * **Keine autonome Umsetzung:** Der Agent darf keinerlei inhaltliche Kürzungen selbstständig vornehmen.
   * **Explizite Vorlagepflicht:** Jede vorgeschlagene Textänderung muss dem Benutzer als einzelnes Proposal mit Begründung, Vorher/Nachher-Diff und Relevanzbewertung für die Übersetzung vorgelegt werden.
   * **Explizite Freigabe erforderlich:** Erst nach ausdrücklicher Genehmigung durch den Benutzer darf eine Änderung in den Staging-Bestand einfließen.
4. **Propagierbarkeit auf Zielsprachen (Keine Neuübersetzungen):**
   * Das Lehrwerk existiert in zahlreichen Sprachversionen und aktiven Übersetzungspipelines.
   * Die Renovierung der Website dient der strukturellen und visuellen Modernisierung. Die neue Container-Struktur soll automatisiert auf alle anderen Sprachen übertragen werden können.
   * Voraussetzung hierfür ist absolute Text- und Segmenttreue im deutschen Original: Da der Inhalt unangetastet bleibt, bleibt der Translation-Memory- und Übersetzungsbestand intakt und es werden **keinerlei Neuübersetzungen** ausgelöst.
