import { defineConfig } from 'vitepress'
// ── v1.2 languages ────────────────────────────────────────────────────────────
import { de } from './locales/de.mjs'
import { en } from './locales/en.mjs'
import { fr } from './locales/fr.mjs'
import { it } from './locales/it.mjs'
import { bg } from './locales/bg.mjs'
import { ru } from './locales/ru.mjs'
import { uk } from './locales/uk.mjs'
import { hi } from './locales/hi.mjs'
// ── v1.3 languages ────────────────────────────────────────────────────────────
import { es } from './locales/es.mjs'
import { ta } from './locales/ta.mjs'
import { pa } from './locales/pa.mjs'
// ── hidden (planned for later versions) ───────────────────────────────────────
// import { rm } from './locales/rm.mjs'
// import { ar } from './locales/ar.mjs'
// import { arc } from './locales/arc.mjs'
// import { he } from './locales/he.mjs'
// import { zh } from './locales/zh.mjs'
// import { la } from './locales/la.mjs'
// import { grc } from './locales/grc.mjs'
// import { el } from './locales/el.mjs'
// import { fa } from './locales/fa.mjs'
// import { akk } from './locales/akk.mjs'
// import { cop } from './locales/cop.mjs'
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

ta.themeConfig.sidebar[3].items = getSidebarItems('lektion', 'பாடம்', 'ta', 10)
ta.themeConfig.sidebar[4].items = getSidebarItems('schrift', 'எழுத்து', 'ta')
ta.themeConfig.sidebar[5].items = getSidebarItems('uebung', 'பயிற்சி', 'ta', 10)

pa.themeConfig.sidebar[3].items = getSidebarItems('lektion', 'ਪਾਠ', 'pa', 10)
pa.themeConfig.sidebar[4].items = getSidebarItems('schrift', 'ਲਿਪੀ', 'pa')
pa.themeConfig.sidebar[5].items = getSidebarItems('uebung', 'ਅਭਿਆਸ', 'pa', 10)

bg.themeConfig.sidebar[3].items = getSidebarItems('lektion', 'Урок', 'bg', 10)
bg.themeConfig.sidebar[4].items = getSidebarItems('schrift', 'Писмо', 'bg')
bg.themeConfig.sidebar[5].items = getSidebarItems('uebung', 'Упражнение', 'bg', 10)

ru.themeConfig.sidebar[3].items = getSidebarItems('lektion', 'Лекция', 'ru', 10)
ru.themeConfig.sidebar[4].items = getSidebarItems('schrift', 'Письмо', 'ru')
ru.themeConfig.sidebar[5].items = getSidebarItems('uebung', 'Упражнение', 'ru', 10)

uk.themeConfig.sidebar[3].items = getSidebarItems('lektion', 'Лекція', 'uk', 10)
uk.themeConfig.sidebar[4].items = getSidebarItems('schrift', 'Письмо', 'uk')
uk.themeConfig.sidebar[5].items = getSidebarItems('uebung', 'Вправа', 'uk', 10)

hi.themeConfig.sidebar[3].items = getSidebarItems('lektion', 'पाठ', 'hi', 10)
hi.themeConfig.sidebar[4].items = getSidebarItems('schrift', 'लिपि', 'hi')
hi.themeConfig.sidebar[5].items = getSidebarItems('uebung', 'अभ्यास', 'hi', 10)

fr.themeConfig.sidebar[3].items = getSidebarItems('lektion', 'Leçon', 'fr', 10)
fr.themeConfig.sidebar[4].items = getSidebarItems('schrift', 'Écriture', 'fr')
fr.themeConfig.sidebar[5].items = getSidebarItems('uebung', 'Exercice', 'fr', 10)

