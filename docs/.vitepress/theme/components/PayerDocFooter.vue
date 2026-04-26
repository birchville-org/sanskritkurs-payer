<template>
  <div v-if="showFooter" class="payer-doc-footer">
    <!-- Vorherige Seite -->
    <a v-if="prev" :href="prev.link" class="pager-card pager-prev">
      <span class="pager-label">{{ labels.prev }}</span>
      <span class="pager-title">{{ translateTitle(prev.text) }}</span>
    </a>
    <span v-else-if="hasSchrift" class="pager-spacer" />

    <!-- Schriftübung (nur für Lektionen mit Schriftlink) -->
    <a v-if="hasSchrift" :href="schriftUrl" class="pager-card pager-mid">
      <span class="pager-label">{{ labels.exercise }}</span>
      <span class="pager-title">{{ translatedSchriftText }}</span>
    </a>

    <!-- Nächste Seite -->
    <a v-if="next" :href="next.link" class="pager-card pager-next">
      <span class="pager-label">{{ labels.next }}</span>
      <span class="pager-title">{{ translateTitle(next.text) }}</span>
    </a>
    <span v-else-if="hasSchrift" class="pager-spacer" />
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useData, useRoute } from 'vitepress'
import navMapping from '../../data/nav_mapping.json'

const { theme, lang } = useData()
const route = useRoute()

const currentLang = computed(() => {
  const path = route.path
  if (path.startsWith('/en/')) return 'en'
  if (path.startsWith('/it/')) return 'it'
  if (path.startsWith('/es/')) return 'es'
  if (path.startsWith('/bg/')) return 'bg'
  return 'de'
})

const labels = computed(() => {
  const dict = {
    de: { prev: 'Vorherige Seite', exercise: 'Zusätzliche Übung', next: 'Nächste Seite' },
    en: { prev: 'Previous Page', exercise: 'Additional Exercise', next: 'Next Page' },
    it: { prev: 'Pagina precedente', exercise: 'Esercizio aggiuntivo', next: 'Prossima pagina' },
    es: { prev: 'Página anterior', exercise: 'Ejercicio adicional', next: 'Próxima página' },
    bg: { prev: 'Предишна страница', exercise: 'Допълнително упражнение', next: 'Следваща страница' }
  }
  return dict[currentLang.value] || dict.de
})

const translateTitle = (text) => {
  if (!text) return ''
  const l = currentLang.value
  if (l === 'de') return text
  
  let t = text
  if (l === 'it') {
    t = t.replace(/Schriftübung/g, 'Esercizio di scrittura')
    t = t.replace(/Lektion/g, 'Lezione')
    t = t.replace(/Übung/g, 'Esercizio')
    t = t.replace(/Schrift/g, 'Scrittura')
  } else if (l === 'es') {
    t = t.replace(/Schriftübung/g, 'Ejercicio de escritura')
    t = t.replace(/Lektion/g, 'Lección')
    t = t.replace(/Übung/g, 'Ejercicio')
    t = t.replace(/Schrift/g, 'Escritura')
  } else if (l === 'en') {
    t = t.replace(/Schriftübung/g, 'Writing Exercise')
    t = t.replace(/Lektion/g, 'Lesson')
    t = t.replace(/Übung/g, 'Exercise')
    t = t.replace(/Schrift/g, 'Script')
  } else if (l === 'bg') {
    t = t.replace(/Schriftübung/g, 'Упражнение по писмо')
    t = t.replace(/Lektion/g, 'Урок')
    t = t.replace(/Übung/g, 'Упражнение')
    t = t.replace(/Schrift/g, 'Писмо')
    t = t.replace(/Devanāgarī/g, 'Деванагари')
  }
  return t
}

// Alle Sidebar-Links der Reihe nach einsammeln
function flattenSidebar(sidebar) {
  const items = []
  function walk(arr) {
    for (const item of arr) {
      if (item.link) items.push({ text: item.text, link: item.link })
      if (item.items) walk(item.items)
    }
  }
  if (Array.isArray(sidebar)) {
    walk(sidebar)
  } else if (sidebar && typeof sidebar === 'object') {
    for (const key of Object.keys(sidebar)) walk(sidebar[key])
  }
  return items
}

const prevNext = computed(() => {
  const all = flattenSidebar(theme.value.sidebar || [])
  const cur = route.path.replace(/\/$/, '').replace(/\.html$/, '')
  const idx = all.findIndex(item => {
    const l = (item.link || '').replace(/\/$/, '').replace(/\.html$/, '')
    return cur === l || cur.endsWith(l)
  })
  if (idx < 0) return { prev: null, next: null }
  return {
    prev: idx > 0 ? all[idx - 1] : null,
    next: idx < all.length - 1 ? all[idx + 1] : null
  }
})

const prev = computed(() => prevNext.value.prev)
const next = computed(() => prevNext.value.next)

// Schriftlink aus nav_mapping
const schriftData = computed(() => {
  const m = route.path.match(/lektion(\d+)/)
  if (!m) return null
  const key = `lektion${m[1].padStart(2, '0')}`
  const d = navMapping[key]
  if (!d || !d.schrift) return null
  return d
})

const hasSchrift = computed(() => !!schriftData.value)

const schriftUrl = computed(() => {
  if (!schriftData.value) return ''
  const l = currentLang.value
  const base = l === 'de' ? '/lektionen/' : `/${l}/lektionen/`
  return base + schriftData.value.schrift.replace(/\.md$/, '')
})

const translatedSchriftText = computed(() => {
  if (!schriftData.value) return ''
  return translateTitle(schriftData.value.schrift_text)
})

const showFooter = computed(() => prev.value || next.value || hasSchrift.value)
</script>

<style scoped>
.payer-doc-footer {
  display: flex;
  gap: 8px;
  margin: 2rem 0 1rem 0;
  padding-top: 1.5rem;
  border-top: 1px solid var(--vp-c-divider);
}

.pager-card {
  display: flex;
  flex-direction: column;
  flex: 1;
  min-width: 0;
  border: 1px solid var(--vp-c-divider);
  border-radius: 8px;
  padding: 11px 16px 13px;
  text-decoration: none !important;
  transition: border-color 0.25s;
  font-family: "Inter", sans-serif;
}

.pager-card:hover {
  border-color: var(--vp-c-brand-1);
}

.pager-prev {
  text-align: left;
}

.pager-mid,
.pager-next {
  text-align: right;
}

.pager-spacer {
  flex: 1;
}

.pager-label {
  display: block;
  font-size: 12px;
  font-weight: 500;
  line-height: 20px;
  color: var(--vp-c-text-2);
}

.pager-title {
  display: block;
  font-size: 14px;
  font-weight: 400;
  line-height: 20px;
  color: var(--vp-c-brand-1);
  transition: color 0.25s;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}
</style>
