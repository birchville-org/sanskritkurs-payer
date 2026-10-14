<script setup>
import { ref, computed, watch, nextTick, onMounted, onUnmounted } from 'vue'
import { withBase, useRoute } from 'vitepress'
import { ACTIVE_LOCALES } from '../../languages.mjs'

const route = useRoute()
const isOpen = ref(false)
const toggleBtnRef = ref(null)
const closeBtnRef = ref(null)

const currentLang = computed(() => {
  const path = route.path || (typeof window !== 'undefined' ? window.location.pathname : '')
  const parts = path.split('/').filter(Boolean)
  if (parts.length > 0 && ACTIVE_LOCALES.includes(parts[0])) {
    return parts[0]
  }
  return 'de'
})

const isEn = computed(() => currentLang.value !== 'de')

function open() {
  isOpen.value = true
  nextTick(() => {
    closeBtnRef.value?.focus()
  })
}

function close(restoreFocus = true) {
  if (!isOpen.value) return
  isOpen.value = false
  if (restoreFocus) {
    nextTick(() => {
      toggleBtnRef.value?.focus()
    })
  }
}

function toggle() {
  if (isOpen.value) {
    close(true)
  } else {
    open()
  }
}

// Close drawer on route change (without focus restore)
watch(() => route.path, () => close(false))

function handleKeydown(e) {
  if (e.key === 'Escape' && isOpen.value) {
    close()
  }
}

onMounted(() => {
  window.addEventListener('keydown', handleKeydown)
})

onUnmounted(() => {
  window.removeEventListener('keydown', handleKeydown)
})

const navLinks = computed(() => {
  const l = currentLang.value
  const prefix = l === 'de' ? '' : `/${l}`
  const qaUrl = `/qa_viewer.html?lang=${l}`

  if (l === 'de') {
    return [
      { text: 'Startseite', href: withBase('/'), badge: 'Kurs' },
      { text: 'Inhaltsverzeichnis', href: withBase('/lektionen/inhaltsverzeichnis'), badge: 'Gliederung' },
      { text: 'Grammatik-Themen', href: withBase('/grammatik'), badge: 'Systematik' },
      { text: 'Grammatik-Index', href: withBase('/themen'), badge: 'Index' },
      { text: 'Wortliste', href: withBase('/lektionen/wortliste'), badge: 'Vokabeln' },
      { text: 'QA-Viewer', href: qaUrl, target: '_blank', badge: 'Tools' },
      { text: 'Einstellungen', href: withBase('/settings'), badge: 'Optionen' },
      { text: 'Impressum & Zitieren', href: withBase('/impressum'), badge: 'Rechtliches' },
      { text: 'GitHub Repository', href: 'https://github.com/birchville-org/sanskritkurs-payer', target: '_blank', badge: 'Code' }
    ]
  }

  return [
    { text: 'Home', href: withBase(`${prefix}/`), badge: 'Course' },
    { text: 'Table of Contents', href: withBase(`${prefix}/lektionen/inhaltsverzeichnis`), badge: 'Syllabus' },
    { text: 'Grammar Topics', href: withBase(`${prefix}/grammatik`), badge: 'Topics' },
    { text: 'Grammar Index', href: withBase(`${prefix}/themen`), badge: 'Index' },
    { text: 'Word List', href: withBase(`${prefix}/lektionen/wortliste`), badge: 'Vocab' },
    { text: 'QA Viewer', href: qaUrl, target: '_blank', badge: 'Tools' },
    { text: 'Settings', href: withBase(`${prefix}/settings`), badge: 'Options' },
    { text: 'Legal Notice & Citation', href: withBase(`${prefix}/impressum`), badge: 'Legal' },
    { text: 'GitHub Repository', href: 'https://github.com/birchville-org/sanskritkurs-payer', target: '_blank', badge: 'Code' }
  ]
})
</script>