// rm.themeConfig.sidebar[3].items = getSidebarItems('lektion', 'Lecziun', 'rm', 10)
// rm.themeConfig.sidebar[4].items = getSidebarItems('schrift', 'Scrittira', 'rm')
// rm.themeConfig.sidebar[5].items = getSidebarItems('uebung', 'Exercizi', 'rm', 10)
// ta.themeConfig.sidebar[3].items = getSidebarItems('lektion', 'பாடம்', 'ta', 10)
// ta.themeConfig.sidebar[4].items = getSidebarItems('schrift', 'எழுத்து', 'ta')
// ta.themeConfig.sidebar[5].items = getSidebarItems('uebung', 'பயிற்சி', 'ta', 10)
// ar.themeConfig.sidebar[3].items = getSidebarItems('lektion', 'الدرس', 'ar', 10)
// ar.themeConfig.sidebar[4].items = getSidebarItems('schrift', 'الكتابة', 'ar')
// ar.themeConfig.sidebar[5].items = getSidebarItems('uebung', 'التمرين', 'ar', 10)
// arc.themeConfig.sidebar[3].items = getSidebarItems('lektion', 'ܡܠܦܢܘܬܐ', 'arc', 10)
// arc.themeConfig.sidebar[4].items = getSidebarItems('schrift', 'ܟܬܒܬܐ', 'arc')
// arc.themeConfig.sidebar[5].items = getSidebarItems('uebung', 'ܬܪܓܘܡܐ', 'arc', 10)
// he.themeConfig.sidebar[3].items = getSidebarItems('lektion', 'שיעור', 'he', 10)
// he.themeConfig.sidebar[4].items = getSidebarItems('schrift', 'כתב', 'he')
// he.themeConfig.sidebar[5].items = getSidebarItems('uebung', 'תרגיל', 'he', 10)
// zh.themeConfig.sidebar[3].items = getSidebarItems('lektion', '第', 'zh', 10)
// zh.themeConfig.sidebar[4].items = getSidebarItems('schrift', '书写', 'zh')
// zh.themeConfig.sidebar[5].items = getSidebarItems('uebung', '练习', 'zh', 10)
// la.themeConfig.sidebar[3].items = getSidebarItems('lektion', 'Lectio', 'la', 10)
// la.themeConfig.sidebar[4].items = getSidebarItems('schrift', 'Scriptura', 'la')
// la.themeConfig.sidebar[5].items = getSidebarItems('uebung', 'Exercitatio', 'la', 10)
// grc.themeConfig.sidebar[3].items = getSidebarItems('lektion', 'Μάθημα', 'grc', 10)
// grc.themeConfig.sidebar[4].items = getSidebarItems('schrift', 'Γραφή', 'grc')
// grc.themeConfig.sidebar[5].items = getSidebarItems('uebung', 'Ἄσκησις', 'grc', 10)
// el.themeConfig.sidebar[3].items = getSidebarItems('lektion', 'Μάθημα', 'el', 10)
// el.themeConfig.sidebar[4].items = getSidebarItems('schrift', 'Γραφή', 'el')
// el.themeConfig.sidebar[5].items = getSidebarItems('uebung', 'Άσκηση', 'el', 10)
// fa.themeConfig.sidebar[3].items = getSidebarItems('lektion', 'درس', 'fa', 10)
// fa.themeConfig.sidebar[4].items = getSidebarItems('schrift', 'خط', 'fa')
// fa.themeConfig.sidebar[5].items = getSidebarItems('uebung', 'تمرین', 'fa', 10)
// akk.themeConfig.sidebar[3].items = getSidebarItems('lektion', 'Ṭupšarru', 'akk', 10)
// akk.themeConfig.sidebar[4].items = getSidebarItems('schrift', 'Šiṭru', 'akk')
// akk.themeConfig.sidebar[5].items = getSidebarItems('uebung', 'Birku', 'akk', 10)
// cop.themeConfig.sidebar[3].items = getSidebarItems('lektion', 'ⲙⲁⲑⲏⲙⲁ', 'cop', 10)
// cop.themeConfig.sidebar[4].items = getSidebarItems('schrift', 'ⲥϧⲁⲓ', 'cop')
// cop.themeConfig.sidebar[5].items = getSidebarItems('uebung', 'ⲙⲉⲗⲉⲧⲏ', 'cop', 10)

