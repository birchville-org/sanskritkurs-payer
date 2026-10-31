<script setup>
import { ref, onMounted, onUnmounted } from 'vue'

const dialogRef = ref(null)
const contentRef = ref(null)
const currentUrl = ref('')
const displayUrl = ref('')
const headword = ref('')
const loading = ref(false)
const errorMsg = ref('')

const ALLOWED_TAGS = new Set([
  'DIV', 'H1', 'H2', 'H3', 'P', 'TABLE', 'TBODY', 'THEAD', 'TR', 'TD', 'TH',
  'SPAN', 'I', 'B', 'STRONG', 'EM', 'BR', 'A', 'SUP', 'SUB', 'UL', 'OL', 'LI'
])

function sanitizeAndBuildDom(sourceNode, targetDoc) {
  if (sourceNode.nodeType === Node.TEXT_NODE) {
    return targetDoc.createTextNode(sourceNode.textContent)
  }
  if (sourceNode.nodeType !== Node.ELEMENT_NODE) {
    return null
  }

  const tag = sourceNode.tagName.toUpperCase()
  // Skip empty/custom metadata tags like <listinfo>
  if (tag === 'LISTINFO' || tag === 'SCRIPT' || tag === 'STYLE') {
    return null
  }

  const el = ALLOWED_TAGS.has(tag)
    ? targetDoc.createElement(tag.toLowerCase())
    : targetDoc.createElement('span')

  if (sourceNode.className) {
    el.className = sourceNode.className
  }

  const titleAttr = sourceNode.getAttribute('title')
  if (titleAttr) {
    el.setAttribute('title', titleAttr)
    el.classList.add('mw-abbr-tooltip')
  }

  const styleAttr = (sourceNode.getAttribute('style') || '').toLowerCase()
  if (styleAttr.includes('#8080ff')) {
    el.classList.add('mw-lit-ref')
  } else if (styleAttr.includes('brown')) {
    el.classList.add('mw-botanical')
  } else if (styleAttr.includes('rgb(160,160,160)')) {
    el.classList.add('mw-muted')
  } else if (styleAttr.includes('font-weight:bold') || styleAttr.includes('font-weight: bold')) {
    el.classList.add('mw-bold')
  }

  if (tag === 'A') {
    let href = sourceNode.getAttribute('href') || ''
    if (href.startsWith('//')) {
      href = 'https:' + href
    } else if (href.startsWith('/')) {
      href = 'https://www.sanskrit-lexicon.uni-koeln.de' + href
    }
    if (href.startsWith('https://') || href.startsWith('http://')) {
      el.setAttribute('href', href)
      el.setAttribute('target', '_blank')
      el.setAttribute('rel', 'noopener noreferrer')
    }
  }

  for (const child of sourceNode.childNodes) {
    const safeChild = sanitizeAndBuildDom(child, targetDoc)
    if (safeChild) {
      el.appendChild(safeChild)
    }
  }

  return el
}

async function openMwPopup(href, rawHref, wordText) {
  currentUrl.value = href
  try {
    displayUrl.value = decodeURIComponent(rawHref || href)
  } catch {
    displayUrl.value = rawHref || href
  }

  let extractedKey = wordText
  try {
    const u = new URL(href)
    const k = u.searchParams.get('key')
    if (k) extractedKey = k
  } catch {}
  headword.value = extractedKey || wordText || 'Monier-Williams'

  loading.value = true
  errorMsg.value = ''
  if (contentRef.value) {
    contentRef.value.replaceChildren()
  }

  const dialog = dialogRef.value
  if (dialog && !dialog.open) {
    dialog.showModal()
  }

  try {
    const resp = await fetch(href)
    if (!resp.ok) {
      throw new Error(`HTTP ${resp.status}`)
    }
    const htmlText = await resp.text()
    const parser = new DOMParser()
    const doc = parser.parseFromString(htmlText, 'text/html')
    const root = doc.getElementById('CologneBasic') || doc.body

    // Remove the redundant top <h1> inside #CologneBasic since we show the headword in the dialog header
    const firstH1 = root.querySelector('h1')
    if (firstH1) {
      firstH1.remove()
    }

    const fragment = document.createDocumentFragment()
    for (const child of root.childNodes) {
      const safeNode = sanitizeAndBuildDom(child, document)
      if (safeNode) {
        fragment.appendChild(safeNode)
      }
    }

    if (contentRef.value) {
      contentRef.value.replaceChildren(fragment)
    }
  } catch (err) {
    errorMsg.value = `Eintrag konnte nicht direkt geladen werden (${err.message}). Bitte nutzen Sie den untenstehenden Direktlink.`
  } finally {
    loading.value = false
  }
}

