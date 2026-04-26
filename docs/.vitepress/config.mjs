import { defineConfig } from 'vitepress'
import { de } from './locales/de.mjs'
import { en } from './locales/en.mjs'
import { it } from './locales/it.mjs'
import { es } from './locales/es.mjs'
import { bg } from './locales/bg.mjs'

export default defineConfig({
  title: "Sanskritkurs",
  description: "Grammatik Lehrbuch von Alois Payer",
  lang: 'de-DE',
  base: '/',
  ignoreDeadLinks: true,
  cleanUrls: true,

  locales: {
    root: { ...de },
    en: { ...en },
    it: { ...it },
    es: { ...es },
    bg: { ...bg }
  },
  
  themeConfig: {
    search: { 
      provider: 'local', 
      options: { 
        miniSearch: {
          options: {
            processTerm: function(term) {
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
          es: { translations: { button: { buttonText: 'Buscar' } } },
          bg: { translations: { button: { buttonText: 'Търсене' } } }
        } 
      }
    }
  }
})
