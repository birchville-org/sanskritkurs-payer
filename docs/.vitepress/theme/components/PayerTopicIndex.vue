<script setup>
import { useRoute } from 'vitepress'
import { useData } from 'vitepress'
import { computed } from 'vue'
import { data } from '../../data/topics.data.js'

const route = useRoute()

const LOCALES = ['en','it','es','fr','hi','bg','ru','uk','ta','pa','la','rm','ro']

const langPrefix = computed(() => {
  const first = route.path.split('/').filter(Boolean)[0]
  return LOCALES.includes(first) ? `/${first}` : ''
})

const localeCode = computed(() => {
  const first = route.path.split('/').filter(Boolean)[0]
  return LOCALES.includes(first) ? first : ''
})

// Use locale-specific topic map
const topicMap = computed(() => {
  return data.localeTopicMap[localeCode.value] || data.topicMap
})

const topicList = computed(() => {
  return Object.keys(topicMap.value).sort((a, b) => a.localeCompare(b))
})

function cleanTopicStart(topic) {
  if (!topic) return ''
  // Remove leading quotes, backslashes, and whitespace
  return topic.trim().replace(/^[\\"'„“«»‘’\s]+/, '')
}

function getBaseChar(char) {
  if (!char) return ''
  // Normalize accents (e.g. À -> A) and cleanup whitespace
  const normalized = char.normalize("NFD").replace(/[\u0300-\u036f]/g, "")
  return normalized.toUpperCase().trim()
}

// Group topics dynamically by their actual starting letters (supports Cyrillic, Hindi, Tamil, Gurmukhi, Hebrew, Arabic etc.)
const alphabetList = computed(() => {
  const letters = new Set()
  for (const topic of topicList.value) {
    const cleaned = cleanTopicStart(topic)
    if (cleaned) {
      const firstChar = cleaned.charAt(0)
      const baseChar = getBaseChar(firstChar)
      if (baseChar) {
        letters.add(baseChar)
      }
    }
  }
  return Array.from(letters).sort((a, b) => a.localeCompare(b, localeCode.value || 'de'))
})

const groupedTopics = computed(() => {
  return alphabetList.value.reduce((acc, letter) => {
    const matches = topicList.value.filter(t => {
      const cleaned = cleanTopicStart(t)
      if (!cleaned) return false
      const first = cleaned.charAt(0)
      return getBaseChar(first) === letter
    })
    if (matches.length > 0) {
      acc.push({ letter, matches })
    }
    return acc
  }, [])
})

function getLessonLink(num) {
  const padded = num.toString().padStart(2, '0');
  return `${langPrefix.value}/lektionen/lektion${padded}`;
}

function formatTopic(content) {
  if (!content) return '';
  const SANSKRIT_RE = /[⟪《]([^⟫⟩》]+)[⟫⟩》]/g;
  const SIG_RE = /sig\[(.*?)\]/g;
  let html = content.replace(SANSKRIT_RE, '<span class="sanskrit-dev" translate="no" lang="sa">$1</span>');
  html = html.replace(SIG_RE, '<strong class="signalrot">$1</strong>');
  return html;
}
</script>

<template>
  <div class="topic-index">
    <nav class="alpha-nav">
      <a v-for="group in groupedTopics" :key="group.letter" :href="'#' + group.letter">
        {{ group.letter }}
      </a>
    </nav>

    <div v-for="group in groupedTopics" :key="group.letter" class="letter-group">
      <h2 :id="group.letter">{{ group.letter }}</h2>
      <ul class="topic-list">
        <li v-for="topic in group.matches" :key="topic" class="topic-item">
          <span class="topic-name" v-html="formatTopic(topic)"></span>
          <div class="lesson-links">
            <a v-for="num in topicMap[topic]" 
               :key="num" 
               :href="getLessonLink(num)" 
               class="lesson-tag">
              L{{ num }}
            </a>
          </div>
        </li>
      </ul>
    </div>
  </div>
</template>

<style scoped>
.topic-index {
  margin-top: 2rem;
}

.alpha-nav {
  position: sticky;
  top: var(--vp-nav-height);
  background: var(--vp-c-bg);
  padding: 1rem 0;
  z-index: 10;
  display: flex;
  flex-wrap: wrap;
  gap: 0.8rem;
  border-bottom: 1px solid var(--vp-c-divider);
  margin-bottom: 2rem;
}

.alpha-nav a {
  font-weight: bold;
  font-size: 0.9rem;
  color: var(--vp-c-brand);
  text-decoration: none;
}

.alpha-nav a:hover {
  text-decoration: underline;
}

.letter-group h2 {
  border-bottom: none;
  font-family: var(--vp-font-family-base);
  font-weight: 700;
  color: var(--vp-c-brand);
  margin-top: 3rem;
  font-size: 2rem;
}

.topic-list {
  list-style: none;
  padding: 0;
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 1.5rem;
}

.topic-item {
  background: var(--vp-c-bg-soft);
  padding: 1.2rem;
  border-radius: 12px;
  display: flex;
  flex-direction: column;
  gap: 0.8rem;
  transition: all 0.3s ease;
}

.topic-item:hover {
  background: var(--vp-c-bg-mute);
  transform: translateY(-2px);
}

.topic-name {
  font-family: 'Newsreader', serif;
  font-size: 1.25rem;
  font-weight: 600;
  line-height: 1.2;
}

.lesson-links {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.lesson-tag {
  background: var(--vp-c-brand-soft);
  color: var(--vp-c-brand);
  padding: 0.2rem 0.6rem;
  border-radius: 4px;
  font-size: 0.8rem;
  text-decoration: none;
  font-family: var(--vp-font-family-mono);
  font-weight: bold;
}

.lesson-tag:hover {
  background: var(--vp-c-brand);
  color: white;
}
</style>