function handleDocumentClick(e) {
  if (!e.isTrusted) return
  if (e.metaKey || e.ctrlKey || e.shiftKey || e.altKey || e.button !== 0) return

  const link = e.target.closest('a[href*="sanskrit-lexicon.uni-koeln.de"]')
  if (!link) return
  if (link.closest('.payer-mw-dialog')) return

  e.preventDefault()
  e.stopPropagation()

  openMwPopup(
    link.href,
    link.getAttribute('href') || link.href,
    link.textContent ? link.textContent.trim() : ''
  )
}

onMounted(() => {
  window.addEventListener('click', handleDocumentClick, true)

  const dialog = dialogRef.value
  // Fallback for browsers without native <dialog closedby="any"> support (e.g. Safari)
  if (dialog && !('closedBy' in HTMLDialogElement.prototype)) {
    dialog.addEventListener('click', (event) => {
      if (event.target !== dialog) return
      const rect = dialog.getBoundingClientRect()
      const isDialogContent = (
        rect.top <= event.clientY &&
        event.clientY <= rect.top + rect.height &&
        rect.left <= event.clientX &&
        event.clientX <= rect.left + rect.width
      )
      if (isDialogContent) return
      dialog.close()
    })
  }
})

onUnmounted(() => {
  window.removeEventListener('click', handleDocumentClick, true)
})
</script>

<template>
  <dialog
    ref="dialogRef"
    class="payer-mw-dialog"
    closedby="any"
    aria-labelledby="payer-mw-dialog-title"
  >
    <div class="payer-mw-frame-header">
      <div class="payer-mw-title-row">
        <div class="payer-mw-title-group">
          <span class="payer-mw-badge">MW 1899</span>
          <h2 id="payer-mw-dialog-title" class="payer-mw-title">
            {{ headword }}
          </h2>
          <span class="payer-mw-subtitle">Monier-Williams Sanskrit-English Dictionary</span>
        </div>
        <form method="dialog" class="payer-mw-close-form">
          <button
            type="submit"
            class="payer-mw-close-btn"
            aria-label="Popup schließen"
            title="Schließen (Esc)"
            autofocus
          >
            ✕
          </button>
        </form>
      </div>

      <div class="payer-mw-url-bar">
        <span class="payer-mw-url-label">Link:</span>
        <a
          :href="currentUrl"
          target="_blank"
          rel="noopener noreferrer"
          class="payer-mw-url-link"
          title="Monier-Williams in neuem Tab öffnen"
        >
          {{ displayUrl }}
        </a>
        <a
          :href="currentUrl"
          target="_blank"
          rel="noopener noreferrer"
          class="payer-mw-external-btn"
          title="In neuem Tab öffnen"
          aria-label="In neuem Tab öffnen"
        >
          ↗
        </a>
      </div>
    </div>

    <div class="payer-mw-body">
      <div v-if="loading" class="payer-mw-status">
        Lade Wörterbucheintrag von sanskrit-lexicon.uni-koeln.de …
      </div>
      <div v-else-if="errorMsg" class="payer-mw-error">
        {{ errorMsg }}
      </div>
      <div ref="contentRef" class="payer-mw-content"></div>
    </div>
  </dialog>
</template>

