# 📱 PWA & Infrastructure

## 1. Progressive Web App (PWA) Architecture

The Sanskrit course is engineered as a fully functional Progressive Web App. Students can install the complete curriculum across desktop and mobile devices (iOS, Android, Windows, macOS, Linux) and study without an active internet connection.

### 1.1. Caching Strategy & Storage Management
- **Language-Partitioned Storage:** The service worker downloads and caches assets on a per-language basis. Each locale bundle consumes approximately 23 MB of pre-rendered HTML, CSS, JavaScript, and SVG vector glyphs.
- **Cache Inspection:** The settings page (`settings.md`) exposes `navigator.storage.estimate()` metrics, allowing users to inspect storage consumption and purge caches on demand.
- **Bilingual Offline Fallback:** Uncached pages render a responsive offline notice that automatically reloads when internet connectivity is re-established.

---

## 2. VitePress SSG Configuration

The project utilizes **VitePress 1.6** as its core static site generator.

### 2.1. Algorithmic Sidebar Population
Each locale's sidebar is constructed dynamically via `populateSidebar()` (`docs/.vitepress/utils.mjs`):
- Automatic grouping into 10-lesson clusters (*Lesson 01–10*, *11–20* through *51–61*).
- Localized labels for *Lesson*, *Script*, and *Exercise*.

### 2.2. Local Full-Text Search & Diacritic Normalization
Integrated MiniSearch indexing with IAST diacritical stripping (`docs/.vitepress/config.mjs`):
- Queries with or without vowel marks (`ā` vs. `a`, `ś` vs. `s`, `ṛ` vs. `r`) match the same underlying grammatical rules.
- URL-prefix filtering isolates search results to the student's active language.

---

## 3. Docker Containers & GHCR Deployment

For web server hosting, an ultra-lightweight production Docker container is published automatically:

- **Base Image:** `nginx:alpine` (compressed image footprint: ~50 MB).
- **Multi-Architecture Builds:** Built natively for `linux/amd64` and `linux/arm64` via GitHub Actions (`.github/workflows/deploy.yml`).
- **Clean URLs:** Optimized `nginx.conf` ensures modern URL rewriting without `.html` extensions.

```bash
# Pull production image
docker pull ghcr.io/birchville-org/sanskritkurs-payer:latest

# Run locally
docker run -d -p 8080:80 ghcr.io/birchville-org/sanskritkurs-payer:latest
```

---

## 4. Native Desktop Bundles (Tauri)

The course is also packaged as a native desktop application using [Tauri](https://tauri.app/):
- **Preparation:** `python3 scripts/prepare_desktop_dist.py` (filters core locales for minimal bundle size).
- **Build Execution:** `npx tauri build --bundles dmg`.
