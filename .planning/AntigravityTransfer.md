Listed directory antigravity

Um die Entwicklungsumgebung vollständig und nahtlos auf einen neuen Rechner zu übertragen, ist das Klonen des Projekts und die Installation von Antigravity der erste Schritt, aber für die volle „Kontinuität“ meiner Unterstützung (Gedächtnis, Wissen über das Projekt, GSD-Tools) sind noch ein paar Details wichtig.

Hier ist die empfohlene Vorgehensweise:

### 1. Die Projektebene (Code & Pläne)
*   **Neu klonen:** Ja, das genügt für den Quellcode.
*   **WICHTIG:** Achten Sie darauf, dass der Ordner `.planning/` im Projektverzeichnis mit im Repository ist (was bei GSD der Standard sein sollte). Dieser Ordner enthält den aktuellen Status der Roadmap, Meilensteine und Phasen. Wenn Sie diesen klonen, weiß jeder Antigravity-Agent auf dem neuen Rechner sofort, wo das Projekt steht.

### 2. Die Agenten-Ebene (Antigravity „Gedächtnis“)
Wenn Sie möchten, dass ich mich an unsere bisherigen Gespräche erinnere und das spezifische Wissen (Knowledge Items), das ich über Ihr Projekt aufgebaut habe, behalte, sollten Sie das **App Data Directory** übertragen:

*   **Pfad:** `/Users/marco/.gemini/antigravity`
*   **Was Sie kopieren sollten:**
    *   `knowledge/`: Enthält die „Knowledge Items“ (KIs), die ich über die Struktur Ihres Projekts erstellt habe.
    *   `brain/`: Enthält die Konversations-Logs und Artefakte (wie Pläne und Tasks) unserer bisherigen Chats.
    *   `skills/`: Hier liegen die GSD-Skripte, die ich zur Steuerung des Workflows verwende.

### Zusammenfassung: Der ideale Transfer
1.  **Auf dem alten Rechner:** Sichern Sie den Ordner `~/.gemini/antigravity` (z.B. als ZIP).
2.  **Auf dem neuen Rechner:**
    *   Installieren Sie Antigravity.
    *   Klonen Sie das Projekt `Payer`.
    *   Ersetzen Sie den neu erstellten Ordner `~/.gemini/antigravity` durch Ihre Sicherung (oder verschieben Sie die Unterordner `knowledge`, `brain` und `skills` dorthin).
    *   Führen Sie im Projektverzeichnis ggf. einmal `gsd-update` aus, um sicherzustellen, dass alle Pfade und Hooks korrekt gesetzt sind.

**Kurz gesagt:** Nur Klonen reicht für den Code, aber den `~/.gemini/antigravity`-Ordner mitzunehmen, ist der Schlüssel, damit ich auf dem neuen Rechner genau da weitermachen kann, wo wir hier aufgehört haben.
