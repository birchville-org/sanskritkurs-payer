import { defineConfig } from 'vitepress'
import { ACTIVE_LOCALES } from './languages.mjs'
// ── v1.2 languages ────────────────────────────────────────────────────────────
import { de } from './locales/de.mjs'
import { en } from './locales/en.mjs'
import { fr } from './locales/fr.mjs'
import { it } from './locales/it.mjs'
// import { bg } from './locales/bg.mjs'
import { ru } from './locales/ru.mjs'
import { uk } from './locales/uk.mjs'
import { hi } from './locales/hi.mjs'
// ── v1.3 languages ────────────────────────────────────────────────────────────
import { es } from './locales/es.mjs'
import { ta } from './locales/ta.mjs'
import { pa } from './locales/pa.mjs'
// ── v1.3 additional ───────────────────────────────────────────────────────────
import { la } from './locales/la.mjs'
import { rm } from './locales/rm.mjs'
import { ro } from './locales/ro.mjs'
// ── hidden (planned for later versions) ───────────────────────────────────────
import { ar } from './locales/ar.mjs'
// import { arc } from './locales/arc.mjs'
import { id } from './locales/id.mjs'
import { zhCN } from './locales/zh-CN.mjs'
import { he } from './locales/he.mjs'
import { el } from './locales/el.mjs'
import { th } from './locales/th.mjs'
import { grc } from './locales/grc.mjs'
// import { fi } from './locales/fi.mjs'
// import { hu } from './locales/hu.mjs'
import { createRequire } from 'module'
const require = createRequire(import.meta.url)
const multimd_table = require('markdown-it-multimd-table')
const extensiblePlugin = require('markdown-it-extensible')
import { getSidebarItems } from './utils.mjs'

// Populate sidebars dynamically
de.themeConfig.sidebar[5].items = getSidebarItems('lektion', 'Lektion', 'root', 10)
de.themeConfig.sidebar[6].items = getSidebarItems('schrift', 'Schrift', 'root')
de.themeConfig.sidebar[7].items = getSidebarItems('uebung', 'Übung', 'root', 10)

en.themeConfig.sidebar[5].items = getSidebarItems('lektion', 'Lesson', 'en', 10)
en.themeConfig.sidebar[6].items = getSidebarItems('schrift', 'Script', 'en')
en.themeConfig.sidebar[7].items = getSidebarItems('uebung', 'Exercise', 'en', 10)

it.themeConfig.sidebar[5].items = getSidebarItems('lektion', 'Lezione', 'it', 10)
it.themeConfig.sidebar[6].items = getSidebarItems('schrift', 'Scrittura', 'it')
it.themeConfig.sidebar[7].items = getSidebarItems('uebung', 'Esercizio', 'it', 10)

es.themeConfig.sidebar[5].items = getSidebarItems('lektion', 'Lección', 'es', 10)
es.themeConfig.sidebar[6].items = getSidebarItems('schrift', 'Escritura', 'es')
es.themeConfig.sidebar[7].items = getSidebarItems('uebung', 'Ejercicio', 'es', 10)

ta.themeConfig.sidebar[5].items = getSidebarItems('lektion', 'பாடம்', 'ta', 10)
ta.themeConfig.sidebar[6].items = getSidebarItems('schrift', 'எழுத்து', 'ta')
ta.themeConfig.sidebar[7].items = getSidebarItems('uebung', 'பயிற்சி', 'ta', 10)

pa.themeConfig.sidebar[5].items = getSidebarItems('lektion', 'ਪਾਠ', 'pa', 10)
pa.themeConfig.sidebar[6].items = getSidebarItems('schrift', 'ਲਿਪੀ', 'pa')
pa.themeConfig.sidebar[7].items = getSidebarItems('uebung', 'ਅਭਿਆਸ', 'pa', 10)

// bg.themeConfig.sidebar[5].items = getSidebarItems('lektion', 'Урок', 'bg', 10)
// bg.themeConfig.sidebar[6].items = getSidebarItems('schrift', 'Писмо', 'bg')
// bg.themeConfig.sidebar[7].items = getSidebarItems('uebung', 'Упражнение', 'bg', 10)

ru.themeConfig.sidebar[5].items = getSidebarItems('lektion', 'Лекция', 'ru', 10)
ru.themeConfig.sidebar[6].items = getSidebarItems('schrift', 'Письмо', 'ru')
ru.themeConfig.sidebar[7].items = getSidebarItems('uebung', 'Упражнение', 'ru', 10)

