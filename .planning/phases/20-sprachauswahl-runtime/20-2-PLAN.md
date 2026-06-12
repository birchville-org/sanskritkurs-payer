# Plan 20-2: Sidebar-Filter

**Phase**: 20 Sprachauswahl (Runtime-Filter)  
**Status**: Pending  
**Dependencies**: 20-1 ✅

## Ziel

Sidebar zeigt nur Sprachen die in Settings aktiviert sind. Nicht-aktive Sprachen werden ausgeblendet (nicht entfernt — sie sind im HTML, aber `display: none`).

## Deliverables

Modifikation: `docs/.vitepress/theme/index.mjs`

## Implementation

Die Language-Switcher-Group in der Sidebar (VitePress generiert sie als `.VPSidebarItem.level-0` Einträge mit Sprachcodes) wird via CSS/JS gefiltert:

### Filter-Logik in `setup()` hinzufügen

```javascript
// In setup() — nach route watcher
function filterSidebarByLocales() {
  if (typeof document === 'undefined') return
  const active = getActiveLocales()  // from lang-settings.js
  
  // VitePress Locale-Links haben Pattern: /<locale>/
  const sidebar = document.querySelector('.VPSidebar')
  if (!sidebar) return
  
  // Alle Top-Level Language-Items (nicht die Lektionen/Schriften innerhalb)
  // VitePress strukturiert Locales nicht als Sidebar-Items, sie sind in der Language-Switcher
  // → Wir verstecken Links im gesamten App-DOM die auf nicht-aktive Sprachen zeigen
  
  document.querySelectorAll('a[href^="/"]').forEach(link => {
    const href = link.getAttribute('href') || ''
    const match = href.match(/^\/([a-z]{2})(\/|$)/)
    if (!match) return
    
    const locale = match[1] === '' ? 'de' : match[1]
    const rootLocale = locale === 'de' ? true : active.includes(locale)
    
    if (locale === 'de' || active.includes(locale)) {
      link.classList.remove('locale-hidden')
    } else {
      link.classList.add('locale-hidden')
    }
  })
}
```

### CSS hinzufügen in `custom.css`

```css
.locale-hidden {
  display: none !important;
}
```

### Re-Filter bei Navigation

Im bestehenden `watch(() => route.path, ...)`:
```javascript
watch(() => route.path, (path) => {
  setTimeout(() => {
    closeInactiveGroups()
    mergeTableCells()
    filterSidebarByLocales()  // NEU
  }, 250)
}, { immediate: true })
```

### Re-Filter bei Locale-Change Event

```javascript
window.addEventListener('payer:locales-changed', () => {
  filterSidebarByLocales()
})
```

## Scope-Überlegungen

**Was wird gefiltert**:
- Links in der Sidebar (`/en/lektion/01/` etc.)
- Links in Language-Switcher Dropdown
- Navigation zu anderen Locales

**Was bleibt sichtbar**:
- Aktuelle Sprache (immer sichtbar — User ist ja schon da)
- Alle Lektionen/Schriften/Übungen INNERHALB der aktiven Sprache
- DE/Root wird nie versteckt

**Edge Case**: User deaktiviert Sprache, in der er gerade ist
- Settings-Prompt warnt davor (disabled Checkbox für current locale)
- Plan 20-1 hat das schon geblockt

## Verification

```bash
npm run docs:dev
# 1. Default: Sidebar zeigt alle 14 Sprachen
# 2. Settings: Deaktiviere "English" → save
# 3. Sidebar: /en/ Links sind verschwunden
# 4. Direkte Navigation zu /en/lektion/01/ funktioniert noch (URL ist erreichbar)
# 5. Settings → Re-aktiviere En → Links kommen zurück
```

## Success Criteria

- ✅ Filter wendet sich sofort nach Save an
- ✅ Re-Filter bei jeder Routenänderung
- ✅ DE (root) bleibt immer sichtbar
- ✅ Current Locale bleibt immer sichtbar
- ✅ Direkte URL-Navigation funktioniert trotzdem (Link-Hiding ≠ Route-Blocking)
- ✅ Build erfolgreich

## Notes

- Wir verstecken Links, nicht Routen — URL `/en/...` bleibt erreichbar
- Das ist bewusst: User könnte Link direkt öffnen wollen
- Wenn User versucht, eine nicht-aktive Sprache offline zu öffnen → offline.html (Plan 19-4)
