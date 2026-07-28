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
  } else if (l === 'ru') {
    t = t.replace(/Schriftübung/g, 'Упражнение по письму')
    t = t.replace(/Lektion/g, 'Лекция')
    t = t.replace(/Übung/g, 'Упражнение')
    t = t.replace(/Schrift/g, 'Письмо')
  } else if (l === 'uk') {
    t = t.replace(/Schriftübung/g, 'Вправа з письма')
    t = t.replace(/Lektion/g, 'Лекція')
    t = t.replace(/Übung/g, 'Вправа')
    t = t.replace(/Schrift/g, 'Письмо')
  } else if (l === 'hi') {
    t = t.replace(/Schriftübung/g, 'लिपि अभ्यास')
    t = t.replace(/Lektion/g, 'पाठ')
    t = t.replace(/Übung/g, 'अभ्यास')
    t = t.replace(/Schrift/g, 'लिपि')
  } else if (l === 'fr') {
    t = t.replace(/Schriftübung/g, "Exercice d'écriture")
    t = t.replace(/Lektion/g, 'Leçon')
    t = t.replace(/Übung/g, 'Exercice')
    t = t.replace(/Schrift/g, 'Écriture')
  } else if (l === 'ta') {
    t = t.replace(/Schriftübung/g, 'எழுத்து பயிற்சி')
    t = t.replace(/Lektion/g, 'பாடம்')
    t = t.replace(/Übung/g, 'பயிற்சி')
    t = t.replace(/Schrift/g, 'எழுத்து')
  } else if (l === 'pa') {
    t = t.replace(/Schriftübung/g, 'ਲਿਪੀ ਅਭਿਆਸ')
    t = t.replace(/Lektion/g, 'ਪਾਠ')
    t = t.replace(/Übung/g, 'ਅਭਿਆਸ')
    t = t.replace(/Schrift/g, 'ਲਿਪੀ')
  } else if (l === 'la') {
    t = t.replace(/Schriftübung/g, 'Exercitatio scripturae')
    t = t.replace(/Lektion/g, 'Lectio')
    t = t.replace(/Übung/g, 'Exercitatio')
    t = t.replace(/Schrift/g, 'Scriptura')
  } else if (l === 'rm') {
    t = t.replace(/Schriftübung/g, "Exercizi da scrittira")
    t = t.replace(/Lektion/g, 'Lecziun')
    t = t.replace(/Übung/g, 'Exercizi')
    t = t.replace(/Schrift/g, 'Scrittira')
  } else if (l === 'ro') {
    t = t.replace(/Schriftübung/g, 'Exercițiu de scriere')
    t = t.replace(/Lektion/g, 'Lecție')
    t = t.replace(/Übung/g, 'Exercițiu')
    t = t.replace(/Schrift/g, 'Scriere')
  } else if (l === 'he') {
    t = t.replace(/Schriftübung/g, 'תרגיל כתיבה')
    t = t.replace(/Lektion/g, 'שיעור')
    t = t.replace(/Übung/g, 'תרגיל')
    t = t.replace(/Schrift/g, 'כתב')
  } else if (l === 'id') {
    t = t.replace(/Schriftübung/g, 'Latihan Menulis')
    t = t.replace(/Lektion/g, 'Pelajaran')
    t = t.replace(/Übung/g, 'Latihan')
    t = t.replace(/Schrift/g, 'Aksara')
  } else if (l === 'ar') {
    t = t.replace(/Schriftübung/g, 'تمرين كتابة')
    t = t.replace(/Lektion/g, 'درس')
    t = t.replace(/Übung/g, 'تمرين')
    t = t.replace(/Schrift/g, 'خط')
  } else if (l === 'arc') {
    t = t.replace(/Schriftübung/g, 'Writing Exercise')
    t = t.replace(/Lektion/g, 'Lesson')
    t = t.replace(/Übung/g, 'Exercise')
    t = t.replace(/Schrift/g, 'Script')
  } else if (l === 'zh-CN') {
    t = t.replace(/Schriftübung/g, '书写练习')
    t = t.replace(/Lektion/g, '课')
    t = t.replace(/Übung/g, '练习')
    t = t.replace(/Schrift/g, '字母')
  } else if (l === 'th') {
    t = t.replace(/Schriftübung/g, 'แบบฝึกหัดการเขียน')
    t = t.replace(/Lektion/g, 'บทเรียน')
    t = t.replace(/Übung/g, 'แบบฝึกหัด')
    t = t.replace(/Schrift/g, 'อักษร')
  } else if (l === 'el') {
    t = t.replace(/Schriftübung/g, 'Άσκηση Γραφής')
    t = t.replace(/Lektion/g, 'Μάθημα')
    t = t.replace(/Übung/g, 'Άσκηση')
    t = t.replace(/Schrift/g, 'Γραφή')
  } else if (l === 'grc') {
    t = t.replace(/Schriftübung/g, 'Ἄσκησις γραφῆς')
    t = t.replace(/Lektion/g, 'Μάθημα')
    t = t.replace(/Übung/g, 'Ἄσκησις')
    t = t.replace(/Schrift/g, 'Γραφή')
  } else if (l === 'cop') {
    t = t.replace(/Schriftübung/g, 'Writing Exercise')
    t = t.replace(/Lektion/g, 'Lesson')
    t = t.replace(/Übung/g, 'Exercise')
    t = t.replace(/Schrift/g, 'Script')
  } else if (l === 'fi') {
    t = t.replace(/Schriftübung/g, 'Kirjoitusharjoitus')
    t = t.replace(/Lektion/g, 'Oppitunti')
    t = t.replace(/Übung/g, 'Harjoitus')
    t = t.replace(/Schrift/g, 'Kirjoitus')
  } else if (l === 'hu') {
    t = t.replace(/Schriftübung/g, 'Írásgyakorlat')
    t = t.replace(/Lektion/g, 'Lecke')
    t = t.replace(/Übung/g, 'Gyakorlat')
    t = t.replace(/Schrift/g, 'Írás')
  } else if (l === 'pt') {
    t = t.replace(/Schriftübung/g, 'Exercício de escrita')
    t = t.replace(/Lektion/g, 'Lição')
    t = t.replace(/Übung/g, 'Exercício')
    t = t.replace(/Schrift/g, 'Escrita')
  } else if (l === 'af') {
    t = t.replace(/Schriftübung/g, 'Skryfoefening')
    t = t.replace(/Lektion/g, 'Les')
    t = t.replace(/Übung/g, 'Oefening')
    t = t.replace(/Schrift/g, 'Skrif')
  } else if (l === 'lt') {
    t = t.replace(/Schriftübung/g, 'Rašymo užduotis')
    t = t.replace(/Lektion/g, 'Pamoka')
    t = t.replace(/Übung/g, 'Užduotis')
    t = t.replace(/Schrift/g, 'Raštas')
  } else if (l === 'sh') {
    t = t.replace(/Schriftübung/g, 'Vežba pisanja')
    t = t.replace(/Lektion/g, 'Lekcija')
    t = t.replace(/Übung/g, 'Vežba')
    t = t.replace(/Schrift/g, 'Pismo')
  } else if (l === 'sq') {
    t = t.replace(/Schriftübung/g, 'Ushtrim shkrimi')
    t = t.replace(/Lektion/g, 'Mësimi')
    t = t.replace(/Übung/g, 'Ushtrim')
    t = t.replace(/Schrift/g, 'Shkrimi')
  } else if (l === 'am') {
    t = t.replace(/Schriftübung/g, 'የጽሑፍ ልምምድ')
    t = t.replace(/Lektion/g, 'ትምህርት')
    t = t.replace(/Übung/g, 'ልምምድ')
    t = t.replace(/Schrift/g, 'ጽሑፍ')
  } else if (l === 'fa') {
    t = t.replace(/Schriftübung/g, 'تمرین نوشتاری')
    t = t.replace(/Lektion/g, 'درس')
    t = t.replace(/Übung/g, 'تمرین')
    t = t.replace(/Schrift/g, 'خط')
  } else if (l === 'nl') {
    t = t.replace(/Schriftübung/g, 'Schrijfoefening')
    t = t.replace(/Lektion/g, 'Les')
    t = t.replace(/Übung/g, 'Oefening')
    t = t.replace(/Schrift/g, 'Schrift')
  } else if (l === 'zh') {
    t = t.replace(/Schriftübung/g, '書寫練習')
    t = t.replace(/Lektion/g, '課')
    t = t.replace(/Übung/g, '練習')
    t = t.replace(/Schrift/g, '字母')
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
