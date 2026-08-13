# Sanskritkurs Payer (VitePress Migration)

This repository contains the migrated and modernized version of the original Sanskrit course by Alois Payer. The content has been algorithmically parsed, cleaned of legacy HTML clutter, and reconstructed into a modern, lightning-fast static documentation site using [VitePress](https://vitepress.dev/).

## 🚀 Setup & Development

When cloning this repository to a new machine, you will notice that dependency folders (like `node_modules`) are missing. This is intentional to ensure cross-platform compatibility and keep the repository clean.

To initialize the project and start working locally, follow these steps:

1. **Clone the repository:**
   ```bash
   git clone https://github.com/birchville-org/sanskritkurs-payer.git
   cd sanskritkurs-payer
   ```

2. **Install Node dependencies:**
   This will download all required VitePress build files matching your current operating system.
   ```bash
   npm install
   ```

3. **Start the local development server:**
   ```bash
   npm run docs:dev
   ```
   *The interactive course will now be hosted locally, usually at `http://localhost:5173`. Any changes made to the Markdown files will be instantly updated in your browser.*

## 📦 Deployment (Hosting on a Web Server)

To deploy the course to a live web server (such as Apache, Nginx, or any static hosting provider), you do not need to run Node.js on your server. VitePress pre-renders all content into flat, static files.

1. **Build the production files:**
   ```bash
   npm run docs:build
   ```

2. **Locate the output directory:**
   Once the build completes, VitePress generates a distribution folder located at `docs/.vitepress/dist`.

3. **Deploy to production:**
   Simply copy the **contents** of the `docs/.vitepress/dist` folder to the public root directory (e.g., `htdocs` or `public_html`) of your web server. The site is completely static, extremely secure, and requires no database.

## 📱 Progressive Web App (PWA)

The course is fully installable as a Progressive Web App on desktop and mobile devices. Once installed, the selected languages are available **offline** without any network connection.

### Installation

1. Open the course in a supported browser (Chrome, Edge, Safari 16.4+, Firefox).
2. Click the **"App installieren"** button that appears in the bottom-right corner (desktop) or use the browser's native install prompt (mobile: "Add to Home Screen").
3. Choose your preferred languages in the Settings page (accessible via the sidebar).
4. Confirm installation. The app will cache all selected languages (~23 MB per language).

### Offline Usage

- After the first online visit, all visited content is cached locally.
- Unvisited pages show a bilingual offline fallback page and auto-reload when the connection is restored.
- You can add languages later via the Settings page — new content is fetched online and added to the cache.

### Browser Compatibility

| Browser | Minimum Version | Notes |
|---------|----------------|-------|
| Chrome / Edge | 90+ | Full PWA support |
| Safari (iOS/macOS) | 16.4+ | Push notifications require 16.4+ |
| Firefox | 90+ | Full offline support, install prompt varies |

### Cache Management

Open the Settings page to:
- See current cache size (`navigator.storage.estimate()`)
- Clear the cache to re-download selected languages
- Add or remove active languages

## 🐳 Docker

Pre-built Docker images are published to GitHub Container Registry (GHCR) on every push to `main`.

### Pull the Image

```bash
docker pull ghcr.io/birchville-org/sanskritkurs-payer:latest
```

Available tags:
- `latest` — most recent commit on `main`
- `v*.*.*` — semantic version releases
- `sha-<commit>` — pinned to a specific commit

### Run Locally

```bash
docker run -d -p 8080:80 ghcr.io/birchville-org/sanskritkurs-payer:latest
# Visit http://localhost:8080
```

### Deploy Behind a Reverse Proxy

Example `docker-compose.yml` for deployment with a reverse proxy (e.g., Caddy, Traefik, nginx):

```yaml
services:
  payer:
    image: ghcr.io/birchville-org/sanskritkurs-payer:latest
    restart: unless-stopped
    ports:
      - "8080:80"
    # Optionally restrict visibility with Authelia, Cloudflare Access, etc.
```

For HTTPS termination and routing, use your preferred reverse proxy. The container itself only exposes port 80 (HTTP).

### Image Internals

- Base image: `nginx:alpine` (minimal footprint, ~50 MB)
- Static build is performed in GitHub Actions (native AMD64, fast)
- Only `docs/.vitepress/dist` is copied into the image — no Node.js in the runtime image
- Custom `nginx.conf` is shipped for clean URL rewriting

### Build Locally (Optional)

To build the Docker image yourself:

```bash
npm ci
npm run docs:build
docker build -t sanskritkurs-payer:local .
docker run -d -p 8080:80 sanskritkurs-payer:local
```
