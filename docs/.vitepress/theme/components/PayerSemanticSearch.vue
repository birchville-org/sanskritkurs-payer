<template>
  <div class="payer-semantic-search-wrapper">
    <!-- Trigger Button in Navbar / Header -->
    <button 
      class="payer-semantic-search-btn" 
      @click="openModal" 
      title="Semantische KI-Suche"
    >
      <span class="search-icon">🧠</span>
      <span class="search-label">KI-Suche</span>
    </button>

    <!-- Modal Dialog -->
    <Teleport to="body">
      <div v-if="isOpen" class="payer-semantic-modal-backdrop" @click.self="closeModal">
        <div class="payer-semantic-modal">
          
          <!-- Header -->
          <div class="payer-semantic-header">
            <div class="title-wrap">
              <span class="brain-badge">🧠 Semantische Suche</span>
              <p class="subtitle">Durchsuche den Sanskritkurs nach Bedeutung und Konzepten</p>
            </div>
            <div class="header-status" v-if="workerStatus">
              <span class="status-dot" :class="workerStatus"></span>
              <span class="status-text">{{ workerStatusLabel }}</span>
            </div>
            <button class="close-btn" @click="closeModal">&times;</button>
          </div>

          <!-- Input Field -->
          <div class="payer-semantic-input-wrap">
            <input 
              v-model="query" 
              type="text" 
              class="payer-semantic-input" 
              placeholder="z.B. 'Vergangenheit im Sanskrit' oder 'Wie drücke ich müssen aus?'"
              @keyup.enter="performSearch"
              ref="searchInput"
            />
            <button class="action-search-btn" @click="performSearch" :disabled="isLoading">
              {{ isLoading ? 'Sucht...' : 'Suchen' }}
            </button>
          </div>

          <!-- Quick Examples -->
          <div class="payer-quick-queries">
            <span class="label">Beispiele:</span>
            <button @click="setQuery('Vergangenheit im Sanskrit')">Vergangenheit</button>
            <button @click="setQuery('Wie drücke ich müssen aus?')">Notwendigkeit (müssen)</button>
            <button @click="setQuery('Passivform im Sanskrit')">Passiv</button>
          </div>

          <!-- Loading Indicator -->
          <div v-if="isLoading" class="payer-semantic-loading">
            <div class="spinner"></div>
            <span>Vektor-Ähnlichkeit wird berechnet...</span>
          </div>

          <!-- Results List -->
          <div v-else-if="results.length > 0" class="payer-semantic-results">
            <div 
              v-for="(item, idx) in results" 
              :key="idx" 
              class="payer-semantic-card"
              @click="navigateTo(item)"
            >
              <div class="card-header">
                <span class="match-badge" :style="{ backgroundColor: getBadgeColor(item.score) }">
                  {{ (item.score * 100).toFixed(1) }}% Match
                </span>
                <span class="file-tag">{{ formatFileName(item.file) }}</span>
              </div>
              <h4 class="card-title">{{ item.heading }}</h4>
              <p class="card-snippet">{{ item.snippet }}...</p>
            </div>
          </div>

          <!-- Empty / No Results -->
          <div v-else-if="hasSearched" class="payer-semantic-empty">
            Keine passenden Lektionsabschnitte gefunden. Versuche es mit anderen Begriffen.
          </div>

        </div>
      </div>
    </Teleport>
  </div>
</template>

<script setup>
import { ref, computed, nextTick } from 'vue'
import { withBase } from 'vitepress'
import { ACTIVE_LOCALES } from '../../languages.mjs'

const isOpen = ref(false)
const query = ref('')
const isLoading = ref(false)
const hasSearched = ref(false)
const results = ref([])
const searchInput = ref(null)
const workerStatus = ref('') // 'loading_model' | 'ready' | 'fallback'
const searchMethod = ref('') // 'vector' | 'hybrid'

let vectorIndex = null
let loadedLocale = ''
let worker = null

function getActiveLocale() {
  if (typeof window === 'undefined') return 'de'
  const base = (import.meta.env.BASE_URL || '/').replace(/\/$/, '')
  const pathname = base && window.location.pathname.startsWith(base)
    ? window.location.pathname.slice(base.length)
    : window.location.pathname
  const seg = pathname.split('/').filter(Boolean)[0] || ''
  return (seg && seg !== 'de' && ACTIVE_LOCALES.includes(seg)) ? seg : 'de'
}

