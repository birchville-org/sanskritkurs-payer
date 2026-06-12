# Plan 20-1: Settings-Page UI

**Phase**: 20 Sprachauswahl (Runtime-Filter)  
**Status**: Pending  
**Dependencies**: Phase 19 ✅

## Ziel

Settings-Page erstellen wo der User aktive Sprachen auswählt. Auswahl wird in localStorage persistiert.

## Deliverables

1. `docs/de/settings.md` (+ 13 Sprach-Versionen) — Markdown-Page
2. `docs/.vitepress/theme/components/PayerLanguageSettings.vue` — Vue-Component
3. `docs/.vitepress/theme/lang-settings.js` — shared state (localStorage wrapper)

## Implementation

### 20-1.1: Shared State (`lang-settings.js`)

```javascript
// docs/.vitepress/theme/lang-settings.js
const STORAGE_KEY = 'payer_active_locales'
const ALL_LOCALES = ['de', 'en', 'it', 'bg', 'ru', 'uk', 'hi', 'fr', 'es', 'ta', 'pa', 'la', 'rm', 'ro']
const DEFAULT_LOCALES = ['de', 'en', 'it']

export function getActiveLocales() {
  if (typeof localStorage === 'undefined') return DEFAULT_LOCALES
  const stored = localStorage.getItem(STORAGE_KEY)
  if (!stored) return DEFAULT_LOCALES
  try {
    const parsed = JSON.parse(stored)
    return Array.isArray(parsed) ? parsed : DEFAULT_LOCALES
  } catch {
    return DEFAULT_LOCALES
  }
}

export function setActiveLocales(locales) {
  if (typeof localStorage === 'undefined') return
  localStorage.setItem(STORAGE_KEY, JSON.stringify(locales))
  // Broadcast an Service Worker (Plan 20-3)
  if (navigator.serviceWorker?.controller) {
    navigator.serviceWorker.controller.postMessage({
      type: 'SET_ACTIVE_LOCALES',
      locales
    })
  }
  // Custom Event für Vue-Komponenten
  window.dispatchEvent(new CustomEvent('payer:locales-changed', { detail: locales }))
}

export { ALL_LOCALES, DEFAULT_LOCALES }
```

### 20-1.2: Vue Component (`PayerLanguageSettings.vue`)

```vue
<script setup>
import { ref, onMounted } from 'vue'
import { ALL_LOCALES, getActiveLocales, setActiveLocales } from '../lang-settings.js'

const selected = ref(getActiveLocales())
const currentLocale = ref('de')  // injected at runtime
const saving = ref(false)

const LOCALE_NAMES = {
  de: 'Deutsch', en: 'English', it: 'Italiano', bg: 'Български',
  ru: 'Русский', uk: 'Українська', hi: 'हिन्दी', fr: 'Français',
  es: 'Español', ta: 'தமிழ்', pa: 'ਪੰਜਾਬੀ', la: 'Latine',
  rm: 'Rumantsch', ro: 'Română'
}

function save() {
  if (selected.value.length === 0) {
    alert('Mindestens eine Sprache muss ausgewählt sein.')
    return
  }
  saving.value = true
  setActiveLocales(selected.value)
  setTimeout(() => saving.value = false, 500)
}

onMounted(() => {
  // Aktuelle Sprache aus URL ableiten
  const path = window.location.pathname
  const match = path.match(/^\/([a-z]{2})(\/|$)/)
  currentLocale.value = match ? match[1] : 'de'
})
</script>

<template>
  <div class="language-settings">
    <h2>Aktive Sprachen / Active Languages</h2>
    <p class="hint">
      Wählen Sie die Sprachen aus, die in der Navigation sichtbar und offline verfügbar sein sollen.
    </p>
    <div class="locale-grid">
      <label v-for="locale in ALL_LOCALES" :key="locale" class="locale-item">
        <input
          type="checkbox"
          :value="locale"
          v-model="selected"
          :disabled="locale === currentLocale"
        />
        <span class="locale-name">{{ LOCALE_NAMES[locale] }}</span>
        <span class="locale-code">({{ locale }})</span>
        <span v-if="locale === currentLocale" class="locale-current">aktuell</span>
      </label>
    </div>
    <button @click="save" :disabled="saving || selected.length === 0" class="save-btn">
      {{ saving ? 'Gespeichert ✓' : 'Speichern' }}
    </button>
    <div class="cache-info">
      Geschätzte Cache-Größe: ~{{ (selected.length * 23).toFixed(0) }} MB
    </div>
  </div>
</template>

<style scoped>
.language-settings {
  max-width: 640px;
  margin: 2rem auto;
  padding: 2rem;
  background: var(--vp-c-bg-soft);
  border-radius: 8px;
}

.locale-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
  gap: 0.5rem;
  margin: 1.5rem 0;
}

.locale-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 0.75rem;
  cursor: pointer;
  border-radius: 4px;
  transition: background 200ms;
}

.locale-item:hover {
  background: var(--vp-c-bg);
}

.locale-name { font-weight: 500; }
.locale-code { color: var(--vp-c-text-2); font-size: 0.875em; }
.locale-current {
  margin-left: auto;
  font-size: 0.75em;
  padding: 2px 6px;
  background: var(--vp-c-brand);
  color: white;
  border-radius: 2px;
}

.save-btn {
  background: #03192e;
  color: #fcf9f2;
  border: none;
  padding: 10px 24px;
  border-radius: 4px;
  cursor: pointer;
  font-family: 'Inter', sans-serif;
  font-weight: 500;
}

.save-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.cache-info {
  margin-top: 1rem;
  font-size: 0.875em;
  color: var(--vp-c-text-2);
}
</style>
```

