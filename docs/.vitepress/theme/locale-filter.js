/**
 * Hide/show elements that link to locales based on active locale settings.
 * 
 * Filters the VitePress Language Switcher dropdown items based on the user's
 * active language selection in Settings.
 * 
 * Always keeps visible:
 * - The current locale (user is currently browsing it)
 * - DE (root locale, always available)
 */

import { getActiveLocales, ALL_LOCALES } from './lang-settings.js'

let lastActiveLocales = null

/**
 * Apply locale-based visibility filter to language switcher dropdowns
 */
export function filterSidebarByLocales() {
  if (typeof document === 'undefined') return
  
  const isDesktop = typeof window !== 'undefined' && (
    Boolean(window.IS_DESKTOP_APP) ||
    Boolean(window.__TAURI__) ||
    Boolean(window.__TAURI_INTERNALS__) ||
    window.location.protocol === 'tauri:'
  )

  // If user has never configured settings, keep all available languages visible (unless on Desktop)
  if (!isDesktop && typeof localStorage !== 'undefined' && !localStorage.getItem('payer_active_locales')) {
    const existing = document.getElementById('payer-dynamic-locales')
    if (existing) existing.textContent = ''
    return
  }

  const activeLocales = isDesktop ? ['en'] : getActiveLocales()
  
  // Detect current locale from URL
  const pathname = window.location.pathname
  const currentLocaleMatch = pathname.match(/^\/([^/]+)(?:\/|$)/)
  let currentLocale = 'de'
  if (currentLocaleMatch && ALL_LOCALES.includes(currentLocaleMatch[1])) {
    currentLocale = currentLocaleMatch[1]
  }
  
  // Build CSS rules to hide INACTIVE locales in language switcher menus
  const inactiveLocales = ALL_LOCALES.filter(
    loc => loc !== currentLocale && loc !== 'de' && !activeLocales.includes(loc)
  )
  
  const cssRules = inactiveLocales.map(loc => `
    .VPNavBarTranslations .VPMenuLink:has(a[href^="/${loc}/"]),
    .VPNavBarTranslations .VPMenuLink:has(a[href="/${loc}/"]),
    .VPNavScreenTranslations li:has(a[href^="/${loc}/"]),
    .VPNavScreenTranslations li:has(a[href="/${loc}/"]),
    .VPNavBarTranslations a[href^="/${loc}/"],
    .VPNavBarTranslations a[href="/${loc}/"],
    .VPNavScreenTranslations a[href^="/${loc}/"],
    .VPNavScreenTranslations a[href="/${loc}/"] {
      display: none !important;
    }
  `).join('\n')
  
  const settingsRule = isDesktop ? `
    .VPNavBar a:has(.nav-gear-icon),
    .VPNavScreen a:has(.nav-gear-icon),
    .VPNavBar a[href*="settings"],
    .VPNavScreen a[href*="settings"],
    .VPNavBar a[href*="qa_viewer"],
    .VPNavScreen a[href*="qa_viewer"],
    a[href*="qa_viewer"],
    .nav-gear-icon {
      display: none !important;
    }
  ` : ''
  
  // Inject or update style tag
  let styleEl = document.getElementById('payer-dynamic-locales')
  if (!styleEl) {
    styleEl = document.createElement('style')
    styleEl.id = 'payer-dynamic-locales'
    document.head.appendChild(styleEl)
  }
  styleEl.textContent = cssRules + '\n' + settingsRule
}

/**
 * Initialize auto-re-filter on locale-change events
 */
export function setupLocaleFilter() {
  if (typeof window === 'undefined') return
  
  // Initial run
  filterSidebarByLocales()
  
  // Re-filter when locales are changed in settings
  window.addEventListener('payer:locales-changed', () => {
    requestAnimationFrame(() => filterSidebarByLocales())
  })
}