uk.themeConfig.sidebar[5].items = getSidebarItems('lektion', 'Лекція', 'uk', 10)
uk.themeConfig.sidebar[6].items = getSidebarItems('schrift', 'Письмо', 'uk')
uk.themeConfig.sidebar[7].items = getSidebarItems('uebung', 'Вправа', 'uk', 10)

hi.themeConfig.sidebar[5].items = getSidebarItems('lektion', 'पाठ', 'hi', 10)
hi.themeConfig.sidebar[6].items = getSidebarItems('schrift', 'लिपि', 'hi')
hi.themeConfig.sidebar[7].items = getSidebarItems('uebung', 'अभ्यास', 'hi', 10)

fr.themeConfig.sidebar[5].items = getSidebarItems('lektion', 'Leçon', 'fr', 10)
fr.themeConfig.sidebar[6].items = getSidebarItems('schrift', 'Écriture', 'fr')
fr.themeConfig.sidebar[7].items = getSidebarItems('uebung', 'Exercice', 'fr', 10)

rm.themeConfig.sidebar[5].items = getSidebarItems('lektion', 'Lecziun', 'rm', 10)
rm.themeConfig.sidebar[6].items = getSidebarItems('schrift', 'Scrittira', 'rm')
rm.themeConfig.sidebar[7].items = getSidebarItems('uebung', 'Exercizi', 'rm', 10)

ro.themeConfig.sidebar[5].items = getSidebarItems('lektion', 'Lecție', 'ro', 10)
ro.themeConfig.sidebar[6].items = getSidebarItems('schrift', 'Scriere', 'ro')
ro.themeConfig.sidebar[7].items = getSidebarItems('uebung', 'Exercițiu', 'ro', 10)
// ta.themeConfig.sidebar[6].items = getSidebarItems('lektion', 'பாடம்', 'ta', 10)
// ta.themeConfig.sidebar[6].items = getSidebarItems('schrift', 'எழுத்து', 'ta')
// ta.themeConfig.sidebar[6].items = getSidebarItems('uebung', 'பயிற்சி', 'ta', 10)
ar.themeConfig.sidebar[3].items = getSidebarItems('lektion', 'الدرس', 'ar', 10)
ar.themeConfig.sidebar[4].items = getSidebarItems('schrift', 'الكتابة', 'ar')
ar.themeConfig.sidebar[5].items = getSidebarItems('uebung', 'التمرين', 'ar', 10)
// arc.themeConfig.sidebar[3].items = getSidebarItems('lektion', 'ܡܠܦܢܘܬܐ', 'arc', 10)
// arc.themeConfig.sidebar[4].items = getSidebarItems('schrift', 'ܟܬܒܬܐ', 'arc')
// arc.themeConfig.sidebar[5].items = getSidebarItems('uebung', 'ܬܪܓܘܡܐ', 'arc', 10)
he.themeConfig.sidebar[3].items = getSidebarItems('lektion', 'שיעור', 'he', 10)
he.themeConfig.sidebar[4].items = getSidebarItems('schrift', 'כתב', 'he')
he.themeConfig.sidebar[5].items = getSidebarItems('uebung', 'תרגיל', 'he', 10)
la.themeConfig.sidebar[4].items = getSidebarItems('lektion', 'Lectio', 'la', 10)
la.themeConfig.sidebar[5].items = getSidebarItems('schrift', 'Scriptura', 'la')
la.themeConfig.sidebar[6].items = getSidebarItems('uebung', 'Exercitatio', 'la', 10)

id.themeConfig.sidebar[5].items = getSidebarItems('lektion', 'Pelajaran', 'id', 10)
id.themeConfig.sidebar[6].items = getSidebarItems('schrift', 'Aksara', 'id')
id.themeConfig.sidebar[7].items = getSidebarItems('uebung', 'Latihan', 'id', 10)

zhCN.themeConfig.sidebar[5].items = getSidebarItems('lektion', '第', 'zh-CN', 10)
zhCN.themeConfig.sidebar[6].items = getSidebarItems('schrift', '书写', 'zh-CN')
zhCN.themeConfig.sidebar[7].items = getSidebarItems('uebung', '练习', 'zh-CN', 10)

// fi.themeConfig.sidebar[5].items = getSidebarItems('lektion', 'Oppitunti', 'fi', 10)
// fi.themeConfig.sidebar[6].items = getSidebarItems('schrift', 'Kirjoitusjärjestelmä', 'fi')
// fi.themeConfig.sidebar[7].items = getSidebarItems('uebung', 'Harjoitus', 'fi', 10)

// hu.themeConfig.sidebar[5].items = getSidebarItems('lektion', 'Lecke', 'hu', 10)
// hu.themeConfig.sidebar[6].items = getSidebarItems('schrift', 'Írásrendszer', 'hu')
// hu.themeConfig.sidebar[7].items = getSidebarItems('uebung', 'Gyakorlat', 'hu', 10)