### 20-1.3: Markdown-Page (`docs/de/settings.md` + 13 Lokalisierungen)

```markdown
---
layout: doc
title: Einstellungen
---

<ClientOnly>
  <PayerLanguageSettings />
</ClientOnly>

## Sprache hinzufügen

Wenn Sie eine neue Sprache aktivieren, werden die entsprechenden Inhalte beim nächsten
Online-Besuch automatisch heruntergeladen und im Cache gespeichert.

## Cache verwalten

Unter "Cache leeren" können Sie den lokalen Cache zurücksetzen:
- Alle offline-Inhalte werden gelöscht
- Beim nächsten Online-Besuch werden nur die aktiven Sprachen neu gecacht

<button onclick="caches.keys().then(names => Promise.all(names.map(n => caches.delete(n)))).then(() => location.reload())">
  Cache leeren / Clear Cache
</button>
```

**Lokalisierungen**: `docs/{locale}/settings.md` für alle 14 Sprachen (generiert via Skript).

### 20-1.4: Component registrieren in `index.mjs`

```javascript
import PayerLanguageSettings from './components/PayerLanguageSettings.vue'

// In enhanceApp:
app.component('PayerLanguageSettings', PayerLanguageSettings)
```

### 20-1.5: Sidebar-Eintrag hinzufügen

In jedem `locales/{lang}.mjs` einen Sidebar-Link unter "Index" hinzufügen:
```javascript
{
  text: 'Einstellungen',
  link: '/settings'
}
```

## Verification

```bash
npm run docs:dev
# 1. Öffne /settings
# 2. Checkboxen funktionieren
# 3. "Speichern" schreibt in localStorage
# 4. Reload → Auswahl bleibt erhalten
# 5. Console: keine Errors
```

## Success Criteria

- ✅ Settings-Page existiert in allen 14 Sprachen
- ✅ Vue-Component rendert 14 Checkboxen
- ✅ localStorage persistiert Auswahl
- ✅ Custom Event `payer:locales-changed` feuert bei Save
- ✅ Service Worker empfängt Post-Message (nur log, Plan 20-3 nutzt es)
- ✅ Current locale ist disabled (kann nicht deaktiviert werden)
- ✅ Build erfolgreich

## Notes

- `<ClientOnly>` ist nötig weil `localStorage` nur im Browser existiert
- Settings-Page ist KEIN Markdown-Feature, sondern eine dedizierte Vue-Page
- Cache-Info (23MB pro Sprache) ist Schätzung — exakte Zahl in Plan 20-5
