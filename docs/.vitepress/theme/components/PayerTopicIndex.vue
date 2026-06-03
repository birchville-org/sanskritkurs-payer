<script setup>
import { useData } from 'vitepress'
import { computed } from 'vue'
import { data } from '../data/topics.data.mjs'

const { localeIndex } = useData()

// localeIndex is 'root' for DE, 'ta', 'ro', 'la' etc. for other locales
const langPrefix = computed(() =>
  localeIndex.value === 'root' ? '' : `/${localeIndex.value}`
)

// Group topics by their first letter
const alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ".split("");
const groupedTopics = alphabet.reduce((acc, letter) => {
  const matches = data.topics.filter(t => t.toUpperCase().startsWith(letter));
  if (matches.length > 0) {
    acc.push({ letter, matches });
  }
  return acc;
}, []);

// Add Devanagari / Special group for everything else
const otherMatches = data.topics.filter(t => {
  const first = t.charAt(0).toUpperCase();
  return !alphabet.includes(first);
});

if (otherMatches.length > 0) {
  groupedTopics.push({ letter: "Saṃskṛtam", matches: otherMatches });
}

function getLessonLink(num) {
  const padded = num.toString().padStart(2, '0');
  return `${langPrefix.value}/lektionen/lektion${padded}`;
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
          <span class="topic-name">{{ topic }}</span>
          <div class="lesson-links">
            <a v-for="num in data.topicMap[topic]" 
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