el.themeConfig.sidebar[3].items = getSidebarItems('lektion', 'Μάθημα', 'el', 10)
el.themeConfig.sidebar[4].items = getSidebarItems('schrift', 'Γραφή', 'el')
el.themeConfig.sidebar[5].items = getSidebarItems('uebung', 'Άσκηση', 'el', 10)

th.themeConfig.sidebar[5].items = getSidebarItems('lektion', 'บทที่', 'th', 10)
th.themeConfig.sidebar[6].items = getSidebarItems('schrift', 'ตัวอักษร', 'th')
th.themeConfig.sidebar[7].items = getSidebarItems('uebung', 'แบบฝึกหัด', 'th', 10)

he.themeConfig.sidebar[5].items = getSidebarItems('lektion', 'שיעור', 'he', 10)
he.themeConfig.sidebar[6].items = getSidebarItems('schrift', 'כתב', 'he')
he.themeConfig.sidebar[7].items = getSidebarItems('uebung', 'תרגיל', 'he', 10)

grc.themeConfig.sidebar[3].items = getSidebarItems('lektion', 'Μάθημα', 'grc', 10)
grc.themeConfig.sidebar[4].items = getSidebarItems('schrift', 'Γραφή', 'grc')
grc.themeConfig.sidebar[5].items = getSidebarItems('uebung', 'Ἄσκησις', 'grc', 10)

const isAuthorBuild = process.env.VITEPRESS_ENV === 'author';
const localeObjects = {
  de, en, it, ru, uk, hi, fr, es, ta, pa, la, rm, ro, id, 'zh-CN': zhCN, he, ar, el, th, grc
};
const allLocales = ACTIVE_LOCALES.map(code => localeObjects[code]).filter(Boolean);

if (!isAuthorBuild) {
  for (const localeObj of allLocales) {
    if (localeObj.themeConfig && localeObj.themeConfig.nav) {
      localeObj.themeConfig.nav = localeObj.themeConfig.nav.filter(item => item.link !== '/qa_viewer.html');
    }
  }
}

