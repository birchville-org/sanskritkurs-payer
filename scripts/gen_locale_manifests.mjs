#!/usr/bin/env node
// ============================================================
// gen_locale_manifests.mjs
// Generates manifest-{locale}.json files for each locale
// so the service worker can pre-fetch URLs for a given language.
//
// Run after `vitepress build`: node scripts/gen_locale_manifests.mjs
// Or as part of docs:build via npm post-hook.
// ============================================================

import { readdir, writeFile, stat, rm } from 'node:fs/promises'
import { join, relative } from 'node:path'

const DIST_DIR = new URL('../docs/.vitepress/dist/', import.meta.url).pathname

import { ACTIVE_LOCALES as LOCALES } from '../docs/.vitepress/languages.mjs'

/**
 * Recursively collect all .html files under dirPath.
 * Returns array of paths relative to DIST_DIR (e.g. 'lektion/01/index.html').
 */
async function collectHtmlFiles(dirPath, rootPath = dirPath) {
  const entries = await readdir(dirPath, { withFileTypes: true })
  const results = []

  for (const entry of entries) {
    const fullPath = join(dirPath, entry.name)
    if (entry.isDirectory()) {
      const nested = await collectHtmlFiles(fullPath, rootPath)
      results.push(...nested)
    } else if (entry.isFile() && entry.name.endsWith('.html')) {
      results.push(relative(rootPath, fullPath))
    }
  }

  return results
}

/**
 * Convert 'path/to/page/index.html' → '/path/to/page'
 * and 'path/to/page.html' → '/path/to/page'
 * (VitePress cleanUrls mode)
 */
function toCleanUrl(relativePath) {
  // Remove .html extension
  let path = relativePath.replace(/\.html$/, '')
  // Remove trailing '/index'
  path = path.replace(/\/index$/, '')
  // Normalize: empty → '/'
  if (path === '') path = '/'
  // Ensure leading slash
  if (!path.startsWith('/')) path = '/' + path
  return path
}

/**
 * Determine locale of a file based on first path segment.
 * Files in /en/* → 'en', /it/* → 'it', root files → 'de'
 */
function detectLocale(relativePath) {
  const firstSegment = relativePath.split('/')[0]
  if (LOCALES.includes(firstSegment)) {
    return firstSegment
  }
  return 'de' // root = DE
}

async function main() {
  console.log(`[manifests] Scanning ${DIST_DIR}...`)

  try {
    await stat(DIST_DIR)
  } catch {
    console.error(`[manifests] ERROR: dist dir not found: ${DIST_DIR}`)
    console.error(`[manifests] Run "npm run docs:build" first.`)
    process.exit(1)
  }

  // Clean up any uncompiled markdown copies of excluded locales in dist
  const distEntries = await readdir(DIST_DIR, { withFileTypes: true })
  const coreDirs = new Set(['assets', 'images', 'lektionen', 'qa', 'pwa-icons'])
  for (const entry of distEntries) {
    if (entry.isDirectory()) {
      const name = entry.name
      if (!coreDirs.has(name) && !LOCALES.includes(name) && name !== 'de') {
        const full = join(DIST_DIR, name)
        await rm(full, { recursive: true, force: true })
      }
    }
  }

  const htmlFiles = await collectHtmlFiles(DIST_DIR)
  console.log(`[manifests] Found ${htmlFiles.length} HTML files total`)

  // Group by locale
  const byLocale = {}
  for (const locale of LOCALES) byLocale[locale] = []

  for (const file of htmlFiles) {
    const locale = detectLocale(file)
    byLocale[locale].push(toCleanUrl(file))
  }

  // Sort URLs within each locale for cache determinism
  for (const locale of LOCALES) {
    byLocale[locale].sort()
  }

  // Write manifest files
  let totalCount = 0
  for (const locale of LOCALES) {
    const urls = byLocale[locale]
    if (urls.length === 0) {
      console.log(`[manifests] SKIP ${locale} (0 URLs)`)
      continue
    }
    
    const manifest = {
      locale,
      count: urls.length,
      generated: new Date().toISOString(),
      urls
    }
    const outFile = join(DIST_DIR, `manifest-${locale}.json`)
    await writeFile(outFile, JSON.stringify(manifest, null, 2))
    totalCount += urls.length
    console.log(`[manifests] ✓ ${locale}: ${urls.length} URLs → manifest-${locale}.json`)
  }

  console.log(`[manifests] Done. ${totalCount} total URLs across ${LOCALES.length} locales.`)
}

main().catch((err) => {
  console.error('[manifests] FATAL:', err)
  process.exit(1)
})
