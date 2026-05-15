<template>
  <button 
    class="wide-toggle" 
    :class="{ 'is-active': isWide }" 
    @click="toggleWide"
    title="Breit-Modus umschalten"
  >
    <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
      <polyline points="15 3 21 3 21 9"></polyline>
      <polyline points="9 21 3 21 3 15"></polyline>
      <line x1="21" y1="3" x2="14" y2="10"></line>
      <line x1="3" y1="21" x2="10" y2="14"></line>
    </svg>
  </button>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const isWide = ref(false)

const toggleWide = () => {
  const scrollPos = window.scrollY
  isWide.value = !isWide.value
  if (isWide.value) {
    document.documentElement.classList.add('is-wide')
    localStorage.setItem('payer_wide_mode', 'true')
  } else {
    document.documentElement.classList.remove('is-wide')
    localStorage.setItem('payer_wide_mode', 'false')
  }
  // Restore scroll position after layout shift
  requestAnimationFrame(() => {
    window.scrollTo({ top: scrollPos, behavior: 'auto' })
  })
}

onMounted(() => {
  const saved = localStorage.getItem('payer_wide_mode')
  if (saved === 'true') {
    isWide.value = true
    document.documentElement.classList.add('is-wide')
  }
})
</script>

<style scoped>
.wide-toggle {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 36px;
  height: 36px;
  border-radius: 4px;
  color: var(--vp-c-text-2);
  transition: color 0.25s, background-color 0.25s;
  background: transparent;
  border: none;
  cursor: pointer;
  margin-left: 8px;
}

.wide-toggle:hover {
  color: var(--vp-c-text-1);
  background-color: var(--vp-c-bg-soft);
}

.wide-toggle.is-active {
  color: var(--vp-c-brand-1);
  background-color: var(--vp-c-brand-soft);
}

@media (max-width: 959px) {
  .wide-toggle {
    display: none;
  }
}
</style>
