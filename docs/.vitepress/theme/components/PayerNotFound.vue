<script setup>
import { computed } from 'vue'

const goHome = (e) => {
  e.preventDefault()
  window.location.href = '/'
}

// Simple localization based on current URL path
const texts = computed(() => {
  if (typeof window === 'undefined') {
    return {
      title: 'SEITE NICHT GEFUNDEN',
      quote: 'Wenn Sie Ihre Richtung nicht ändern und weiter suchen, landen Sie möglicherweise dort, wo Sie hinwollen.',
      linkText: 'Zur Startseite'
    }
  }
  const path = window.location.pathname
  if (path.startsWith('/en/')) {
    return {
      title: 'PAGE NOT FOUND',
      quote: "But if you don't change your direction, and if you keep looking, you may end up where you are heading.",
      linkText: 'Take me home'
    }
  } else if (path.startsWith('/it/')) {
    return {
      title: 'PAGINA NON TROVATA',
      quote: "Ma se non cambi direzione, e se continui a guardare, potresti finire proprio dove sei diretto.",
      linkText: 'Portami alla home'
    }
  } else if (path.startsWith('/es/')) {
    return {
      title: 'PÁGINA NO ENCONTRADA',
      quote: "Pero si no cambias de dirección, y si sigues buscando, puedes terminar donde te diriges.",
      linkText: 'Llevarme al inicio'
    }
  } else if (path.startsWith('/fr/')) {
    return {
      title: 'PAGE NON TROUVÉE',
      quote: "Mais si vous ne changez pas de direction, et si vous continuez à chercher, vous risquez de vous retrouver là où vous vous dirigez.",
      linkText: 'Zurück zur Startseite'
    }
  }
  
  // Default to German since DE is root locale
  return {
    title: 'SEITE NICHT GEFUNDEN',
    quote: 'Wenn Sie Ihre Richtung nicht ändern und weiter suchen, landen Sie möglicherweise dort, wo Sie hinwollen.',
    linkText: 'Zur Startseite'
  }
})
</script>

<template>
  <div class="NotFound">
    <p class="code">404</p>
    <h1 class="title">{{ texts.title }}</h1>
    <div class="divider" />
    <blockquote class="quote">
      {{ texts.quote }}
    </blockquote>

    <div class="action">
      <a class="link" href="/" @click="goHome">
        {{ texts.linkText }}
      </a>
    </div>
  </div>
</template>

<style scoped>
.NotFound {
  padding: 64px 24px 96px;
  text-align: center;
  font-family: var(--vp-font-family);
}
@media (min-width: 768px) {
  .NotFound {
    padding: 96px 32px 128px;
  }
}
.code {
  line-height: 64px;
  font-size: 64px;
  font-weight: 600;
  color: var(--vp-c-brand-1);
}
.title {
  padding-top: 12px;
  letter-spacing: 2px;
  line-height: 20px;
  font-size: 20px;
  font-weight: 700;
  color: var(--vp-c-text-1);
}
.divider {
  margin: 24px auto 18px;
  width: 64px;
  height: 1px;
  background-color: var(--vp-c-divider);
}
.quote {
  margin: 0 auto;
  max-width: 256px;
  font-size: 14px;
  font-weight: 500;
  color: var(--vp-c-text-2);
  border-left: none;
  padding: 0;
  font-style: italic;
}
.action {
  padding-top: 20px;
}
.link {
  display: inline-block;
  border: 1px solid var(--vp-c-brand-1);
  border-radius: 16px;
  padding: 3px 16px;
  font-size: 14px;
  font-weight: 500;
  color: var(--vp-c-brand-1);
  transition: border-color 0.25s, color 0.25s;
  text-decoration: none;
}
.link:hover {
  border-color: var(--vp-c-brand-2);
  color: var(--vp-c-brand-2);
}
</style>
