# VitePress wird nativ im GitHub Actions Workflow gebaut (AMD64, schnell).
# Dieses Dockerfile kopiert nur das fertige dist/ — kein Node.js via QEMU.
FROM nginx:alpine
ARG BUILD_DIR=dist-public
RUN apk add --no-cache python3
COPY docs/.vitepress/${BUILD_DIR} /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY scripts/qa_auth_broker.py /usr/local/bin/qa_auth_broker.py
COPY scripts/docker-entrypoint.sh /usr/local/bin/docker-entrypoint.sh
EXPOSE 80
ENTRYPOINT ["/usr/local/bin/docker-entrypoint.sh"]
