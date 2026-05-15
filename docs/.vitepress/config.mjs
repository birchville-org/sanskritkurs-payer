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
const multimd_table = require('markdown-it-multimd-table')
import { getSidebarItems } from './utils.mjs'

// Populate sidebars dynamically
de.themeConfig.sidebar[3].items = getSidebarItems('lektion', 'Lektion', 'root', 10)
de.themeConfig.sidebar[4].items = getSidebarItems('schrift', 'Schrift', 'root')
de.themeConfig.sidebar[5].items = getSidebarItems('uebung', 'Übung', 'root', 10)

en.themeConfig.sidebar[3].items = getSidebarItems('lektion', 'Lesson', 'en', 10)
en.themeConfig.sidebar[4].items = getSidebarItems('schrift', 'Script', 'en')
en.themeConfig.sidebar[5].items = getSidebarItems('uebung', 'Exercise', 'en', 10)

it.themeConfig.sidebar[3].items = getSidebarItems('lektion', 'Lezione', 'it', 10)
it.themeConfig.sidebar[4].items = getSidebarItems('schrift', 'Scrittura', 'it')
it.themeConfig.sidebar[5].items = getSidebarItems('uebung', 'Esercizio', 'it', 10)

es.themeConfig.sidebar[3].items = getSidebarItems('lektion', 'Lección', 'es', 10)
es.themeConfig.sidebar[4].items = getSidebarItems('schrift', 'Escritura', 'es')
es.themeConfig.sidebar[5].items = getSidebarItems('uebung', 'Ejercicio', 'es', 10)

bg.themeConfig.sidebar[3].items = getSidebarItems('lektion', 'Урок', 'bg', 10)
bg.themeConfig.sidebar[4].items = getSidebarItems('schrift', 'Писмо', 'bg')
bg.themeConfig.sidebar[5].items = getSidebarItems('uebung', 'Упражнение', 'bg', 10)

ru.themeConfig.sidebar[3].items = getSidebarItems('lektion', 'Лекция', 'ru', 10)
ru.themeConfig.sidebar[4].items = getSidebarItems('schrift', 'Письмо', 'ru')
ru.themeConfig.sidebar[5].items = getSidebarItems('uebung', 'Упражнение', 'ru', 10)

uk.themeConfig.sidebar[3].items = getSidebarItems('lektion', 'Лекція', 'uk', 10)
uk.themeConfig.sidebar[4].items = getSidebarItems('schrift', 'Письмо', 'uk')
uk.themeConfig.sidebar[5].items = getSidebarItems('uebung', 'Вправа', 'uk', 10)

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
      md.use(multimd_table, {
        multiline: true,
        rowspan: true,
        headerless: true,
        multiscript: true,
        colspans: true
      });
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

      md.use(container, 'deleteme-box', {
        render: (tokens, idx) => {
          if (tokens[idx].nesting === 1) {
            return `<div class="deleteme-box custom-block">\n`;
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
      
      // Auto-styling for Devanagari characters and [[br]] replacement
      md.core.ruler.after('linkify', 'scholarly_fixes', (state) => {
        state.tokens.forEach(token => {
          if (token.type === 'inline') {
            let newChildren = [];
            token.children.forEach(child => {
              if (child.type === 'text') {
                // Combined processing for [[br]] and Devanagari
                let segments = [child.content];
                if (child.content.includes('[[br]]')) {
                  segments = child.content.split('[[br]]');
                }

                segments.forEach((segment, index) => {
                  // 1. Process Devanagari in this segment
                  const deParts = segment.split(/([\u0900-\u097F]+)/g);
                  deParts.forEach(part => {
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

                  // 2. Add break if not the last segment
                  if (index < segments.length - 1) {
                    newChildren.push(new state.Token('hardbreak', 'br', 0));
                  }
                });
                return;
              }
 else {
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
