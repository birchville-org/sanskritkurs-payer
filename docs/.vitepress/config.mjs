import { defineConfig } from 'vitepress'
import { de } from './locales/de.mjs'
import { en } from './locales/en.mjs'

export default defineConfig({
  title: "Sanskritkurs",
  description: "Grammatik Lehrbuch von Alois Payer",
  cleanUrls: true,

  locales: {
    root: { ...de },
    en: { ...en },
    it: { label: 'IT', lang: 'it-IT', link: '/it/' },
    es: { label: 'ES', lang: 'es-ES', link: '/es/' }
  },
  
  themeConfig: {
    search: { 
      provider: 'local', 
      options: { 
        miniSearch: {
          options: {
            processTerm: function(term) {
              // DEBUG_V6: Ensure no external references
              if (!term) return term;
              const map = {
                'ā': 'a', 'ī': 'i', 'ū': 'u', 'ṛ': 'r', 'ṝ': 'r', 'ḷ': 'l', 'ḹ': 'l',
                'ṁ': 'm', 'ṃ': 'm', 'ḥ': 'h', 'ṅ': 'n', 'ñ': 'n', 'ṭ': 't', 'ḍ': 'd',
                'ṇ': 'n', 'ś': 's', 'ṣ': 's'
              };
              let n = term.toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g, '');
              for (const k in map) {
                n = n.replace(new RegExp(k, 'g'), map[k]);
              }
              return n;
            }
          }
        },
        locales: { 
          root: { translations: { button: { buttonText: 'Suchen' } } },
          en: { translations: { button: { buttonText: 'Search' } } },
          it: { translations: { button: { buttonText: 'Cerca' } } },
          es: { translations: { button: { buttonText: 'Buscar' } } }
        } 
      } 
    },
    footer: {
      message: "Teil der Tüpfli's Global Village Library",
      copyright: 'Copyright © 2008-2010 Alois Payer'
    }
  }
})
