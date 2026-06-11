<template>
  <div class="width-selector" ref="selectorRef">
    <button
      class="width-btn"
      :title="'Textbreite: ' + current.label"
      @click="toggle"
    >
      <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none"
        stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <polyline points="15 3 21 3 21 9"></polyline>
        <polyline points="9 21 3 21 3 15"></polyline>
        <line x1="21" y1="3" x2="14" y2="10"></line>
        <line x1="3" y1="21" x2="10" y2="14"></line>
      </svg>
      <span class="width-label">{{ current.label }}</span>
    </button>
    <div v-if="open" class="width-dropdown">
      <button
        v-for="step in steps"
        :key="step.value"
        class="width-option"
        :class="{ active: step.value === currentValue }"
        @click="select(step)"
      >
        <span class="option-bar" :style="'width:' + step.barWidth"></span>
        {{ step.label }}
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'

const steps = [
  { value: 'max', label: 'Max',  barWidth: '100%' },
  { value: '75',  label: '75%',  barWidth: '75%'  },
  { value: '50',  label: '50%',  barWidth: '50%'  },
  { value: '25',  label: '25%',  barWidth: '25%'  },
  { value: 'min', label: 'Min',  barWidth: '12%'  },
]

const currentValue = ref('min')
const open = ref(false)
const selectorRef = ref(null)

const current = computed(() => steps.find(s => s.value === currentValue.value) || steps[4])

function applyWidth(value) {
  const scrollPos = window.scrollY
  document.documentElement.setAttribute('data-width', value)
  // Backwards compat: keep is-wide in sync
  if (value === 'max') {
    document.documentElement.classList.add('is-wide')
  } else {
    document.documentElement.classList.remove('is-wide')
  }
  requestAnimationFrame(() => window.scrollTo({ top: scrollPos, behavior: 'auto' }))
}

function select(step) {
  currentValue.value = step.value
  applyWidth(step.value)
  localStorage.setItem('payer_width_step', step.value)
  open.value = false
}

function toggle() {
  open.value = !open.value
}

function onOutsideClick(e) {
  if (selectorRef.value && !selectorRef.value.contains(e.target)) {
    open.value = false
  }
}

onMounted(() => {
  // Migrate legacy payer_wide_mode
  const legacy = localStorage.getItem('payer_wide_mode')
  const saved = localStorage.getItem('payer_width_step')
  const initial = saved || (legacy === 'true' ? 'max' : 'min')
  currentValue.value = initial
  applyWidth(initial)
  document.addEventListener('click', onOutsideClick)
})

onUnmounted(() => {
  document.removeEventListener('click', onOutsideClick)
})
</script>

<style scoped>
.width-selector {
  position: relative;
  display: flex;
  align-items: center;
  margin-left: 4px;
}

.width-btn {
  display: flex;
  align-items: center;
  gap: 4px;
  height: 36px;
  padding: 0 8px;
  border-radius: 4px;
  color: var(--vp-c-text-2);
  background: transparent;
  border: none;
  cursor: pointer;
  transition: color 0.25s, background-color 0.25s;
  white-space: nowrap;
}

.width-btn:hover {
  color: var(--vp-c-text-1);
  background-color: var(--vp-c-bg-soft);
}

.width-label {
  font-size: 0.78rem;
  font-family: 'Inter', sans-serif;
  font-weight: 500;
  min-width: 22px;
}

.width-dropdown {
  position: absolute;
  top: calc(100% + 6px);
  right: 0;
  background: var(--vp-c-bg-elv);
  border: 1px solid var(--vp-c-divider);
  border-radius: 8px;
  box-shadow: 0 4px 16px rgba(0,0,0,0.12);
  z-index: 1000;
  min-width: 120px;
  padding: 4px;
  overflow: hidden;
}

.width-option {
  display: flex;
  align-items: center;
  gap: 10px;
  width: 100%;
  padding: 7px 12px;
  border: none;
  background: transparent;
  cursor: pointer;
  font-size: 0.85rem;
  font-family: 'Inter', sans-serif;
  color: var(--vp-c-text-1);
  border-radius: 4px;
  transition: background 0.15s;
  text-align: left;
}

.width-option:hover {
  background: var(--vp-c-bg-soft);
}

.width-option.active {
  color: var(--vp-c-brand-1);
  font-weight: 600;
}

.option-bar {
  display: inline-block;
  height: 3px;
  background: currentColor;
  border-radius: 2px;
  min-width: 4px;
  flex-shrink: 0;
  max-width: 60px;
}

@media (max-width: 959px) {
  .width-selector { display: none; }
}
</style>