<template>
  <div class="bv-drawer-wrapper">
    <!-- Hairline Divider before Hamburger -->
    <span class="bv-nav-divider" aria-hidden="true"></span>

    <!-- Universal Hamburger Toggle Button -->
    <button
      ref="toggleBtnRef"
      type="button"
      class="bv-hamburger-btn"
      :class="{ 'is-active': isOpen }"
      :aria-expanded="isOpen"
      :aria-label="isEn ? (isOpen ? 'Close menu' : 'Open menu') : (isOpen ? 'Menü schliessen' : 'Menü öffnen')"
      @click="toggle"
    >
      <span class="bv-hamburger-box">
        <span class="bv-bar bar-top"></span>
        <span class="bv-bar bar-mid"></span>
        <span class="bv-bar bar-bot"></span>
      </span>
    </button>

    <!-- Slide-over Drawer Teleported to Body -->
    <Teleport to="body">
      <div
        class="bv-drawer-backdrop"
        :class="{ 'is-open': isOpen }"
        aria-hidden="true"
        @click="close(true)"
      ></div>

      <aside
        class="bv-drawer-panel"
        :class="{ 'is-open': isOpen }"
        :aria-hidden="!isOpen"
        :inert="!isOpen ? true : undefined"
        role="dialog"
        aria-modal="true"
        :aria-label="isEn ? 'Navigation Menu' : 'Navigationsmenü'"
      >
        <!-- Drawer Header with Birchville Coat of Arms -->
        <div class="bv-drawer-header">
          <div class="bv-drawer-brand">
            <img :src="withBase('/birchville_logo.png')" alt="Birchville" class="bv-drawer-logo" />
            <div class="bv-drawer-brand-text">
              <span class="bv-brand-title">Sanskritkurs</span>
              <span class="bv-brand-sub">{{ isEn ? 'Alois Payer · Textbook' : 'Alois Payer · Lehrbuch' }}</span>
            </div>
          </div>
          <button
            ref="closeBtnRef"
            type="button"
            class="bv-drawer-close"
            :aria-label="isEn ? 'Close menu' : 'Menü schliessen'"
            @click="close(true)"
          >
            &times;
          </button>
        </div>

        <!-- Navigation Links -->
        <nav class="bv-drawer-nav">
          <div class="bv-nav-section-title">{{ isEn ? 'COURSE NAVIGATION' : 'KURS-NAVIGATION' }}</div>
          <ul>
            <li v-for="item in navLinks" :key="item.text">
              <a
                :href="item.href"
                :target="item.target || null"
                :rel="item.target ? 'noopener noreferrer' : null"
                @click="close(false)"
              >
                <span class="bv-link-text">{{ item.text }}</span>
                <span v-if="item.badge" class="bv-link-badge">{{ item.badge }}</span>
                <span class="bv-link-arrow" aria-hidden="true">&rarr;</span>
              </a>
            </li>
          </ul>
        </nav>

        <!-- Secondary Cross-Project Links -->
        <div class="bv-drawer-secondary">
          <div class="bv-nav-section-title">{{ isEn ? 'BIRCHVILLE NETWORK' : 'BIRCHVILLE NETZWERK' }}</div>
          <ul>
            <li>
              <a href="https://birchville.org" target="_blank" rel="noopener">
                <span>Birchville Homelab Portal</span>
                <span class="bv-link-arrow">&rarr;</span>
              </a>
            </li>
            <li>
              <a href="https://birchville-org.github.io/dhatupatha/" target="_blank" rel="noopener">
                <span>Pāṇinīya-Dhātupāṭha (2.259 Wurzeln)</span>
                <span class="bv-link-arrow">&rarr;</span>
              </a>
            </li>
            <li>
              <a href="https://birchville-org.github.io/boethlingk/" target="_blank" rel="noopener">
                <span>Böhtlingk: Pāṇini-Grammatik</span>
                <span class="bv-link-arrow">&rarr;</span>
              </a>
            </li>
            <li>
              <a href="https://birchville-org.github.io/HeritageDictionnaire/" target="_blank" rel="noopener">
                <span>Héritage du Sanskrit Dictionnaire</span>
                <span class="bv-link-arrow">&rarr;</span>
              </a>
            </li>
          </ul>
        </div>

        <!-- Footer in Drawer -->
        <div class="bv-drawer-footer">
          <div class="bv-drawer-copy">&copy; 2026 Birchville · Scholarly Synthesis</div>
        </div>
      </aside>
    </Teleport>
  </div>
