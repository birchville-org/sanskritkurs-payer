<script setup>
import { ref, onMounted, onUnmounted } from 'vue'

const offline = ref(false)
const syncing = ref(false)

function updateOnlineStatus() {
  offline.value = !navigator.onLine
}

// Listen for prefetch progress from SW
onMounted(() => {
  if (typeof navigator !== 'undefined') {
    offline.value = !navigator.onLine
    window.addEventListener('online', updateOnlineStatus)
    window.addEventListener('offline', updateOnlineStatus)
    
    // Listen for SW prefetch progress events
    if (navigator.serviceWorker) {
      navigator.serviceWorker.addEventListener('message', (event) => {
        if (event.data?.type === 'PREFETCH_PROGRESS' ||
            event.data?.type === 'PREFETCH_BATCH_PROGRESS') {
          syncing.value = true
        }
        if (event.data?.type === 'PREFETCH_COMPLETE' ||
            event.data?.type === 'PREFETCH_BATCH_COMPLETE') {
          syncing.value = false
        }
      })
    }
  }
})

onUnmounted(() => {
  if (typeof window !== 'undefined') {
    window.removeEventListener('online', updateOnlineStatus)
    window.removeEventListener('offline', updateOnlineStatus)
  }
})
</script>

<template>
  <div v-if="offline || syncing" class="payer-offline-banner" role="alert">
    <span class="payer-offline-icon">{{ syncing ? '🔄' : '⚠' }}</span>
    <span class="payer-offline-text">
      {{ syncing ? 'Synchronisiere…' : 'Offline — Inhalte werden aus dem Cache geladen' }}
    </span>
  </div>
</template>

<style scoped>
.payer-offline-banner {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 16px;
  font-size: 0.8125rem;
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
  background: var(--vp-c-parchment, #fcf9f2);
  color: var(--vp-c-slate, #48626e);
  border-bottom: 1px solid var(--vp-c-divider, #e8e4d8);
  text-align: center;
  justify-content: center;
  position: relative;
  z-index: 100;
}

.payer-offline-icon {
  font-size: 1rem;
  opacity: 0.7;
}

.payer-offline-text {
  font-weight: 500;
}
</style>