export default defineConfig({
  title: "Sanskritkurs",
  description: "Grammatik Lehrbuch von Alois Payer",
  lang: 'de-DE',
  base: '/',
  ignoreDeadLinks: true,
  cleanUrls: true,

  locales: {
    // ── v1.2 languages ──────────────────────────────────────────────────────────
    root: { ...de },
    en: { ...en },
    it: { ...it },
    bg: { ...bg },
    ru: { ...ru },
    uk: { ...uk },
    hi: { ...hi },
    fr: { ...fr },
    // ── v1.3 languages ───────────────────────────────────────────────────────────
    es: { ...es },
    ta: { ...ta },
    pa: { ...pa },
    // ── hidden (planned for later versions) ─────────────────────────────────────
    // rm: { ...rm },
    // ar: { ...ar },
    // arc: { ...arc },
    // he: { ...he },
    // zh: { ...zh },
    // la: { ...la },
    // grc: { ...grc },
    // el: { ...el },
    // fa: { ...fa },
    // akk: { ...akk },
    // cop: { ...cop },
  },
  
  themeConfig: {
    search: { 
      provider: 'local', 
      options: {
        detailedView: true,
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
          },
          searchOptions: {
            fuzzy: false,
            prefix: function(term) { return term.length >= 4; },
            boost: { title: 5, text: 1, titles: 3 },
            filter: function(result) {
              const ACTIVE = ['en','it','bg','ru','uk','hi','fr','es','ta','pa'];
              const seg = (typeof window !== 'undefined' ? window.location.pathname : '/').split('/').filter(Boolean)[0] || '';
              if (ACTIVE.includes(seg)) {
                // Sprachseite: nur Ergebnisse dieser Sprache
                return result.id.startsWith('/' + seg + '/');
              }
              // Root/DE: nur Seiten ohne Sprachpräfix (kein /xx/ am Anfang)
              return !result.id.match(/^\/[a-z]{2,3}\//);
            }
          }
        },
        locales: {
          // ── v1.2 languages ────────────────────────────────────────────────────
          root: { translations: { button: { buttonText: 'Suchen' } } },
          en: { translations: { button: { buttonText: 'Search' } } },
          it: { translations: { button: { buttonText: 'Cerca' } } },
          bg: { translations: { button: { buttonText: 'Търсене' } } },
          ru: { translations: { button: { buttonText: 'Поиск' } } },
          uk: { translations: { button: { buttonText: 'Пошук' } } },
          hi: { translations: { button: { buttonText: 'खोज' } } },
          fr: { translations: { button: { buttonText: 'Rechercher' } } },
          // ── v1.3 languages ────────────────────────────────────────────────────
          es: { translations: { button: { buttonText: 'Buscar' } } },
          ta: { translations: { button: { buttonText: 'தேடு' } } },
          pa: { translations: { button: { buttonText: 'ਖੋਜ' } } },
          // ── hidden (planned for later versions) ───────────────────────────────
          // rm: { translations: { button: { buttonText: 'Tschertgar' } } },
          // ar: { translations: { button: { buttonText: 'بحث' } } },
          // arc: { translations: { button: { buttonText: 'ܒܥܬܐ' } } },
          // he: { translations: { button: { buttonText: 'חיפוש' } } },
          // zh: { translations: { button: { buttonText: '搜索' } } },
          // la: { translations: { button: { buttonText: 'Quaerere' } } },
          // grc: { translations: { button: { buttonText: 'Ζητεῖν' } } },
          // el: { translations: { button: { buttonText: 'Αναζήτηση' } } },
          // fa: { translations: { button: { buttonText: 'جستجو' } } },
          // akk: { translations: { button: { buttonText: 'Šâlu' } } },
          // cop: { translations: { button: { buttonText: 'ϣⲓⲛⲓ' } } },
        }
      }
    }
  },
  
  markdown: {
    lineNumbers: true,
    breaks: true,
    config: (md) => {
      md.core.ruler.before('normalize', 'prevent_br_link', (state) => {
        state.src = state.src.replace(/\[\[br\]\]\(/g, '[[br]] (');
      });
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
      md.use(container, 'grammar-box2', {
        render: (tokens, idx) => {
          if (tokens[idx].nesting === 1) {
            return `<div class="grammar-box2 custom-block">\n`;
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
      md.use(container, 'metrik-schema', {
        render: (tokens, idx) => {
          if (tokens[idx].nesting === 1) {
            return `<div class="metrik-schema custom-block">\n`;
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

      md.use(container, 'note-box', {
        render: (tokens, idx) => {
          if (tokens[idx].nesting === 1) {
            return `<div class="note-box custom-block">\n`;
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

      md.use(container, 'indent', {
        render: (tokens, idx) => {
          if (tokens[idx].nesting === 1) {
            return `<div class="indent custom-block">\n`;
          } else {
            return `</div>\n`;
          }
        }
      });

      md.use(container, 'compact', {
        render: (tokens, idx) => {
          if (tokens[idx].nesting === 1) {
            return `<div class="compact custom-block">\n`;
          } else {
            return `</div>\n`;
          }
        }
      });

      md.use(container, 'no-header', {
        render: (tokens, idx) => {
          if (tokens[idx].nesting === 1) {
            return `<div class="no-header custom-block">\n`;
          } else {
            return `</div>\n`;
          }
        }
      });
      
      // Fix for markdown-it-attrs tables tbody calculate error with markdown-it-multimd-table:
      // Temporarily rename tbody_close to bypass the buggy calculate rule
      md.core.ruler.before('curly_attributes', 'table_meta_fix', (state) => {
        for (let i = 0; i < state.tokens.length; i++) {
          const token = state.tokens[i];
          if (token.type === 'tbody_close') {
            token.type = 'tbody_close_temp';
          }
        }
      });

      // Restore tbody_close after curly_attributes has finished
      md.core.ruler.after('curly_attributes', 'table_meta_restore', (state) => {
        for (let i = 0; i < state.tokens.length; i++) {
          const token = state.tokens[i];
          if (token.type === 'tbody_close_temp') {
            token.type = 'tbody_close';
          }
        }
      });
      
      // Auto-styling for Devanagari characters and [[br]] replacement
      md.core.ruler.after('linkify', 'scholarly_fixes', (state) => {
        const isHindiPage = state.env?.relativePath?.startsWith('hi/');
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
                  // 1. Process Devanagari (\u27EAmarked\u27EB = Sanskrit, bare = locale-dependent) and [[indent]]
                  const parts = segment.split(/(\u27EA[\u0900-\u097F]+\u27EB|[\u0900-\u097F]+|\[\[indent\]\])/g);
                  parts.forEach(part => {
                    if (part.startsWith('\u27EA') && part.endsWith('\u27EB')) {
                      // Explicitly marked Sanskrit \u2014 always red, strip \u27EA\u27EB wrappers
                      const span = new state.Token('span_open', 'span', 1);
                      span.attrs = [['class', 'sanskrit-dev']];
                      newChildren.push(span);
                      const text = new state.Token('text', '', 0);
                      text.content = part.slice(1, -1);
                      newChildren.push(text);
                      newChildren.push(new state.Token('span_close', 'span', -1));
                    } else if (/[\u0900-\u097F]/.test(part)) {
                      const span = new state.Token('span_open', 'span', 1);
                      span.attrs = [['class', isHindiPage ? 'hindi-dev' : 'sanskrit-dev']];
                      newChildren.push(span);

                      const text = new state.Token('text', '', 0);
                      text.content = part;
                      newChildren.push(text);

                      newChildren.push(new state.Token('span_close', 'span', -1));
                    } else if (part === '[[indent]]') {
                      const span = new state.Token('span_open', 'span', 1);
                      span.attrs = [['class', 'indent-inline']];
                      newChildren.push(span);
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
  },

  buildEnd: async (siteConfig) => {
    const fs = require('fs')
    const path = require('path')
    function copyMdFiles(src, out) {
      if (!fs.existsSync(src)) return
      for (const e of fs.readdirSync(src, { withFileTypes: true })) {
        if (e.name === '.vitepress') continue
        const s = path.join(src, e.name), d = path.join(out, e.name)
        if (e.isDirectory()) copyMdFiles(s, d)
        else if (e.name.endsWith('.md')) {
          fs.mkdirSync(path.dirname(d), { recursive: true })
          fs.copyFileSync(s, d)
        }
      }
    }
    copyMdFiles(siteConfig.srcDir, siteConfig.outDir)
  }
})
