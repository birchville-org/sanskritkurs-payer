---
phase: 21-offline-qa-polishing
plan: 3
type: execute
wave: 1
depends_on: []
files_modified:
  - docs/.vitepress/theme/components/PayerOfflineIndicator.vue
  - docs/.vitepress/theme/index.mjs
  - docs/.vitepress/theme/custom.css
autonomous: true

must_haves:
  truths:
    - "Offline banner appears when navigator.onLine === false"
    - "Banner disappears when connection restored"
    - "Banner uses Design System colors (Parchment #fcf9f2, Deep Ink #03192e)"
    - "No layout shift when banner appears/disappears"
  artifacts:
    - path: "docs/.vitepress/theme/components/PayerOfflineIndicator.vue"
      provides: "Vue component for offline/online status display"
      contains: "online/offline event listeners, reactive state"
  key_links:
    - from: "index.mjs Layout"
      to: "PayerOfflineIndicator"
      via: "h() slot injection"
      pattern: "doc-before.*PayerOfflineIndicator"
---

# Plan 21-3: UX Offline Indicator + Sync Status

**Phase**: 21 Offline QA & Polishing
**Status**: Pending
**Dependencies**: Phase 20 (lang-settings.js exists)

## Objective

Create a Vue component that displays an offline banner when the browser loses network connectivity, and a sync status indicator when content is being prefetched.

## Tasks

### Task 21-3.1: Create PayerOfflineIndicator Component

<task type="auto">
<name>Create PayerOfflineIndicator.vue</name>
<files>
  - docs/.vitepress/theme/components/PayerOfflineIndicator.vue
</files>
<read_first>
- docs/.vitepress/theme/custom.css (Design System variables)
- docs/.vitepress/theme/components/PayerLanguageSettings.vue (existing component patterns)
</read_first>
<action>
Create `docs/.vitepress/theme/components/PayerOfflineIndicator.vue`:

```vue
<script setup>
import { ref, onMounted, onUnmounted } from 'vue'

const offline = ref(!navigator.onLine)
const syncing = ref(false)

function updateOnlineStatus() {
  offline.value = !navigator.onLine
}

// Listen for prefetch progress from SW
onMounted(() => {
  window.addEventListener('online', updateOnlineStatus)
  window.addEventListener('offline', updateOnlineStatus)
  
  // Listen for SW prefetch progress events
  if (navigator.serviceWorker) {
    navigator.serviceWorker.addEventListener('message', (event) => {
      if (event.data?.type === 'PREFETCH_PROGRESS' ||
          event.data?.type === 'PREFETCH_BATCH_PROGRESS') {
        syncing.value = true
      }
      if (event.data?.type === 'PREFETCH_COMPLETE' ||
          event.data?.type === 'PREFETCH_BATCH_COMPLETE') {
        syncing.value = false
      }
    })
  }
})

onUnmounted(() => {
  window.removeEventListener('online', updateOnlineStatus)
  window.removeEventListener('offline', updateOnlineStatus)
})
</script>

<template>
  <div v-if="offline" class="payer-offline-banner" role="alert">
    <span class="payer-offline-icon">⚠</span>
    <span class="payer-offline-text">
      {{ syncing ? 'Synchronisiere…' : 'Offline — Inhalte werden aus dem Cache geladen' }}
    </span>
  </div>
</template>

<style scoped>
.payer-offline-banner {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 16px;
  font-size: 0.8125rem;
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
  background: #fcf9f2;
  color: #48626e;
  border-bottom: 1px solid #e8e4d8;
  text-align: center;
  justify-content: center;
}

.payer-offline-icon {
  font-size: 1rem;
  opacity: 0.7;
}

.payer-offline-text {
  font-weight: 500;
}
</style>
```

Key design decisions:
- Banner uses Parchment background (#fcf9f2) and Slate Grey text (#48626e) to match Design System
- Positioned at top of page via `doc-before` slot
- Uses `role="alert"` for accessibility
- Shows sync status when prefetch is in progress
- No layout shift: banner height is fixed, uses flexbox centering
</action>
<verify>
Component file created with correct structure.
</verify>
<acceptance_criteria>
- PayerOfflineIndicator.vue exists in theme/components/
- Uses Design System colors
- Listens to online/offline events
- Shows sync status during prefetch
- Scoped CSS only
</acceptance_criteria>
</task>

### Task 21-3.2: Register Component in index.mjs

<task type="auto">
<name>Integrate PayerOfflineIndicator into theme</name>
<files>
  - docs/.vitepress/theme/index.mjs
</files>
<read_first>
- docs/.vitepress/theme/index.mjs (current Layout slots)
</read_first>
<action>
1. Import the component:
   ```js
   import PayerOfflineIndicator from './components/PayerOfflineIndicator.vue'
   ```
2. Register as global component in enhanceApp:
   ```js
   app.component('PayerOfflineIndicator', PayerOfflineIndicator)
   ```
3. Add to Layout slots:
   ```js
   Layout: () => h(DefaultTheme.Layout, null, {
     'doc-footer-before': () => h(PayerDocFooter),
     'doc-before': () => h(PayerOfflineIndicator),
     'nav-bar-content-after': () => h(PayerWideToggle)
   }),
   ```
</action>
<verify>
Component imported, registered, and injected into Layout.
</verify>
<acceptance_criteria>
- Import added at top of index.mjs
- Component registered in enhanceApp
- 'doc-before' slot injects PayerOfflineIndicator
- Build succeeds
</acceptance_criteria>
</task>

### Task 21-3.3: Add CSS Variables (if needed)

<task type="auto">
<name>Add any missing CSS variables to custom.css</name>
<files>
  - docs/.vitepress/theme/custom.css
</files>
<read_first>
- docs/.vitepress/theme/custom.css
</read_first>
<action>
Check if custom.css has the Design System color variables. If not, add:
```css
:root {
  --vp-c-parchment: #fcf9f2;
  --vp-c-parchment-dark: #f1eee7;
  --vp-c-ink: #03192e;
  --vp-c-slate: #48626e;
}
```
</action>
<verify>
CSS variables available for component styling.
</verify>
<acceptance_criteria>
- Design System colors defined in custom.css
- Component references correct variables
</acceptance_criteria>
</task>

## Verification

```bash
# Build check
npm run docs:build

# Preview and test
npm run docs:preview
# Open http://localhost:4173, toggle offline in DevTools
```

## Success Criteria

- [ ] PayerOfflineIndicator.vue created with Design System styling
- [ ] Component registered and injected in index.mjs
- [ ] Offline banner appears when network lost
- [ ] Banner shows sync status during prefetch
- [ ] Banner disappears when network restored
- [ ] Zero JS errors
- [ ] No layout shift
- [ ] `npm run docs:build` successful
