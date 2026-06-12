/**
 * Shared PWA install state.
 *
 * The browser's `beforeinstallprompt` event is captured globally in index.mjs so
 * it doesn't go to waste. Any component (currently: PayerLanguageSettings) can
 * retrieve the deferred prompt and invoke it to show the native install dialog.
 *
 * Flow:
 *   1. index.mjs calls `setupInstallCapture()` once on mount.
 *   2. Browser fires `beforeinstallprompt` → we store it in module state.
 *   3. Settings component calls `getDeferredPrompt()` when user clicks Install.
 *   4. Settings component calls `clearDeferredPrompt()` after `userChoice`.
 *   5. Browser fires `appinstalled` → we clear state automatically.
 */

// Reactive-like state (module-private, exposed via getters)
let deferredPrompt = null
let installed = false
const listeners = new Set()

function notify() {
  for (const fn of listeners) {
    try { fn({ available: isPromptAvailable(), installed }) } catch (err) {
      console.warn('[install-state] listener error:', err)
    }
  }
}

/**
 * Returns true if the native install prompt is currently available.
 * (Not installed, and browser has fired beforeinstallprompt.)
 */
export function isPromptAvailable() {
  return !!deferredPrompt && !installed
}

/**
 * Returns the captured BeforeInstallPromptEvent (or null if none).
 */
export function getDeferredPrompt() {
  return deferredPrompt
}

/**
 * Clear the deferred prompt (after userChoice or appinstalled).
 */
export function clearDeferredPrompt() {
  deferredPrompt = null
  notify()
}

/**
 * Subscribe to availability changes (returns unsubscribe function).
 * Listener receives { available: boolean, installed: boolean }.
 */
export function subscribe(listener) {
  listeners.add(listener)
  // Initial ping so component can sync on mount
  try { listener({ available: isPromptAvailable(), installed }) } catch (err) {
    console.warn('[install-state] initial listener error:', err)
  }
  return () => listeners.delete(listener)
}

/**
 * Attach global listeners. Call exactly once (typically in theme index.mjs setup()).
 */
export function setupInstallCapture() {
  if (typeof window === 'undefined') return

  // Already installed (e.g. user opened the app from home screen / desktop)
  if (window.matchMedia?.('(display-mode: standalone)').matches) {
    installed = true
  }

  window.addEventListener('beforeinstallprompt', (e) => {
    e.preventDefault()
    deferredPrompt = e
    notify()
  })

  window.addEventListener('appinstalled', () => {
    deferredPrompt = null
    installed = true
    notify()
  })
}
