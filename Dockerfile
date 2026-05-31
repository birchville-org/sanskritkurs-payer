# VitePress wird nativ im GitHub Actions Workflow gebaut (AMD64, schnell).
# Dieses Dockerfile kopiert nur das fertige dist/ — kein Node.js via QEMU.
FROM nginx:alpine
COPY docs/.vitepress/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
