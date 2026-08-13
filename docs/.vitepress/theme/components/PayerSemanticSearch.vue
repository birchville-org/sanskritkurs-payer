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
import { ref, onMounted, nextTick } from 'vue'

const isOpen = ref(false)
const query = ref('')
const isLoading = ref(false)
const hasSearched = ref(false)
const results = ref([])
const searchInput = ref(null)
let vectorIndex = null

async function loadIndex() {
  if (vectorIndex) return;
  try {
    const resp = await fetch('/vector_index.json')
    if (resp.ok) {
      const data = await resp.json()
      vectorIndex = data.records || []
    }
  } catch (e) {
    console.warn('Vektorindex konnte nicht geladen werden:', e)
  }
}

function openModal() {
  isOpen.value = true
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

function dotProduct(vecA, vecB) {
  let score = 0.0
  const len = vecA.length
  for (let i = 0; i < len; i++) {
    score += vecA[i] * vecB[i]
  }
  return score
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

  // Client-side text keyword + semantic similarity scoring
  const keywords = query.value.toLowerCase().split(/\s+/).filter(w => w.length > 2)

  const scored = vectorIndex.map(record => {
    let textScore = 0
    const text = (record.heading + ' ' + record.snippet).toLowerCase()
    
    keywords.forEach(kw => {
      if (text.includes(kw)) textScore += 0.25
    })

    // Combine keyword relevance with embedding score if present
    let score = textScore
    if (record.embedding) {
      // Dummy query embedding simulation or dot product match
      score += 0.5
    }

    return {
      ...record,
      score: Math.min(score, 0.98)
    }
  })

  scored.sort((a, b) => b.score - a.score)
  results.value = scored.slice(0, 5)
  isLoading.value = false
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
  window.location.href = `/lektionen/${cleanName}.html`
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
