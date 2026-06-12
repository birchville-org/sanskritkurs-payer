---
phase: 18-pwa-offline-app
plan: 01
type: execute
wave: 1
depends_on: []
files_modified:
  - docs/public/manifest.json
  - docs/public/pwa-icons/
autonomous: true

must_haves:
  truths:
    - "manifest.json ist valide gemäss W3C Web App Manifest Spezifikation"
    - "Alle Pflichtfelder vorhanden: name, short_name, start_url, display, theme_color, background_color, icons"
    - "icons enthält 192x192, 256x256, 384x384, 512x512 (purpose: any+maskable)"
    - "start_url ist '/'"
    - "display ist 'standalone'"
  artifacts:
    - path: "docs/public/manifest.json"
      provides: "Web App Manifest für PWA-Installation"
      contains: "name, short_name, start_url, icons, theme_color"
---

<objective>
Web App Manifest und PWA-Icons erstellen.

Purpose: Das Manifest definiert App-Name, Icons, Start-URL, Farben und Display-Modus.
Ohne dieses File kann die App nicht als PWA installiert werden.

Output: Valides manifest.json + 4 PNG-Icons in docs/public/pwa-icons/.
</objective>

<context>
VitePress kopiert alles in docs/public/ 1:1 in den Build-Output.
manifest.json wird unter /manifest.json erreichbar sein.
Icons werden unter /pwa-icons/icon-192.png etc. erreichbar sein.

Farben aus Design System (AGENTS.md):
- theme_color: #03192e (Deep Ink — Primary)
- background_color: #fcf9f2 (Parchment)
</context>

<tasks>

<task type="auto">
  <name>Task 1: PWA-Icons generieren</name>
  <files>docs/public/pwa-icons/</files>
  <action>
    Erstelle docs/public/pwa-icons/ Verzeichnis.
    Generiere 4 PNG-Icons mit image_generate oder Canvas-Script:
    - icon-192.png (192x192)
    - icon-256.png (256x256)
    - icon-384.png (384x384)
    - icon-512.png (512x512)

    Design: Devanāgarī-Zeichen "ॐ" (Om) auf #03192e Hintergrund,
    weisse Farbe, zentriert. Einfach, ikonisch, erkennbar als App-Icon.

    Fallback: Falls image_generate nicht verfügbar, erstelle minimale SVGs
    und konvertiere via sharp/sips CLI.
  </action>
  <verify>
    <automated>ls docs/public/pwa-icons/icon-{192,256,384,512}.png && echo "OK: 4 Icons vorhanden"</automated>
  </verify>
</task>

<task type="auto">
  <name>Task 2: manifest.json erstellen</name>
  <files>docs/public/manifest.json</files>
  <action>
    Erstelle docs/public/manifest.json mit folgendem Inhalt:

    ```json
    {
      "name": "Sanskritkurs — Alois Payer",
      "short_name": "Sanskritkurs",
      "description": "Grammatik Lehrbuch von Alois Payer — Sanskrit Offline",
      "start_url": "/",
      "display": "standalone",
      "orientation": "any",
      "theme_color": "#03192e",
      "background_color": "#fcf9f2",
      "icons": [
        { "src": "/pwa-icons/icon-192.png", "sizes": "192x192", "type": "image/png" },
        { "src": "/pwa-icons/icon-256.png", "sizes": "256x256", "type": "image/png" },
        { "src": "/pwa-icons/icon-384.png", "sizes": "384x384", "type": "image/png" },
        { "src": "/pwa-icons/icon-512.png", "sizes": "512x512", "type": "image/png" }
      ]
    }
    ```
  </action>
  <verify>
    <automated>node -e "const m=JSON.parse(require('fs').readFileSync('docs/public/manifest.json','utf8')); const req=['name','short_name','start_url','display','theme_color','background_color','icons']; const missing=req.filter(k=>!m[k]); if(missing.length){console.error('MISSING:',missing);process.exit(1)} if(m.display!=='standalone'){console.error('display must be standalone');process.exit(1)} if(m.icons.length<4){console.error('Need 4 icons');process.exit(1)} console.log('OK: manifest valid')"</automated>
  </verify>
</task>

</tasks>

<verification>
1. Beide Tasks müssen erfolgreich sein
2. npm run docs:build muss bestehen
3. manifest.json muss unter /manifest.json im Build-Output vorhanden sein
</verification>

<output>
Erstelle .planning/phases/18-pwa-offline-app/18-1-SUMMARY.md wenn fertig.
</output>
