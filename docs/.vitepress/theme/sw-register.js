// Service Worker Registration
// Register in production + localhost:4173 (npm run docs:preview)
// Skip only in Vite dev mode (npm run docs:dev on :5173) which uses HMR
// and conflicts with service workers.

export function registerServiceWorker() {
  if (typeof window === 'undefined') return
  if (!('serviceWorker' in navigator)) {
    console.log('[SW] Service Worker not supported')
    return
  }
  
  const hostname = window.location.hostname
  const port = window.location.port
  
  // Skip only on Vite dev server (HMR active).
  // Vite's default dev port is 5173; accept any other port (incl. 4173 for preview).
  const isDevServer = (hostname === 'localhost' || hostname === '127.0.0.1') && port === '5173'
  if (isDevServer) {
    console.log('[SW] Skipping registration in Vite dev mode (port 5173, HMR active)')
    return
  }
  
  window.addEventListener('load', async () => {
    try {
      const swUrl = port ? '/sw.js' : '/sw.js'
      const registration = await navigator.serviceWorker.register(swUrl, {
        scope: '/'
      })
      
      console.log('[SW] Registered:', registration.scope, '(port:', port || 'default', ')')
      
      registration.addEventListener('updatefound', () => {
        const newWorker = registration.installing
        console.log('[SW] New worker found, installing...')
        
        newWorker.addEventListener('statechange', () => {
          if (newWorker.state === 'installed' && navigator.serviceWorker.controller) {
            console.log('[SW] New content available, refresh to update')
          }
        })
      })
    } catch (error) {
      console.error('[SW] Registration failed:', error)
    }
  })
}