const workerStatusLabel = computed(() => {
  if (workerStatus.value === 'ready') return 'KI-Modell bereit'
  if (workerStatus.value === 'loading_model') return 'Modell lädt...'
  if (workerStatus.value === 'fallback') return 'Hybrid-Modus'
  return ''
})

function initWorker() {
  if (typeof window === 'undefined' || !window.Worker || worker) return
  try {
    worker = new Worker(withBase('/search-worker.js'), { type: 'module' })
    worker.onmessage = (e) => {
      const data = e.data || {}
      if (data.type === 'STATUS') {
        workerStatus.value = data.status
      } else if (data.type === 'RESULTS') {
        results.value = data.results || []
        searchMethod.value = data.method || 'vector'
        isLoading.value = false
      }
    }
    worker.postMessage({ type: 'INIT' })
  } catch (err) {
    console.warn('[PayerSearch] Worker initialization failed, using in-thread search:', err)
    workerStatus.value = 'fallback'
  }
}

async function loadIndex() {
  const currentLocale = getActiveLocale()
  if (vectorIndex && loadedLocale === currentLocale) return

  const primaryUrl = withBase(currentLocale === 'de' ? '/vector_index.json' : `/vector_index_${currentLocale}.json`)
  try {
    let resp = await fetch(primaryUrl)
    if (!resp.ok && currentLocale !== 'de') {
      // Fallback to German index if language-specific index is missing
      resp = await fetch(withBase('/vector_index.json'))
    }
    if (resp.ok) {
      const data = await resp.json()
      vectorIndex = data.records || []
      loadedLocale = currentLocale
    }
  } catch (e) {
    console.warn('Vektorindex konnte nicht geladen werden:', e)
  }
}

function openModal() {
  isOpen.value = true
  initWorker()
  loadIndex()
  nextTick(() => {
    if (searchInput.value) searchInput.value.focus()
  })
}

function closeModal() {
  isOpen.value = false
}

function setQuery(qText) {
  query.value = qText
  performSearch()
}

// In-thread hybrid search fallback if worker is unavailable
function inThreadSearch(q) {
  const qTokens = q.toLowerCase().split(/\s+/).filter(w => w.length > 1)
  const scored = []

  for (const record of (vectorIndex || [])) {
    const heading = (record.heading || '').toLowerCase()
    const snippet = (record.snippet || '').toLowerCase()
    let matched = 0
    let bonus = 0

    for (const t of qTokens) {
      if (heading.includes(t)) {
        matched++
        bonus += 0.25
      } else if (snippet.includes(t)) {
        matched++
      }
    }

    if (matched > 0) {
      const ratio = matched / qTokens.length
      const sim = Math.min(0.95, 0.45 + (ratio * 0.35) + bonus)
      scored.push({ ...record, score: sim })
    }
  }

  scored.sort((a, b) => b.score - a.score)
  results.value = scored.slice(0, 5)
  searchMethod.value = 'hybrid'
  isLoading.value = false
}

async function performSearch() {
  if (!query.value.trim()) return
  isLoading.value = true
  hasSearched.value = true
  results.value = []

  await loadIndex()

  if (!vectorIndex || vectorIndex.length === 0) {
    isLoading.value = false
    return
  }

  // Delegate search to Web Worker
  if (worker) {
    worker.postMessage({
      type: 'SEARCH',
      query: query.value.trim(),
      records: vectorIndex,
      lang: loadedLocale
    })

    // Safety timeout: fall back to in-thread scoring if worker doesn't respond in 4s
    setTimeout(() => {
      if (isLoading.value) {
        inThreadSearch(query.value.trim())
      }
    }, 4000)
  } else {
    inThreadSearch(query.value.trim())
  }
}

function formatFileName(filename) {
  return filename.replace('.md', '').toUpperCase()
}

function getBadgeColor(score) {
  if (score >= 0.7) return '#10b981' // Green
  if (score >= 0.4) return '#f59e0b' // Yellow
  return '#48626e' // Slate
}