<style>
dialog.payer-mw-dialog {
  width: fit-content;
  min-width: min(560px, 94vw);
  max-width: min(920px, 94vw);
  height: fit-content;
  max-height: 85vh;
  margin: auto;
  padding: 0;
  border: 1px solid var(--vp-c-divider, #d8d2c6);
  border-radius: 10px;
  background-color: var(--vp-c-bg, #fcf9f2);
  color: var(--vp-c-text-1, #03192e);
  box-shadow: 0 22px 54px rgba(3, 25, 46, 0.38);
  font-family: var(--vp-font-family-base, 'Newsreader', Georgia, serif);
}

dialog.payer-mw-dialog[open] {
  display: flex;
  flex-direction: column;
}

dialog.payer-mw-dialog:modal {
  overscroll-behavior: contain;
}

dialog.payer-mw-dialog::backdrop {
  overflow: hidden;
  overscroll-behavior: contain;
  background-color: rgba(3, 25, 46, 0.52);
  backdrop-filter: blur(3px);
}

.payer-mw-frame-header {
  display: flex;
  flex-direction: column;
  gap: 0.45rem;
  padding: 0.75rem 1rem;
  background-color: var(--vp-c-bg-soft, #f1eee7);
  border-bottom: 1px solid var(--vp-c-divider, #d8d2c6);
  border-radius: 10px 10px 0 0;
  flex-shrink: 0;
}

.payer-mw-title-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
}

.payer-mw-title-group {
  display: flex;
  align-items: baseline;
  flex-wrap: wrap;
  gap: 0.55rem;
}

.payer-mw-badge {
  font-family: var(--vp-font-family-mono, monospace);
  font-size: 0.7rem;
  font-weight: 700;
  letter-spacing: 0.04em;
  text-transform: uppercase;
  padding: 0.12rem 0.45rem;
  border-radius: 4px;
  background-color: var(--vp-c-brand-soft, rgba(180, 83, 9, 0.14));
  color: var(--vp-c-brand-1, #b45309);
  align-self: center;
}

.payer-mw-title {
  margin: 0;
  font-size: 1.25rem;
  font-weight: 700;
  line-height: 1.25;
  color: var(--vp-c-text-1, #03192e);
}

.payer-mw-subtitle {
  font-size: 0.8rem;
  color: var(--vp-c-text-2, #6b6257);
  font-family: -apple-system, BlinkMacSystemFont, 'Inter', sans-serif;
}

.payer-mw-close-form {
  margin: 0;
}

.payer-mw-close-btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 1.85rem;
  height: 1.85rem;
  border: 1px solid var(--vp-c-divider, #d8d2c6);
  border-radius: 6px;
  background-color: var(--vp-c-bg, #fcf9f2);
  color: var(--vp-c-text-2, #1e2d37);
  font-size: 0.95rem;
  line-height: 1;
  cursor: pointer;
  transition: background-color 0.15s, color 0.15s, border-color 0.15s;
}

.payer-mw-close-btn:hover {
  background-color: var(--vp-c-brand-1, #b45309);
  border-color: var(--vp-c-brand-1, #b45309);
  color: #ffffff;
}

.payer-mw-url-bar {
  display: flex;
  align-items: center;
  gap: 0.45rem;
  padding: 0.3rem 0.55rem;
  background-color: var(--vp-c-bg, #fcf9f2);
  border: 1px solid var(--vp-c-divider, #d8d2c6);
  border-radius: 6px;
  font-family: var(--vp-font-family-mono, ui-monospace, SFMono-Regular, Menlo, monospace);
  font-size: 0.74rem;
  line-height: 1.35;
  overflow-x: auto;
}

.payer-mw-url-label {
  font-weight: 600;
  color: var(--vp-c-text-2, #6b6257);
  user-select: none;
  flex-shrink: 0;
}

.payer-mw-url-link {
  color: var(--vp-c-brand-1, #b45309);
  text-decoration: none;
  word-break: break-all;
  flex: 1;
}

.payer-mw-url-link:hover {
  text-decoration: underline;
}

.payer-mw-external-btn {
  flex-shrink: 0;
  padding: 0.05rem 0.35rem;
  border-radius: 4px;
  color: var(--vp-c-text-2, #6b6257);
  text-decoration: none;
  font-weight: 700;
}

.payer-mw-external-btn:hover {
  color: var(--vp-c-brand-1, #b45309);
}

.payer-mw-body {
  padding: 1rem 1.25rem 1.15rem;
  overflow-y: auto;
  max-height: calc(85vh - 5.5rem);
  font-size: 1rem;
  line-height: 1.65;
}

.payer-mw-status {
  padding: 1.25rem 0;
  color: var(--vp-c-text-2, #6b6257);
  font-style: italic;
}

.payer-mw-error {
  padding: 0.75rem 1rem;
  border-radius: 6px;
  background-color: rgba(244, 63, 94, 0.1);
  color: #e11d48;
}

.payer-mw-content table.display {
  width: 100%;
  border-collapse: collapse;
  margin: 0;
}

.payer-mw-content td.display {
  padding: 0.55rem 0.65rem;
  border-bottom: 1px solid var(--vp-c-divider, #d8d2c6);
  vertical-align: top;
}

.payer-mw-content tr:last-child td.display {
  border-bottom: none;
}

.payer-mw-content td.cssshade {
  background-color: var(--vp-c-bg-soft, rgba(241, 238, 231, 0.55));
}

.payer-mw-content .sdata,
.payer-mw-content .sdata_italic_iast {
  font-weight: 600;
  color: var(--vp-c-brand-1, #b45309);
}

.payer-mw-content .mw-abbr-tooltip {
  border-bottom: 1px dotted var(--vp-c-text-2, #6b6257);
  cursor: help;
}

.payer-mw-content .mw-lit-ref {
  color: var(--vp-c-brand-1, #b45309);
}

.payer-mw-content .mw-botanical {
  font-style: italic;
}

.payer-mw-content .mw-muted,
.payer-mw-content .lnum,
.payer-mw-content .hrefdata {
  font-size: 0.82rem;
  color: var(--vp-c-text-3, #6b6257);
}

.payer-mw-content .mw-bold {
  font-weight: 600;
}

.payer-mw-content a {
  color: var(--vp-c-brand-1, #b45309);
  text-decoration: underline;
}
</style>
