---
phase: 18-pwa-offline-app
plan: 02
type: execute
wave: 1
depends_on: [18-1]
files_modified:
  - docs/.vitepress/config.mjs
autonomous: true

must_haves:
  truths:
    - "config.mjs enthält einen head-Array mit PWA Meta-Tags"
    - "link rel='manifest' href='/manifest.json' ist im head"
    - "meta name='theme-color' content='#03192e' ist im head"
    - "meta name='apple-mobile-web-app-capable' content='yes' ist im head"
    - "apple-touch-icon link ist im head"
  artifacts:
    - path: "docs/.vitepress/config.mjs"
      provides: "PWA Meta-Tags werden in jede generierte HTML-Seite injiziert"
      contains: "manifest.json, theme-color, apple-mobile-web-app"
---

<objective>
PWA Meta-Tags in die VitePress-Head-Konfiguration injizieren.

Purpose: Das Manifest allein reicht nicht — Browser benötigen Meta-Tags im HTML <head>,
um die App als PWA zu erkennen. Apple-spezifische Tags sind zusätzlich nötig für iOS Safari.

Output: Alle PWA Meta-Tags sind in config.mjs head-Array und werden in jede Seite injiziert.
</objective>

<context>
VitePress config.mjs unterstützt ein `head` Top-Level-Property (Array von [tag, attrs, children?]-Tupeln).
Aktuell hat config.mjs kein head-Property → muss hinzugefügt werden nach `cleanUrls: true`.

Benötigte Tags:
1. link rel="manifest" href="/manifest.json"
2. meta name="theme-color" content="#03192e"
3. meta name="apple-mobile-web-app-capable" content="yes"
4. meta name="apple-mobile-web-app-status-bar-style" content="black-translucent"
5. meta name="apple-mobile-web-app-title" content="Sanskritkurs"
6. link rel="apple-touch-icon" href="/pwa-icons/icon-192.png"
7. meta name="mobile-web-app-capable" content="yes"
</context>

<tasks>

<task type="auto">
  <name>Task 1: head-Array in config.mjs einfügen</name>
  <files>docs/.vitepress/config.mjs</files>
  <read_first>
    - docs/.vitepress/config.mjs Zeilen 121-128 (defineConfig Start, nach cleanUrls)
  </read_first>
  <action>
    Füge nach `cleanUrls: true,` (Zeile 127) das head-Property ein:

    ```javascript
    head: [
      ['link', { rel: 'manifest', href: '/manifest.json' }],
      ['meta', { name: 'theme-color', content: '#03192e' }],
      ['meta', { name: 'apple-mobile-web-app-capable', content: 'yes' }],
      ['meta', { name: 'apple-mobile-web-app-status-bar-style', content: 'black-translucent' }],
      ['meta', { name: 'apple-mobile-web-app-title', content: 'Sanskritkurs' }],
      ['link', { rel: 'apple-touch-icon', href: '/pwa-icons/icon-192.png' }],
      ['meta', { name: 'mobile-web-app-capable', content: 'yes' }],
    ],
    ```
  </action>
  <verify>
    <automated>grep -c "manifest.json\|theme-color\|apple-mobile-web-app\|apple-touch-icon\|mobile-web-app-capable" docs/.vitepress/config.mjs | xargs test 7 -le && echo "OK: alle PWA Meta-Tags vorhanden"</automated>
  </verify>
</task>

</tasks>

<verification>
1. npm run docs:build muss bestehen
2. Generierte HTML-Dateien müssen alle PWA Meta-Tags im <head> enthalten
3. manifest.json muss vom Browser korrekt geladen werden können
</verification>

<output>
Erstelle .planning/phases/18-pwa-offline-app/18-2-SUMMARY.md wenn fertig.
</output>
