# Anforderungen (Requirements) - Milestone v1.2

## 1. Sanskrit-Optimierte Suche (SRCH)
- [ ] **SRCH-01**: Implementierung von IAST-Folding in MiniSearch (Normalisierung von Sonderzeichen ā, ś, ṣ zu a, s, s).
- [ ] **SRCH-02**: Lokalisierung der Suche für DE, EN, IT und ES (sprachspezifische Indizes und UI-Texte).

## 2. Thematische Erschließung (INDEX)
- [ ] **INDEX-01**: Automatische Generierung einer Register-Seite (Themen-Index) basierend auf Frontmatter-Tags.
- [ ] **INDEX-02**: Entwicklung einer "Related Lessons" Komponente zur Verknüpfung verwandter Inhalte.

## 3. Internationale Expansion (I18N)
- [ ] **I18N-03**: Einrichtung der italienischen Sprachversion (`/it/`) inkl. Sidebar-Struktur.
- [ ] **I18N-04**: Einrichtung der spanischen Sprachversion (`/es/`) inkl. Sidebar-Struktur.
- [ ] **I18N-05**: Durchführung der Massenübersetzung aller 61 Lektionen/Übungen ins Italienische und Spanische via Ollama-Endpoint (`192.168.1.44:11434/v1`).

## 4. Beta-Kommunikation & Transparenz (BETA)
- [ ] **BETA-01**: Implementierung eines prominenten Beta-Hinweises auf der Startseite aller Sprachversionen.
    - **Inhalt**: Test der KI-Übersetzungsqualität.
    - **Kontakt**: webmaster@birchville.cc
    - **Tech-Info**: Google Antigravity (Gemma 3.1 Flash) & lokale Gemma4:26b (Ollama) auf M4/32 GB.

## Rückverfolgbarkeit (Traceability)

| ID | Beschreibung | Phase | Status |
|----|--------------|-------|--------|
| SRCH-01 | IAST Folding | 10 | Pending |
| SRCH-02 | Search Locales | 10 | Pending |
| INDEX-01 | Themen-Index | 11 | Pending |
| INDEX-02 | Related Lessons | 11 | Pending |
| I18N-03 | Italian Setup | 12 | Pending |
| I18N-04 | Spanish Setup | 12 | Pending |
| I18N-05 | Mass Translation | 12 | Pending |
| BETA-01 | Beta Notice | 12 | Pending |

---
*Historie (v1.1 Anforderungen wurden nach [v1.1-MILESTONE-AUDIT.md](file:///.planning/v1.1-MILESTONE-AUDIT.md) archiviert)*
