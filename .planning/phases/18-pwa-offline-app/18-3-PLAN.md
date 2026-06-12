---
phase: 18-pwa-offline-app
plan: 03
type: execute
wave: 1
depends_on: [18-2]
files_modified:
  - docs/.vitepress/theme/index.mjs
autonomous: true

must_haves:
  truths:
    - "beforeinstallprompt Event wird abgefangen und gespeichert"
    - "Install-Button ist sichtbar wenn App installierbar ist"
    - "Install-Button wird ausgeblendet nach Installation (appinstalled Event)"
    - "Button-Style passt zum Scholarly Design System (#03192e, Newsreader/Inter)"
    - "Kein Layout-Shift durch verspätetes Erscheinen des Buttons"
  artifacts:
    - path: "docs/.vitepress/theme/index.mjs"
      provides: "PWA Install-Prompt Logik + UI-Button"
      contains: "beforeinstallprompt, appinstalled, .pwa-install-btn"
---

<objective>
PWA Install-Prompt UI implementieren.

Purpose: Bots zeigen keinen nativen Install-Banner. Wir fangen das browser native
beforeinstallprompt Event ab und zeigen einen eigenen, zum Design passenden Button.

Output: Install-Button erscheint unten-rechts, verschwindet nach Installation.
</objective>

<context>
VitePress Custom Theme: docs/.vitepress/theme/index.mjs.
Falls nicht vorhanden: defaultTheme als Basis erweitern.

Das beforeinstallprompt Event:
- Wird nur gefeuert wenn: Manifest valide + Service Worker aktiv + HTTPS + nicht schon installiert
- Muss mit event.preventDefault() gestoppt werden, sonst zeigt Chrome den nativen Banner
- event.prompt() zeigt dann unseren Custom-Prompt
- appinstalled Event feuert nach erfolgreicher Installation → Button ausblenden

Design (AGENTS.md):
- Farbe: #03192e (Deep Ink) Hintergrund, #fcf9f2 (Parchment) Text
- Font: Inter (sans-serif), 14px
- Position: fixed, bottom-right, margin 16px
- Animation: fade-in 200ms
</context>

<tasks>

<task type="auto">
  <name>Task 1: Custom Theme mit Install-Prompt Logik</name>
  <files>docs/.vitepress/theme/index.mjs</files>
  <read_first>
    - docs/.vitepress/theme/index.mjs (falls existent)
    - docs/.vitepress/theme/ (Verzeichnis-Listing)
  </read_first>
  <action>
    Falls docs/.vitepress/theme/index.mjs NICHT existiert:
    Erstelle es mit default-Export der defaultTheme + Layout-Wrapper:

    ```javascript
    import DefaultTheme from 'vitepress/theme'
    import { onMounted } from 'vue'

    export default {
      extends: DefaultTheme,
      setup() {
        onMounted(() => {
          if (typeof window === 'undefined') return

          let deferredPrompt = null
          const btn = document.createElement('button')
          btn.className = 'pwa-install-btn'
          btn.textContent = 'App installieren'
          btn.style.display = 'none'
          btn.addEventListener('click', async () => {
            if (!deferredPrompt) return
            deferredPrompt.prompt()
            const { outcome } = await deferredPrompt.userChoice
            deferredPrompt = null
            btn.style.display = 'none'
          })
          document.body.appendChild(btn)

          window.addEventListener('beforeinstallprompt', (e) => {
            e.preventDefault()
            deferredPrompt = e
            btn.style.display = 'block'
          })

          window.addEventListener('appinstalled', () => {
            deferredPrompt = null
            btn.style.display = 'none'
          })
        })
      }
    }
    ```

    Falls existent: Integriere die Install-Prompt Logik in das bestehende setup().

    CSS (in docs/.vitepress/theme/custom.css oder inline im Layout):

    ```css
    .pwa-install-btn {
      position: fixed;
      bottom: 16px;
      right: 16px;
      z-index: 9999;
      padding: 12px 24px;
      background: #03192e;
      color: #fcf9f2;
      font-family: 'Inter', sans-serif;
      font-size: 14px;
      font-weight: 500;
      border: none;
      border-radius: 8px;
      cursor: pointer;
      box-shadow: 0 2px 8px rgba(3, 25, 46, 0.3);
      animation: fadeIn 200ms ease-out;
      transition: opacity 200ms;
    }
    .pwa-install-btn:hover {
      opacity: 0.9;
    }
    @keyframes fadeIn {
      from { opacity: 0; transform: translateY(8px); }
      to { opacity: 1; transform: translateY(0); }
    }
    ```
  </action>
  <verify>
    <automated>grep -c "beforeinstallprompt\|appinstalled\|pwa-install-btn\|deferredPrompt" docs/.vitepress/theme/index.mjs | xargs test 4 -le && echo "OK: Install-Prompt Logik vorhanden"</automated>
  </verify>
</task>

</tasks>

<verification>
1. npm run docs:build muss bestehen
2. Button erscheint nur wenn App installierbar ist (Chrome DevTools → Application → Manifest prüfen)
3. Button verschwindet nach Installation
4. Kein JS-Error in der Konsole
</verification>

<output>
Erstelle .planning/phases/18-pwa-offline-app/18-3-SUMMARY.md wenn fertig.
</output>
