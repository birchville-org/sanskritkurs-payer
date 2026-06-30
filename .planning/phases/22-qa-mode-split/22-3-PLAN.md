## Plan 22.3: Add build-script to package.json

Goal: Add `docs:build:author` to the npm scripts for easy author-mode builds.

- [ ] Add `docs:build:author: NODE_OPTIONS=--max-old-space-size=8192 vitepress build docs --config .vitepress/config.author.mjs` to `package.json`.
- [ ] Verify the build process creates a distinct directory or flags for author-only assets.
