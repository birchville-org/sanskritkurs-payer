# Release Notes — v1.6 «Surgical Fallback & Integrity»

**Veröffentlicht:** 2026-07-13  
**Vorherige Version:** v1.5.0  

---

## 🛠 Chirurgische Fallback-Reparaturen & Stabilität

In diesem Release lag der absolute Fokus auf der Ausfallsicherheit der massiven KI-Übersetzungen und der Datenintegrität über alle unterstützten Sprachen hinweg.

**Lückenlose Vervollständigung (100% Coverage)**  
Alle bisherigen Übersetzungs-Jobs (Indonesisch, Hindi, Tamil, Arabisch und Vereinfachtes Chinesisch) wurden systematisch auf stehengebliebene `<!-- TODO: Fallback translation -->` Tags durchleuchtet.
- Das Übersetzungsskript wurde mit einer **chirurgischen Fallback-Logik (Stufe 2)** ausgestattet, welche riesige Dateien (wie die massive `wortliste.md` oder das `glossar.md` mit teilweise über 5.000 Token pro Block) exakt Block-für-Block neu übersetzt, sobald in der globalen Übersetzung Lücken entstanden sind.
- Die Ausführung dieser Mega-Blöcke lief extrem stabil auf dem dedizierten lokalen Mac-Server (`nyx.local`) bei Geschwindigkeiten von durchgehend ~22 Token pro Sekunde.

**Ergebnis:**
- Indonesisch (ID), Hindi (HI), Tamil (TA), Arabisch (AR) und Vereinfachtes Chinesisch (zh-CN) stehen nun in sämtlichen 61 Lektionen, 11 Schriften, 61 Übungen und den 4 Root-Dateien bei echten **✅ 100%**. 

*(Anmerkung: Die Sprachen Thai, Griechisch und Koptisch sind für ein kommendes Release v1.7 vorgesehen und bleiben vorerst noch pausiert.)*

---

## 💻 QA & Architektur

- **Payer QA Mode Integrity:** Der QA-Mode (`qa_viewer.html`) wurde erfolgreich durch Build-Eingriffe in der `config.mjs` vor der Auslieferung geschützt, sodass keine ungewollten Zugriffe auf den Editor im Produktions-Build (z.B. auf `payer.birchville.org`) möglich sind.
- Die VitePress-Build-Pipeline läuft nun fehlerfrei über die absolut synchronisierten und validierten Markdown-Dateien aller freigeschalteten Locales.
