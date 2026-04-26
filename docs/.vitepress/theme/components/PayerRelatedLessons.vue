<script setup>
import { computed } from 'vue'
import { useData } from 'vitepress'
import { data } from '../data/topics.data.mjs'

const { page } = useData()

const currentLessonNumber = computed(() => {
  const match = page.value.relativePath.match(/lektion(\d+)/)
  return match ? parseInt(match[1]) : null
})

const currentLocale = computed(() => {
  const path = page.value.relativePath
  if (path.startsWith('en/')) return 'en'
  if (path.startsWith('it/')) return 'it'
  if (path.startsWith('es/')) return 'es'
  if (path.startsWith('bg/')) return 'bg'
  return 'root'
})

const relatedLessons = computed(() => {
  if (!currentLessonNumber.value) return []

  // Find topics for current lesson
  const currentTopics = []
  for (const [topic, lessons] of Object.entries(data.topicMap)) {
    if (lessons.includes(currentLessonNumber.value)) {
      currentTopics.push(topic)
    }
  }

  // Find other lessons sharing these topics
  const relatedMap = {}
  currentTopics.forEach(topic => {
    data.topicMap[topic].forEach(num => {
      if (num !== currentLessonNumber.value) {
        relatedMap[num] = (relatedMap[num] || 0) + 1
      }
    })
  })

  // Sort by shared topic count and get top 3
  const sortedIds = Object.keys(relatedMap)
    .sort((a, b) => relatedMap[b] - relatedMap[a])
    .slice(0, 3)
    .map(id => parseInt(id))

  return sortedIds.map(num => {
    // Basic title generation for cards
    // In a real app, we might want to fetch the actual titles from the index
    return {
      number: num,
      link: getLocalizedLink(num)
    }
  })
})

function getLocalizedLink(num) {
  const padded = num.toString().padStart(2, '0')
  const prefix = currentLocale.value === 'root' ? '' : `/${currentLocale.value}`
  return `${prefix}/lektionen/lektion${padded}`
}

function getLabel(num) {
  const labels = {
    root: 'Lektion',
    en: 'Lesson',
    it: 'Lezione',
    es: 'Lección',
    bg: 'Урок'
  }
  return labels[currentLocale.value] || 'Lesson'
}

function getHeading() {
  const headings = {
    root: 'Verwandte Themen',
    en: 'Related Topics',
    it: 'Argomenti correlati',
    es: 'Temas relacionados',
    bg: 'Свързани теми'
  }
  return headings[currentLocale.value] || 'Related Topics'
}
</script>

<template>
  <div v-if="relatedLessons.length > 0" class="related-container">
    <h3 class="related-heading">{{ getHeading() }}</h3>
    <div class="related-grid">
      <a v-for="lesson in relatedLessons" 
         :key="lesson.number" 
         :href="lesson.link" 
         class="related-card">
        <div class="card-label">{{ getLabel(lesson.number) }} {{ lesson.number }}</div>
        <div class="card-arrow">→</div>
      </a>
    </div>
  </div>
</template>

<style scoped>
.related-container {
  margin-top: 4rem;
  padding-top: 2rem;
  border-top: 1px solid var(--vp-c-divider);
}

.related-heading {
  font-family: 'Newsreader', serif;
  font-style: italic;
  font-size: 1.5rem;
  margin-bottom: 1.5rem;
  color: var(--vp-c-text-2);
}

.related-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 1rem;
}

.related-card {
  background: var(--vp-c-bg-soft);
  padding: 1.5rem;
  border-radius: 12px;
  text-decoration: none;
  display: flex;
  justify-content: space-between;
  align-items: center;
  transition: all 0.3s ease;
}

.related-card:hover {
  background: var(--vp-c-brand-soft);
  transform: translateY(-4px);
}

.card-label {
  font-family: 'Inter', sans-serif;
  font-weight: 600;
  color: var(--vp-c-text-1);
}

.card-arrow {
  color: var(--vp-c-brand);
  font-weight: bold;
}
</style>
