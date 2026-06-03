# Release Notes — v1.3 «Polyglot & Polish»

**Veröffentlicht:** 2026-06-03  
**Vorherige Version:** v1.2 (2026-05-27)  
**Phasen:** 15–17

---

## Markdown-Editor mit Live-Vorschau (Phase 15)

**Split-Pane-Editor im QA-Viewer**  
Der QA-Viewer erhält einen vollständigen Markdown-Editor mit Live-Vorschau. Der Editor rendert alle VitePress-Container (`grammar-box`, `indent`, `center`, `media` u.a.) 1:1 wie der Produktions-Build — inklusive `[[br]]`-Zeilenumbrüche und MultiMD-Tabellen mit Colspan/Rowspan.

**Syntax-Panel**  
Eine dritte Spalte links zeigt eine klickbare Referenz aller unterstützten Markdown-Konstrukte. Beschriftungen passen sich automatisch an die gewählte Sprache des rechten Panels an (14 Sprachen).

**File System Access API**  
Dateien können direkt aus dem Dateisystem geöffnet und nach Bearbeitung gespeichert werden. Beim Speichern erscheint ein Toast mit Hinweis an `webmaster@birchville.cc`.

**SWAP / END QA**  
Zwei neue Buttons tauschen linkes und rechtes Panel (SWAP) bzw. kehren zur zuletzt geöffneten Lektion zurück (END QA). Der QA-Modus merkt sich Lektion und Sprache aus dem Referrer.

---

## 5 neue Sprachen (Phase 16)

**Latein (LA), Rumantsch Grischun (RM), Rumänisch (RO), Punjabi (PA)**  
Vier neue Sprachen wurden vollständig übersetzt: alle 61 Lektionen, 11 Schrift-Einführungen und 61 Übungen, je mit Wortliste, Inhaltsverzeichnis und Glossar. Damit bietet der Kurs nun **14 Sprachen**.

| Sprache | Code | Schrift |
|---------|------|---------|
| Latein | LA | Lateinisch |
| Rumantsch Grischun | RM | Lateinisch |
| Rumänisch | RO | Lateinisch |
| Punjabi | PA | Gurmukhi |

**Übersetzungs-Pipeline verbessert**  
- HTTP-Fallback via `subprocess curl` behebt macOS-Homebrew-Python-Netzwerkfehler
- `NoneType`-Crash bei erschöpften Devanāgarī-Platzhaltern behoben
- Automatisches Unescape von Vue-Komponenten-Tags (`<PayerTopicIndex />`) nach LLM-Übersetzung

---

## Glossar (Phase 16)

**Alphabetisches Sanskrit-Glossar in allen 14 Sprachen**  
`scripts/gen_glossar.py` generiert aus den Wortlisten aller Lektionen ein alphabetisches Glossar mit 551 Einträgen (L2–L52). Jeder IAST-Eintrag verlinkt direkt ins [Monier-Williams Wörterbuch 1899](https://www.sanskrit-lexicon.uni-koeln.de/).

---

## Qualitätssicherung (Phase 12 + 17)

**Pre-Push-Check (`scripts/pre_push_check.py`)**  
Automatische Qualitätsprüfung vor jedem Push:
- YAML-Frontmatter-Validierung
- Zero-HTML-Policy
- Escapte Vue-Komponenten (neu)
- Übersetzungsplatzhalter (`DEVA_`, `TODO`)
- CJK- und Kyrillisch-Zeichen in falschen Sprachen
- Bildunterschriften-Format
- Lizenzvollständigkeit aller Sprachen (neu)

**Monitor-Status-Script (`scripts/monitor_status.py`)**  
Zeigt auf einen Blick Übersetzungsstand aller 14 Sprachen + GSD-Phasenstatus mit Timestamp.

**Grammatik-Links korrigiert**  
Alle internen Links in `grammatik.md` aller 13 übersetzten Sprachen zeigen nun auf die sprachspezifischen Lektionen (780 Links korrigiert).

**Themenregister-Links korrigiert**  
`PayerTopicIndex`-Komponente erkennt die aktuelle Sprache via `useRoute().path` und generiert sprachspezifische Links. `PayerRelatedLessons` deckt nun alle 14 Sprachen ab (bisher nur 4).

---

## Lizenz

**Dual-Lizenz eingeführt:**
- Code/Pipeline: [MIT License](LICENSE)
- KI-Übersetzungen: [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/)
- Originaltext: © Alois Payer (alle Rechte vorbehalten)

---

## Bruch mit v1.2

- `PayerRelatedLessons` dekekte bisher nur 4 Sprachen korrekt; alle anderen landeten auf deutschen Lektionen. **Bestehende Bookmarks auf übersetzte Lektionen sind weiterhin gültig.**
- `grammatik.md` in allen 13 Übersetzungssprachen hatte 780 falsche interne Links (auf DE statt Zielsprache). Behoben in v1.3.