export default defineConfig({
  title: "Sanskritkurs",
  description: "Grammatik Lehrbuch von Alois Payer",
  lang: 'de-DE',
  base: '/',
  ignoreDeadLinks: true,
  cleanUrls: true,

  head: [
    ['link', { rel: 'icon', href: '/favicon.ico', sizes: 'any' }],
    ['link', { rel: 'icon', href: '/favicon.png', type: 'image/png' }],
    ['link', { rel: 'manifest', href: '/manifest.json' }],
    ['meta', { name: 'theme-color', content: '#03192e' }],
    ['meta', { name: 'apple-mobile-web-app-capable', content: 'yes' }],
    ['meta', { name: 'apple-mobile-web-app-status-bar-style', content: 'black-translucent' }],
    ['meta', { name: 'apple-mobile-web-app-title', content: 'Sanskritkurs' }],
    ['link', { rel: 'apple-touch-icon', href: '/pwa-icons/icon-192.png' }],
    ['meta', { name: 'mobile-web-app-capable', content: 'yes' }],
  ],

  locales: {
    // ── v1.2 languages ──────────────────────────────────────────────────────────
    root: { ...de },
    en: { ...en },
    it: { ...it },
    // bg: { ...bg },
    ru: { ...ru },
    uk: { ...uk },
    hi: { ...hi },
    fr: { ...fr },
    // ── v1.3 languages ───────────────────────────────────────────────────────────
    es: { ...es },
    ta: { ...ta },
    pa: { ...pa },
    la: { ...la },
    rm: { ...rm },
    id: { ...id },
    'zh-CN': { ...zhCN },
    he: { ...he },
    ar: { ...ar },
    // 'arc': { ...arc },
    el: { ...el },
    th: { ...th },
    ro: { ...ro },
    grc: { ...grc },
    // fi: { ...fi },
    // hu: { ...hu },
  },
  
  themeConfig: {
    logo: '/birchville_logo.png',
    logoLink: 'https://www.birchville.cc',
    socialLinks: [
      { icon: 'github', link: 'https://github.com/marcodem/sanskritkurs-payer' }
    ],
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
              const ACTIVE = ACTIVE_LOCALES.filter(c => c !== 'de');
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
          // bg: { translations: { button: { buttonText: 'Търсене' } } },
          ru: { translations: { button: { buttonText: 'Поиск' } } },
          uk: { translations: { button: { buttonText: 'Пошук' } } },
          hi: { translations: { button: { buttonText: 'खोज' } } },
          fr: { translations: { button: { buttonText: 'Rechercher' } } },
          // ── v1.3 languages ────────────────────────────────────────────────────
          es: { translations: { button: { buttonText: 'Buscar' } } },
          ta: { translations: { button: { buttonText: 'தேடு' } } },
          pa: { translations: { button: { buttonText: 'ਖੋਜ' } } },
          id: { translations: { button: { buttonText: 'Cari' } } },
          'zh-CN': { translations: { button: { buttonText: '搜索' } } },
          he: { translations: { button: { buttonText: 'חפש' } } },
          rm: { translations: { button: { buttonText: 'Tschertgar' } } },
          ar: { translations: { button: { buttonText: 'بحث' } } },
          // arc: { translations: { button: { buttonText: 'ܒܥܬܐ' } } },
          la: { translations: { button: { buttonText: 'Quaerere' } } },
          sq: { translations: { button: { buttonText: 'Kërko' } } },
          el: { translations: { button: { buttonText: 'Αναζήτηση' } } },
          th: { translations: { button: { buttonText: 'ค้นหา' } } },
          ro: { translations: { button: { buttonText: 'Căutare' } } },
          grc: { translations: { button: { buttonText: 'Ἀναζήτησις' } } }
        }
      }
    }
  },
  
  markdown: {
    lineNumbers: isAuthorBuild,
    breaks: true,
    config: (md) => {

      md.use(multimd_table, {
        multiline: true,
        rowspan: true,
        headerless: true,
        multiscript: true,
        colspans: true
      });
      md.use(extensiblePlugin);
    }
  },

  vite: {
    plugins: [
      {
        name: 'qa-save-plugin',
        configureServer(server) {
          server.middlewares.use((req, res, next) => {
            if (req.url === '/api/save' && req.method === 'POST') {
              let body = '';
              req.on('data', chunk => { body += chunk.toString(); });
              req.on('end', () => {
                try {
                  const data = JSON.parse(body);
                  const fs = require('fs');
                  const path = require('path');
                  const absolutePath = path.resolve(process.cwd(), data.filepath);
                  if (!absolutePath.includes('docs/')) {
                     res.statusCode = 403;
                     res.end('Forbidden');
                     return;
                  }
                  fs.writeFileSync(absolutePath, data.content, 'utf-8');
                  res.statusCode = 200;
                  res.end('OK');
                } catch(e) {
                  res.statusCode = 500;
                  res.end(e.message);
                }
              });
              return;
            }
            if (req.url.startsWith('/api/load') && req.method === 'GET') {
              try {
                const url = new URL(req.url, 'http://localhost');
                const filepath = url.searchParams.get('filepath');
                if (!filepath) {
                  res.statusCode = 400;
                  res.end('Missing filepath');
                  return;
                }
                const path = require('path');
                const absolutePath = path.resolve(process.cwd(), filepath);
                if (!absolutePath.includes('docs/')) {
                  res.statusCode = 403;
                  res.end('Forbidden');
                  return;
                }
                const fs = require('fs');
                if (!fs.existsSync(absolutePath)) {
                  res.statusCode = 404;
                  res.end('File not found');
                  return;
                }
                const content = fs.readFileSync(absolutePath, 'utf-8');
                res.statusCode = 200;
                res.setHeader('Content-Type', 'application/json');
                res.end(JSON.stringify({ content }));
              } catch(e) {
                res.statusCode = 500;
                res.end(e.message);
              }
              return;
            }
            next();
          });
        }
      }
    ]
  },

  buildEnd: async (siteConfig) => {
    const fs = require('fs')
    const path = require('path')
    function copyMdFiles(src, out) {
      if (!fs.existsSync(src)) return
      for (const e of fs.readdirSync(src, { withFileTypes: true })) {
        if (e.name === '.vitepress' || e.name === 'deleteme') continue
        const s = path.join(src, e.name), d = path.join(out, e.name)
        if (e.isDirectory()) copyMdFiles(s, d)
        else if (e.name.endsWith('.md')) {
          fs.mkdirSync(path.dirname(d), { recursive: true })
          fs.copyFileSync(s, d)
        }
      }
    }
    copyMdFiles(siteConfig.srcDir, siteConfig.outDir)

    if (!isAuthorBuild) {
      const qaHtml = path.join(siteConfig.outDir, 'qa_viewer.html')
      const qaDir = path.join(siteConfig.outDir, 'qa')
      if (fs.existsSync(qaHtml)) fs.unlinkSync(qaHtml)
      if (fs.existsSync(qaDir)) fs.rmSync(qaDir, { recursive: true, force: true })
    }
  }
})
