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
    // still apply — elements may have been added by navigation
  }
  lastActiveLocales = [...activeLocales]
  
  // Detect current locale from URL
  const pathname = window.location.pathname
  const currentLocaleMatch = pathname.match(/^\/([^/]+)(?:\/|$)/)
  let currentLocale = 'de'
  if (currentLocaleMatch && ALL_LOCALES.includes(currentLocaleMatch[1])) {
      currentLocale = currentLocaleMatch[1]
  }
  
  // --- 1. Filter all <a> links with locale-prefixed hrefs ---
  document.querySelectorAll('a[href]').forEach(a => {
    const href = a.getAttribute('href')
    if (!href) return
    
    // Match: /<locale>/ or /<locale> or /<locale>#...
    // Ignore non-rooted links (mailto:, http://, etc.)
    let locale = null
    
    if (href === '/' || href.startsWith('/#')) {
      locale = 'de'
    } else if (href.startsWith('/')) {
      const m = href.match(/^\/([^/]+)(?=\/|$|#)/)
      if (m && ALL_LOCALES.includes(m[1])) {
          locale = m[1]
      }
    }
    
    if (!locale) {
      // Non-locale link (asset, external, etc.) — leave visible
      a.classList.remove('locale-hidden')
      return
    }
    
    // Always show current locale
    if (locale === currentLocale) {
      a.classList.remove('locale-hidden')
      return
    }
    
    // Hide if not in active locales
    if (!activeLocales.includes(locale)) {
      a.classList.add('locale-hidden')
    } else {
      a.classList.remove('locale-hidden')
    }
  })
  
  // --- 2. Hide locale group containers in sidebar/switcher ---
  // VitePress Language Switcher wraps each locale option in a button/link
  // These typically have data-value attributes — try to detect
  document.querySelectorAll(
    '.VPLocaleLink, ' +              // VitePress locale link
    '[data-locale], ' +              // Generic locale marker
    '.language-selector a, ' +       // Common selector
    '.VPLink[lang]'                   // Lang-attributed link
  ).forEach(el => {
    const elLocale = el.getAttribute('data-locale')
                 || el.getAttribute('lang')
                 || null
    
    if (!elLocale) return
    
    const localeCode = elLocale.split('-')[0]  // 'en-US' → 'en', but wait! 'zh-CN' split by '-' is 'zh'!
    // Actually VitePress uses the exact locale name, e.g. 'zh-CN'. Let's just use the exact match first.
    // We should check ALL_LOCALES
    let exactLocale = ALL_LOCALES.includes(elLocale) ? elLocale : (ALL_LOCALES.includes(localeCode) ? localeCode : null)
    if (!exactLocale) exactLocale = elLocale // fallback to what we had
    
    if (exactLocale === currentLocale) {
      el.classList.remove('locale-hidden')
    } else if (!activeLocales.includes(exactLocale)) {
      el.classList.add('locale-hidden')
    } else {
      el.classList.remove('locale-hidden')
    }
  })
  
  // --- 3. Hide locale <option> elements in any <select> ---
  document.querySelectorAll('select option[value]').forEach(opt => {
    const val = opt.getAttribute('value')
    if (!val || !val.startsWith('/')) return
    
    const m = val.match(/^\/([^/]+)(?:\/|$)/)
    let optLocale = 'de'
    if (m && ALL_LOCALES.includes(m[1])) {
        optLocale = m[1]
    }
    
    if (optLocale === currentLocale || activeLocales.includes(optLocale)) {
      opt.classList.remove('locale-hidden')
    } else {
      opt.classList.add('locale-hidden')
    }
  })
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
