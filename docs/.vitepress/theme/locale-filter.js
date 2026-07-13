/**
 * Hide/show elements that link to locales based on active locale settings.
 * 
 * Applies .locale-hidden class to:
 * - Any link pointing to an inactive locale (e.g. /en/... when EN is not active)
 * - VitePress Language Switcher items for inactive locales
 * 
 * Always keeps visible:
 * - The current locale (user is already browsing it)
 * - DE (root locale, always available)
 * - Any link that doesn't target a specific locale (generic assets)
 */

import { getActiveLocales, ALL_LOCALES } from './lang-settings.js'

let lastActiveLocales = null

/**
 * Apply locale-based visibility filter to all navigation elements
 */
export function filterSidebarByLocales() {
  if (typeof document === 'undefined') return
  
  const activeLocales = getActiveLocales()
  
  // Skip if unchanged (performance optimization)
  if (lastActiveLocales && JSON.stringify(lastActiveLocales) === JSON.stringify(activeLocales)) {
    return
  }
  lastActiveLocales = [...activeLocales]
  
  // Detect current locale from URL
  const pathname = window.location.pathname
  const currentLocaleMatch = pathname.match(/^\/([^/]+)(?:\/|$)/)
  let currentLocale = 'de'
  if (currentLocaleMatch && ALL_LOCALES.includes(currentLocaleMatch[1])) {
      currentLocale = currentLocaleMatch[1]
  }
  
  // Build CSS rules to hide INACTIVE locales
  const inactiveLocales = ALL_LOCALES.filter(loc => loc !== currentLocale && !activeLocales.includes(loc))
  
  let cssRules = inactiveLocales.map(loc => {
      // Hide standard links to this locale, and hide VPMenuLink wrappers (for dropdowns)
      return `
        .VPNav a[href^="/${loc}/"], .VPNav a[href="/${loc}/"],
        .VPSidebar a[href^="/${loc}/"], .VPSidebar a[href="/${loc}/"],
        .VPMenuLink:has(a[href^="/${loc}/"]), .VPMenuLink:has(a[href="/${loc}/"]),
        .VPLink[href^="/${loc}/"], .VPLink[href="/${loc}/"] {
            display: none !important;
        }
      `
  }).join('\n')
  
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
  
  // Re-filter when locales are changed
  window.addEventListener('payer:locales-changed', () => {
    // Allow current UI render cycle to complete
    requestAnimationFrame(() => filterSidebarByLocales())
  })
}