</template>

<style scoped>
.bv-drawer-wrapper {
  display: inline-flex;
  align-items: center;
  position: relative;
  z-index: 25;
}

.bv-nav-divider {
  display: inline-block;
  width: 1px;
  height: 20px;
  background-color: var(--vp-c-divider);
  margin: 0 8px 0 4px;
}

/* Hamburger Button */
.bv-hamburger-btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 36px;
  height: 36px;
  padding: 0;
  border: 1px solid var(--vp-c-border);
  border-radius: 6px;
  background: var(--vp-c-bg-soft);
  cursor: pointer;
  transition: all 0.18s ease;
}

.bv-hamburger-btn:hover {
  background: var(--vp-c-brand-soft);
  border-color: var(--vp-c-brand-1);
}

.bv-hamburger-box {
  position: relative;
  width: 16px;
  height: 12px;
  display: block;
}

.bv-bar {
  position: absolute;
  left: 0;
  width: 16px;
  height: 1.8px;
  background-color: var(--vp-c-text-1);
  border-radius: 1px;
  transition: transform 0.22s ease, top 0.22s ease, opacity 0.22s ease;
}

.bar-top { top: 0; }
.bar-mid { top: 5px; }
.bar-bot { top: 10px; }

.bv-hamburger-btn.is-active .bar-top {
  top: 5px;
  transform: rotate(45deg);
}

.bv-hamburger-btn.is-active .bar-mid {
  opacity: 0;
  transform: scaleX(0);
}

.bv-hamburger-btn.is-active .bar-bot {
  top: 5px;
  transform: rotate(-45deg);
}

/* Backdrop */
.bv-drawer-backdrop {
  position: fixed;
  inset: 0;
  background: rgba(3, 25, 46, 0.45);
  backdrop-filter: blur(6px);
  -webkit-backdrop-filter: blur(6px);
  z-index: 998;
  opacity: 0;
  pointer-events: none;
  transition: opacity 0.25s ease;
}

.dark .bv-drawer-backdrop {
  background: rgba(6, 14, 26, 0.65);
}

.bv-drawer-backdrop.is-open {
  opacity: 1;
  pointer-events: auto;
}

/* Drawer Panel */
.bv-drawer-panel {
  position: fixed;
  top: 0;
  right: 0;
  bottom: 0;
  width: min(390px, 86vw);
  background-color: var(--vp-c-bg);
  border-left: 1px solid var(--vp-c-border);
  box-shadow: -8px 0 32px rgba(3, 25, 46, 0.16);
  z-index: 999;
  display: flex;
  flex-direction: column;
  overflow-y: auto;
  transform: translateX(100%);
  visibility: hidden;
  transition: transform 0.28s cubic-bezier(0.16, 1, 0.3, 1), visibility 0.28s ease;
}

.dark .bv-drawer-panel {
  box-shadow: -8px 0 32px rgba(0, 0, 0, 0.65);
}

.bv-drawer-panel.is-open {
  transform: translateX(0);
  visibility: visible;
}

/* Drawer Header */
.bv-drawer-header {
  display: flex !important;
  align-items: center !important;
  justify-content: space-between !important;
  padding: 1.1rem 1.4rem !important;
  border-bottom: 1px solid var(--vp-c-border) !important;
  background: var(--vp-c-bg-soft) !important;
}

.bv-drawer-brand {
  display: flex !important;
  align-items: center !important;
  gap: 0.75rem !important;
  min-width: 0 !important;
}

