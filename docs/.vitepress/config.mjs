import { defineConfig } from 'vitepress'
import { de } from './locales/de.mjs'
import { en } from './locales/en.mjs'
import { it } from './locales/it.mjs'
import { es } from './locales/es.mjs'
import { bg } from './locales/bg.mjs'
import { ru } from './locales/ru.mjs'
import { uk } from './locales/uk.mjs'
import { createRequire } from 'module'
const require = createRequire(import.meta.url)
const container = require('markdown-it-container')

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
    bg: { ...bg },
    ru: { ...ru },
    uk: { ...uk }
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
  },
  
  markdown: {
    lineNumbers: true,
    breaks: true,
    config: (md) => {
      md.use(container, 'grammar-box', {
        render: (tokens, idx) => {
          if (tokens[idx].nesting === 1) {
            return `<div class="grammar-box custom-block">\n`;
          } else {
            return `</div>\n`;
          }
        }
      });
      md.use(container, 'media', {
        render: (tokens, idx) => {
          if (tokens[idx].nesting === 1) {
            return `<div class="media custom-block">\n`;
          } else {
            return `</div>\n`;
          }
        }
      });
      md.use(container, 'center', {
        render: (tokens, idx) => {
          if (tokens[idx].nesting === 1) {
            return `<div class="center custom-block">\n`;
          } else {
            return `</div>\n`;
          }
        }
      });
      
      md.use(container, 'important', {
        render: (tokens, idx) => {
          if (tokens[idx].nesting === 1) {
            return `<div class="important custom-block">\n`;
          } else {
            return `</div>\n`;
          }
        }
      });

      md.use(container, 'laut-table', {
        render: (tokens, idx) => {
          if (tokens[idx].nesting === 1) {
            return `<div class="laut-table custom-block">\n`;
          } else {
            return `</div>\n`;
          }
        }
      });
      
      // Auto-styling for Devanagari characters (Scholarly Red)
      md.core.ruler.after('linkify', 'devanagari_styling', (state) => {
        state.tokens.forEach(token => {
          if (token.type === 'inline') {
            let newChildren = [];
            token.children.forEach(child => {
              if (child.type === 'text') {
                // Regex for Devanagari range (U+0900-U+097F)
                const parts = child.content.split(/([\u0900-\u097F]+)/g);
                parts.forEach(part => {
                  if (/[\u0900-\u097F]/.test(part)) {
                    const span = new state.Token('span_open', 'span', 1);
                    span.attrs = [['class', 'sanskrit-dev']];
                    newChildren.push(span);
                    
                    const text = new state.Token('text', '', 0);
                    text.content = part;
                    newChildren.push(text);
                    
                    newChildren.push(new state.Token('span_close', 'span', -1));
                  } else if (part) {
                    const text = new state.Token('text', '', 0);
                    text.content = part;
                    newChildren.push(text);
                  }
                });
              } else {
                newChildren.push(child);
              }
            });
            token.children = newChildren;
          }
        });
      });
    }
  }
})