function navigateTo(item) {
  closeModal()
  const cleanName = item.file.replace('.md', '')
  const locale = getActiveLocale()
  const prefix = (locale && locale !== 'de') ? `/${locale}` : ''
  window.location.href = withBase(`${prefix}/lektionen/${cleanName}`)
}
</script>

<style scoped>
.payer-semantic-search-btn {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  background: var(--vp-c-bg-soft, #f1eee7);
  border: 1px solid var(--vp-c-divider, #e2e8f0);
  border-radius: 20px;
  padding: 4px 12px;
  font-size: 13px;
  font-weight: 600;
  color: var(--vp-c-text-1, #03192e);
  cursor: pointer;
  transition: all 0.2s ease;
}

.payer-semantic-search-btn:hover {
  border-color: #48626e;
  background: #e2e8f0;
}

.payer-semantic-modal-backdrop {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background: rgba(3, 25, 46, 0.6);
  backdrop-filter: blur(6px);
  z-index: 9999;
  display: flex;
  justify-content: center;
  align-items: flex-start;
  padding-top: 10vh;
}

.payer-semantic-modal {
  background: #fcf9f2;
  border: 1px solid #48626e;
  border-radius: 12px;
  width: 90%;
  max-width: 650px;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.25);
  padding: 24px;
  color: #03192e;
}

.payer-semantic-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 16px;
}

.brain-badge {
  font-size: 16px;
  font-weight: 700;
  color: #03192e;
}

.subtitle {
  font-size: 12px;
  color: #48626e;
  margin: 4px 0 0 0;
}

.close-btn {
  background: none;
  border: none;
  font-size: 24px;
  color: #48626e;
  cursor: pointer;
}

.header-status {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  font-size: 11px;
  font-weight: 600;
  color: #48626e;
  margin-left: auto;
  margin-right: 12px;
  padding: 3px 8px;
  background: #f1eee7;
  border-radius: 12px;
}

.status-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  display: inline-block;
}

.status-dot.ready {
  background: #10b981;
  box-shadow: 0 0 6px rgba(16, 185, 129, 0.5);
}

.status-dot.loading_model {
  background: #f59e0b;
  animation: pulse 1.5s infinite;
}

.status-dot.fallback {
  background: #64748b;
}

@keyframes pulse {
  0%, 100% { opacity: 1; transform: scale(1); }
  50% { opacity: 0.4; transform: scale(0.85); }
}

.payer-semantic-input-wrap {
  display: flex;
  gap: 8px;
  margin-bottom: 12px;
}

.payer-semantic-input {
  flex: 1;
  background: #ffffff;
  border: 1px solid #48626e;
  border-radius: 8px;
  padding: 10px 14px;
  font-size: 14px;
  color: #03192e;
  outline: none;
}

.action-search-btn {
  background: #03192e;
  color: #fcf9f2;
  border: none;
  border-radius: 8px;
  padding: 0 18px;
  font-weight: 600;
  cursor: pointer;
}

.payer-quick-queries {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 18px;
  flex-wrap: wrap;

  font-size: 12px;
}

.payer-quick-queries .label {
  color: #48626e;
}

.payer-quick-queries button {
  background: #f1eee7;
  border: 1px solid #48626e;
  border-radius: 12px;
  padding: 2px 10px;
  font-size: 12px;
  cursor: pointer;
  color: #03192e;
}

.payer-semantic-card {
  background: #ffffff;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  padding: 14px;
  margin-bottom: 10px;
  cursor: pointer;
  transition: transform 0.15s ease, border-color 0.15s ease;
}

.payer-semantic-card:hover {
  transform: translateY(-1px);
  border-color: #03192e;
}

.card-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 6px;
}

.match-badge {
  color: #ffffff;
  font-size: 11px;
  font-weight: 700;
  padding: 2px 8px;
  border-radius: 10px;
}

.file-tag {
  font-size: 11px;
  color: #48626e;
  font-weight: 600;
}

.card-title {
  font-family: serif;
  font-size: 16px;
  font-weight: 700;
  margin: 0 0 4px 0;
}

.card-snippet {
  font-size: 13px;
  color: #48626e;
  margin: 0;
  line-height: 1.4;
}
</style>