.bv-drawer-logo {
  height: 2.1rem !important;
  max-height: 2.1rem !important;
  width: auto !important;
  max-width: 2.1rem !important;
  flex-shrink: 0 !important;
  object-fit: contain !important;
  border-radius: 4px !important;
  filter: drop-shadow(0 1px 3px rgba(0, 0, 0, 0.18)) !important;
}

.bv-drawer-brand-text {
  display: flex !important;
  flex-direction: column !important;
  min-width: 0 !important;
}

.bv-brand-title {
  font-size: 0.95rem;
  font-weight: 700;
  letter-spacing: -0.01em;
  color: var(--vp-c-text-1);
}

.bv-brand-sub {
  font-size: 0.72rem;
  font-weight: 500;
  color: var(--vp-c-text-3);
  letter-spacing: 0.02em;
}

.bv-drawer-close {
  flex-shrink: 0 !important;
  background: transparent;
  border: 1px solid var(--vp-c-border);
  border-radius: 6px;
  width: 32px;
  height: 32px;
  font-size: 1.25rem;
  line-height: 1;
  color: var(--vp-c-text-2);
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  transition: all 0.15s ease;
}

.bv-drawer-close:hover {
  color: var(--vp-c-brand-1);
  border-color: var(--vp-c-brand-1);
  background: var(--vp-c-bg);
}

/* Nav Section Title */
.bv-nav-section-title {
  font-size: 0.68rem;
  font-weight: 700;
  color: var(--vp-c-text-3);
  letter-spacing: 0.08em;
  text-transform: uppercase;
  padding: 0 0.4rem 0.5rem;
}

/* Drawer Nav */
.bv-drawer-nav {
  padding: 1.4rem 1.4rem 0.8rem;
}

.bv-drawer-nav ul,
.bv-drawer-secondary ul {
  list-style: none;
  padding: 0;
  margin: 0;
  display: flex;
  flex-direction: column;
  gap: 0.35rem;
}

.bv-drawer-nav a,
.bv-drawer-secondary a {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0.65rem 0.85rem;
  border-radius: 6px;
  color: var(--vp-c-text-1);
  text-decoration: none;
  font-size: 0.85rem;
  font-weight: 500;
  transition: all 0.15s ease;
  border: 1px solid transparent;
}

.bv-drawer-nav a:hover,
.bv-drawer-secondary a:hover {
  background-color: var(--vp-c-bg-soft);
  color: var(--vp-c-brand-1);
  border-color: var(--vp-c-border);
  transform: translateX(2px);
}

.bv-link-text {
  flex: 1;
}

.bv-link-badge {
  font-size: 0.68rem;
  font-weight: 600;
  color: var(--vp-c-brand-1);
  background: var(--vp-c-brand-soft);
  padding: 2px 7px;
  border-radius: 4px;
  margin-right: 0.5rem;
  border: 1px solid color-mix(in srgb, var(--vp-c-brand-1) 25%, transparent);
}

.bv-link-arrow {
  font-size: 0.9rem;
  color: var(--vp-c-text-3);
  transition: transform 0.15s ease, color 0.15s ease;
}

.bv-drawer-nav a:hover .bv-link-arrow,
.bv-drawer-secondary a:hover .bv-link-arrow {
  color: var(--vp-c-brand-1);
  transform: translateX(3px);
}

/* Secondary Section */
.bv-drawer-secondary {
  padding: 1rem 1.4rem;
  border-top: 1px solid var(--vp-c-border);
  margin-top: 0.4rem;
}

.bv-drawer-secondary a {
  font-size: 0.8rem;
  color: var(--vp-c-text-2);
}

/* Footer */
.bv-drawer-footer {
  margin-top: auto;
  padding: 1.2rem 1.4rem;
  border-top: 1px solid var(--vp-c-border);
  background: var(--vp-c-bg-soft);
}

.bv-drawer-copy {
  font-size: 0.72rem;
  color: var(--vp-c-text-3);
  text-align: center;
}
</style>
