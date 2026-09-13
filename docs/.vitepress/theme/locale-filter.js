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
  
  // If user has never configured settings, keep all available languages visible
  if (typeof localStorage !== 'undefined' && !localStorage.getItem('payer_active_locales')) {
    const existing = document.getElementById('payer-dynamic-locales')
    if (existing) existing.textContent = ''
    return
  }

  const activeLocales = getActiveLocales()
  
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
  
  // Inject or update style tag
  let styleEl = document.getElementById('payer-dynamic-locales')
  if (!styleEl) {
    styleEl = document.createElement('style')
    styleEl.id = 'payer-dynamic-locales'
    document.head.appendChild(styleEl)
  }
  styleEl.textContent = cssRules
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
