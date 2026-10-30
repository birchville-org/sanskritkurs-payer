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
import { FOOTER_LABELS } from '../../languages.mjs'

const { theme, lang } = useData()
const route = useRoute()

const currentLang = computed(() => {
  const parts = route.path.split('/')
  if (parts.length > 1 && parts[1]) {
    return parts[1]
  }
  return 'de'
})

const labels = computed(() => {
  return FOOTER_LABELS[currentLang.value] || FOOTER_LABELS.de
})

const TITLE_TERMS = {
  en: { Schriftübung: 'Writing Exercise', Lektion: 'Lesson', Übung: 'Exercise', Schrift: 'Script' },
  it: { Schriftübung: 'Esercizio di scrittura', Lektion: 'Lezione', Übung: 'Esercizio', Schrift: 'Scrittura' },
  es: { Schriftübung: 'Ejercicio de escritura', Lektion: 'Lección', Übung: 'Ejercicio', Schrift: 'Escritura' },
  fr: { Schriftübung: "Exercice d'écriture", Lektion: 'Leçon', Übung: 'Exercice', Schrift: 'Écriture' },
  bg: { Schriftübung: 'Упражнение по писмо', Lektion: 'Урок', Übung: 'Упражнение', Schrift: 'Писмо', Devanāgarī: 'Деванагари' },
  ru: { Schriftübung: 'Упражнение по письму', Lektion: 'Лекция', Übung: 'Упражнение', Schrift: 'Письмо' },
  uk: { Schriftübung: 'Вправа з письма', Lektion: 'Лекція', Übung: 'Вправа', Schrift: 'Письмо' },
  hi: { Schriftübung: 'लिपि अभ्यास', Lektion: 'पाठ', Übung: 'अभ्यास', Schrift: 'लिपि' },
  ta: { Schriftübung: 'எழுத்து பயிற்சி', Lektion: 'பாடம்', Übung: 'பயிற்சி', Schrift: 'எழுத்து' },
  te: { Schriftübung: 'లిపి అభ్యాసం', Lektion: 'పాఠం', Übung: 'అభ్యాసం', Schrift: 'లిపి' },
  pa: { Schriftübung: 'ਲਿਪੀ ਅਭਿਆਸ', Lektion: 'ਪਾਠ', Übung: 'ਅਭਿਆਸ', Schrift: 'ਲਿਪੀ' },
  la: { Schriftübung: 'Exercitatio scripturae', Lektion: 'Lectio', Übung: 'Exercitatio', Schrift: 'Scriptura' },
  rm: { Schriftübung: 'Exercizi da scrittira', Lektion: 'Lecziun', Übung: 'Exercizi', Schrift: 'Scrittira' },
  ro: { Schriftübung: 'Exercițiu de scriere', Lektion: 'Lecție', Übung: 'Exercițiu', Schrift: 'Scriere' },
  he: { Schriftübung: 'תרגיל כתיבה', Lektion: 'שיעור', Übung: 'תרגיל', Schrift: 'כתב' },
  id: { Schriftübung: 'Latihan Menulis', Lektion: 'Pelajaran', Übung: 'Latihan', Schrift: 'Aksara' },
  ar: { Schriftübung: 'تمرين كتابة', Lektion: 'درس', Übung: 'تمرين', Schrift: 'خط' },
  cs: { Schriftübung: 'Písemné cvičení', Lektion: 'Lekce', Übung: 'Cvičení', Schrift: 'Písmo' },
  'zh-CN': { Schriftübung: '书写练习', Lektion: '课', Übung: '练习', Schrift: '字母' },
  zh: { Schriftübung: '書寫練習', Lektion: '課', Übung: '練習', Schrift: '字母' },
  el: { Schriftübung: 'Άσκηση Γραφής', Lektion: 'Μάθημα', Übung: 'Άσκηση', Schrift: 'Γραφή' },
  grc: { Schriftübung: 'Ἄσκησις γραφῆς', Lektion: 'Μάθημα', Übung: 'Ἄσκησις', Schrift: 'Γραφή' },
  th: { Schriftübung: 'แบบฝึกหัดการเขียน', Lektion: 'บทเรียน', Übung: 'แบบฝึกหัด', Schrift: 'อักษร' },
  fi: { Schriftübung: 'Kirjoitusharjoitus', Lektion: 'Oppitunti', Übung: 'Harjoitus', Schrift: 'Kirjoitus' },
  hu: { Schriftübung: 'Írásgyakorlat', Lektion: 'Lecke', Übung: 'Gyakorlat', Schrift: 'Írás' },
  pt: { Schriftübung: 'Exercício de escrita', Lektion: 'Lição', Übung: 'Exercício', Schrift: 'Escrita' },
  af: { Schriftübung: 'Skryfoefening', Lektion: 'Les', Übung: 'Oefening', Schrift: 'Skrif' },
  lt: { Schriftübung: 'Rašymo užduotis', Lektion: 'Pamoka', Übung: 'Užduotis', Schrift: 'Raštas' },
  sh: { Schriftübung: 'Vežba pisanja', Lektion: 'Lekcija', Übung: 'Vežba', Schrift: 'Pismo' },
  sq: { Schriftübung: 'Ushtrim shkrimi', Lektion: 'Mësimi', Übung: 'Ushtrim', Schrift: 'Shkrimi' },
  am: { Schriftübung: 'የጽሑፍ ልምምድ', Lektion: 'ትምህርት', Übung: 'ልምምድ', Schrift: 'ጽሑፍ' },
  fa: { Schriftübung: 'تمرین نوشتاری', Lektion: 'درس', Übung: 'تمرین', Schrift: 'خط' },
  nl: { Schriftübung: 'Schrijfoefening', Lektion: 'Les', Übung: 'Oefening', Schrift: 'Schrift' }
}

const translateTitle = (text) => {
  if (!text) return ''
  const l = currentLang.value
  if (l === 'de' || !TITLE_TERMS[l]) return text

  const map = TITLE_TERMS[l]
  let t = text
  for (const [key, val] of Object.entries(map)) {
    t = t.replaceAll(key, val)
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
