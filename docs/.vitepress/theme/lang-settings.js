/**
 * Language Settings State Management
 * 
 * Manages which languages are active (visible in sidebar + cached offline).
 * Persists to localStorage and syncs with Service Worker.
 */

const STORAGE_KEY = 'payer_active_locales'
const ALL_LOCALES = ['de', 'en', 'it', 'bg', 'ru', 'uk', 'hi', 'fr', 'es', 'ta', 'pa', 'la', 'rm', 'ro']
const DEFAULT_LOCALES = ['de', 'en', 'it']

/**
 * Get currently active locales from localStorage (or defaults if not set)
 * @returns {string[]} Array of locale codes (e.g. ['de', 'en', 'it'])
 */
export function getActiveLocales() {
  if (typeof localStorage === 'undefined') return DEFAULT_LOCALES
  
  const stored = localStorage.getItem(STORAGE_KEY)
  if (!stored) return DEFAULT_LOCALES
  
  try {
    const parsed = JSON.parse(stored)
    return Array.isArray(parsed) ? parsed : DEFAULT_LOCALES
  } catch {
    return DEFAULT_LOCALES
  }
}

/**
 * Set active locales, persist to localStorage, and sync with Service Worker
 * @param {string[]} locales - Array of locale codes to activate
 */
export function setActiveLocales(locales) {
  if (typeof localStorage === 'undefined') return
  
  // Validate: at least one locale must be active
  if (!Array.isArray(locales) || locales.length === 0) {
    console.warn('[lang-settings] Invalid locales, ignoring:', locales)
    return
  }
  
  // Persist to localStorage
  localStorage.setItem(STORAGE_KEY, JSON.stringify(locales))
  
  // Sync with Service Worker (if registered)
  if (navigator.serviceWorker?.controller) {
    navigator.serviceWorker.controller.postMessage({
      type: 'SET_ACTIVE_LOCALES',
      locales
    })
  }
  
  // Dispatch custom event for Vue components to listen
  window.dispatchEvent(new CustomEvent('payer:locales-changed', { 
    detail: locales 
  }))
}

/**
 * Check if a locale is currently active
 * @param {string} locale - Locale code to check
 * @returns {boolean}
 */
export function isLocaleActive(locale) {
  const active = getActiveLocales()
  return active.includes(locale)
}

export { ALL_LOCALES, DEFAULT_LOCALES }
