# 📚 Projekt-Wiki Übersicht

Das offizielle technische Wiki des Projekts **Sanskritkurs Payer** wird als eigenständiges Git-Repository (`payer.wiki`) gepflegt und synchronisiert. Es enthält ausführliche Abhandlungen über die Systemarchitektur, historische Hintergründe und empirische Forschungsergebnisse.

---

## 📑 Wiki-Artikel im Überblick

### 1. [Systemarchitektur & Multi-Node-Topologie](system-architecture.md)
*Original im Wiki: `System-Architecture.md`*  
Umfassende Architekturspezifikation zur Hardware-Aufteilung über drei Knoten (**Workstation: `nike.local`**, **`nyx.local` LLM-Inferenz** und **`nataraja.local` Linux-Server/Runner**), inklusive Mermaid-Netzwerkdiagramm, Staging-Umgebung und Concurrency-Modell.

### 2. [KI-Translationsmethoden & Weg B](ai-translation.md)
*Original im Wiki: `AI-Translation-Methods.md`*  
Detaillierte Dokumentation des 3-Stufen-Modells (Lokales 35B-Modell, Claude Sonnet, Gemini 2.5 Pro), Devanāgarī-Schutzfiltern, Translation-Memory-Hashing und Deadlock-Recovery.

### 3. [Prof. Payers Sanskritkurs — Vision & Erbe](index.md)
*Original im Wiki: `Prof-Payers-Sanskrit-Course.md`*  
Die Entstehungsgeschichte des ursprünglichen Lehrbuchs, die Herausforderungen des 1990er-Web-Codes und der Übergang zur zukunftssicheren VitePress Progressive Web App (PWA).

### 4. [Sprachauswahl & Ausschlusskriterien](languages.md)
*Original im Wiki: `Language-Selection-and-Exclusion-Criteria.md`*  
Quantitative Leistungsdaten aus dem 248,3-Stunden-GPU-Benchmark, Analyse der Engpass-Sprachen (Token-Penalty, Vokabular-Lücken) und das resultierende 3-Stufen-Ausschlussframework.

---

## 🔄 Wiki-Synchronisation

Änderungen an der technischen Dokumentation werden zwischen diesem Dokumentationsportal und dem GitHub-Wiki synchron gehalten.

- **GitHub Wiki:** [github.com/birchville-org/sanskritkurs-payer/wiki](https://github.com/birchville-org/sanskritkurs-payer/wiki)
- **Lokaler Klon:** `/Volumes/SanDisk1TB/proj/payer.wiki`
