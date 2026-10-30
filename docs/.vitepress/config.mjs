import { defineConfig } from 'vitepress'
import { ACTIVE_LOCALES } from './languages.mjs'
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
import { te } from './locales/te.mjs'
import { pa } from './locales/pa.mjs'
// ── v1.3 additional ───────────────────────────────────────────────────────────
import { la } from './locales/la.mjs'
import { rm } from './locales/rm.mjs'
import { ro } from './locales/ro.mjs'
// ── hidden (planned for later versions) ───────────────────────────────────────
import { ar } from './locales/ar.mjs'
import { id } from './locales/id.mjs'
import { zhCN } from './locales/zh-CN.mjs'
import { he } from './locales/he.mjs'
import { el } from './locales/el.mjs'
import { th } from './locales/th.mjs'
import { grc } from './locales/grc.mjs'
import { fi } from './locales/fi.mjs'
import { hu } from './locales/hu.mjs'
import { zh } from './locales/zh.mjs'
import { fa } from './locales/fa.mjs'
import { nl } from './locales/nl.mjs'
import { am } from './locales/am.mjs'
import { af } from './locales/af.mjs'
import { lt } from './locales/lt.mjs'
import { sh } from './locales/sh.mjs'
import { sq } from './locales/sq.mjs'
import { pt } from './locales/pt.mjs'
import { tr } from './locales/tr.mjs'
import { vi } from './locales/vi.mjs'
import { da } from './locales/da.mjs'
import { no } from './locales/no.mjs'
import { sv } from './locales/sv.mjs'
import { is } from './locales/is.mjs'
import { cs } from './locales/cs.mjs'
import { createRequire } from 'module'
const require = createRequire(import.meta.url)
const multimd_table = require('markdown-it-multimd-table')
const attrs = require('markdown-it-attrs')
import extensiblePlugin from 'markdown-it-extensible'
import footnote from 'markdown-it-footnote'
import deflist from 'markdown-it-deflist'
import { getSidebarItems } from './utils.mjs'

function populateSidebar(localeObj, lektionLabel, lektionPrefix, schriftLabel, uebungLabel) {
  if (!localeObj || !localeObj.themeConfig || !Array.isArray(localeObj.themeConfig.sidebar)) return;
  if (lektionPrefix !== 'root' && !ACTIVE_LOCALES.includes(lektionPrefix)) return;
  const itemGroups = localeObj.themeConfig.sidebar.filter(g => Array.isArray(g.items));
  if (itemGroups[0]) itemGroups[0].items = getSidebarItems('lektion', lektionLabel, lektionPrefix, 10);
  if (itemGroups[1]) itemGroups[1].items = getSidebarItems('schrift', schriftLabel, lektionPrefix);
  if (itemGroups[2]) itemGroups[2].items = getSidebarItems('uebung', uebungLabel, lektionPrefix, 10);
}

populateSidebar(de, 'Lektion', 'root', 'Schrift', 'Übung');
populateSidebar(en, 'Lesson', 'en', 'Script', 'Exercise');
populateSidebar(it, 'Lezione', 'it', 'Scrittura', 'Esercizio');
populateSidebar(es, 'Lección', 'es', 'Escritura', 'Ejercicio');
populateSidebar(ta, 'பாடம்', 'ta', 'எழுத்து', 'பயிற்சி');
populateSidebar(te, 'పాఠం', 'te', 'లిపి', 'అభ్యాసం');
populateSidebar(pa, 'ਪਾਠ', 'pa', 'ਲਿਪੀ', 'ਅਭਿਆਸ');
populateSidebar(ru, 'Лекция', 'ru', 'Письмо', 'Упражнение');
populateSidebar(uk, 'Лекція', 'uk', 'Письмо', 'Вправа');
populateSidebar(hi, 'पाठ', 'hi', 'लिपि', 'अभ्यास');
populateSidebar(fr, 'Leçon', 'fr', 'Écriture', 'Exercice');
populateSidebar(rm, 'Lecziun', 'rm', 'Scrittira', 'Exercizi');
populateSidebar(ro, 'Lecție', 'ro', 'Scriere', 'Exercițiu');
populateSidebar(ar, 'الدرس', 'ar', 'الكتابة', 'التمرين');
populateSidebar(he, 'שיעור', 'he', 'כתב', 'תרגיל');
populateSidebar(la, 'Lectio', 'la', 'Scriptura', 'Exercitatio');
populateSidebar(id, 'Pelajaran', 'id', 'Aksara', 'Latihan');
populateSidebar(zhCN, '第', 'zh-CN', '书写', '练习');
populateSidebar(fi, 'Oppitunti', 'fi', 'Kirjoitusjärjestelmä', 'Harjoitus');
populateSidebar(hu, 'Lecke', 'hu', 'Írásrendszer', 'Gyakorlat');
populateSidebar(el, 'Μάθημα', 'el', 'Γραφή', 'Άσκηση');
populateSidebar(th, 'บทที่', 'th', 'ตัวอักษร', 'แบบฝึกหัด');
populateSidebar(grc, 'Μάθημα', 'grc', 'Γραφή', 'Ἄσκησις');
populateSidebar(zh, '第', 'zh', '書寫', '練習');
populateSidebar(fa, 'درس', 'fa', 'خط', 'تمرین');
populateSidebar(nl, 'Les', 'nl', 'Schrift', 'Oefening');
populateSidebar(am, 'ትምህርት', 'am', 'ጽሕፈት', 'መልመጃ');
populateSidebar(af, 'Lesing', 'af', 'Skrif', 'Oefening');
populateSidebar(lt, 'Pamoka', 'lt', 'Raštas', 'Pratimas');
populateSidebar(sh, 'Lekcija', 'sh', 'Pismo', 'Vežba');
populateSidebar(sq, 'Mësimi', 'sq', 'Shkrimi', 'Ushtrimi');
populateSidebar(pt, 'Lição', 'pt', 'Escrita', 'Exercício');
populateSidebar(bg, 'Урок', 'bg', 'Писмо', 'Упражнение');
populateSidebar(tr, 'Ders', 'tr', 'Yazı', 'Egzersiz');
populateSidebar(vi, 'Bài học', 'vi', 'Chữ viết', 'Bài tập');
populateSidebar(da, 'Lektion', 'da', 'Skrift', 'Øvelse');
populateSidebar(no, 'Leksjon', 'no', 'Skrift', 'Oppgave');
populateSidebar(sv, 'Lektion', 'sv', 'Skrift', 'Övning');
populateSidebar(is, 'Kennslustund', 'is', 'Skrift', 'Æfing');
populateSidebar(cs, 'Lekce', 'cs', 'Písmo', 'Cvičení');

const isDesktop = process.env.DESKTOP_BUILD === '1' || process.env.DESKTOP_BUILD === 'true';

const desktopExcludes = [
  'af/**', 'am/**', 'ar/**', 'bg/**', 'cs/**', 'da/**', 'el/**', 'es/**', 'fa/**', 'fi/**', 'fr/**', 'gez/**', 'grc/**', 'he/**', 'hi/**', 'hu/**', 'hy/**', 'id/**', 'is/**', 'it/**', 'ka/**', 'la/**', 'lt/**', 'nl/**', 'no/**', 'pa/**', 'pl/**', 'pt/**', 'rm/**', 'ro/**', 'ru/**', 'sh/**', 'si/**', 'sk/**', 'sl/**', 'sq/**', 'sv/**', 'ta/**', 'te/**', 'th/**', 'tr/**', 'uk/**', 'vi/**', 'zh/**', 'zh-CN/**'
];

const allLangDirs = [
  'af', 'am', 'bg', 'da', 'fa', 'fi', 'gez', 'grc', 'hu', 'hy', 'is', 'ka', 'la', 'lt', 'nl', 'no', 'pa', 'pl', 'pt', 'ro', 'sh', 'si', 'sk', 'sl', 'sq', 'sv', 'te', 'th', 'tr', 'vi'
];
const webExcludes = allLangDirs.filter(d => !ACTIVE_LOCALES.includes(d)).map(d => `${d}/**`);

const localeObjects = {
  de, en, it, ru, uk, hi, fr, es, ta, te, pa, la, rm, ro, id, 'zh-CN': zhCN, he, ar, el, th, grc, fi, hu, zh, fa, nl, am, af, lt, sh, sq, pt, bg, tr, vi, da, no, sv, is, cs
};
const allLocales = ACTIVE_LOCALES.map(code => localeObjects[code]).filter(Boolean);

const publishedWebLocales = {};
for (const code of ACTIVE_LOCALES) {
  if (code === 'de') {
    publishedWebLocales.root = { ...de };
  } else if (localeObjects[code]) {
    publishedWebLocales[code] = { ...localeObjects[code] };
  }
}

// QA Viewer navbar link enabled for convenient testing

export default defineConfig({
  title: "Sanskritkurs",
  description: "Grammatik Lehrbuch von Alois Payer",
  lang: 'de-DE',
  base: '/',
  ignoreDeadLinks: true,
  cleanUrls: true,
  srcExclude: [...(isDesktop ? desktopExcludes : webExcludes), '**/*.pdf', '**/*.epub'],

  head: [
    ['link', { rel: 'icon', href: '/favicon.ico', sizes: 'any' }],
    ['link', { rel: 'icon', href: '/favicon.png', type: 'image/png' }],
    ['link', { rel: 'manifest', href: '/manifest.json' }],
    ['meta', { name: 'theme-color', content: '#03192e' }],
    ['meta', { name: 'apple-mobile-web-app-capable', content: 'yes' }],
    ['meta', { name: 'apple-mobile-web-app-status-bar-style', content: 'black-translucent' }],
    ['meta', { name: 'apple-mobile-web-app-title', content: 'Sanskritkurs' }],
    ['link', { rel: 'apple-touch-icon', href: '/og-icon.png' }],
    ['meta', { name: 'mobile-web-app-capable', content: 'yes' }],
    ['meta', { property: 'og:type', content: 'website' }],
    ['meta', { property: 'og:image', content: 'https://payer.birchville.org/og-icon.png' }],
    ['meta', { property: 'og:image:width', content: '128' }],
    ['meta', { property: 'og:image:height', content: '128' }],
    ['meta', { name: 'twitter:card', content: 'summary' }],
    ['meta', { name: 'twitter:image', content: 'https://payer.birchville.org/og-icon.png' }],
  ],

  locales: isDesktop ? {
    root: { ...de },
    en: { ...en }
  } : publishedWebLocales,
  
  themeConfig: {
    logo: '/birchville_logo.png',
    siteTitle: 'Sanskritkurs',
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
              const seg = (typeof window !== 'undefined' ? window.location.pathname : '/').split('/').filter(Boolean)[0] || '';
              if (seg.match(/^[a-z]{2,3}(-[A-Z]{2})?$/)) {
                // Sprachseite: nur Ergebnisse dieser Sprache
                return result.id.startsWith('/' + seg + '/');
              }
              // Root/DE: nur Seiten ohne Sprachpräfix (kein /xx/ oder /xx-XX/ am Anfang)
              return !result.id.match(/^\/[a-z]{2,3}(-[A-Z]{2})?\//);
            }
          }
        },
        locales: {
          root: { translations: { button: { buttonText: 'Suchen' } } },
          en: { translations: { button: { buttonText: 'Search' } } },
          fr: { translations: { button: { buttonText: 'Rechercher' } } },
          it: { translations: { button: { buttonText: 'Cerca' } } },
          rm: { translations: { button: { buttonText: 'Tschertgar' } } },
          es: { translations: { button: { buttonText: 'Buscar' } } },
          el: { translations: { button: { buttonText: 'Αναζήτηση' } } },
          hi: { translations: { button: { buttonText: 'खोज' } } },
          ta: { translations: { button: { buttonText: 'தேடு' } } },
          te: { translations: { button: { buttonText: 'వెతకండి' } } },
          ar: { translations: { button: { buttonText: 'بحث' } } },
          he: { translations: { button: { buttonText: 'חפש' } } },
          ru: { translations: { button: { buttonText: 'Поиск' } } },
          uk: { translations: { button: { buttonText: 'Пошук' } } },
          cs: { translations: { button: { buttonText: 'Hledat' } } },
          'zh-CN': { translations: { button: { buttonText: '搜索' } } },
          zh: { translations: { button: { buttonText: '搜尋' } } },
          id: { translations: { button: { buttonText: 'Cari' } } }
        }
      }
    }
  },
  
  markdown: {
    lineNumbers: false,
    breaks: true,
    config: (md) => {
      md.use(attrs)
      md.use(footnote)
      md.use(deflist)

      md.use(multimd_table, {
        multiline: true,
        rowspan: true,
        headerless: true,
        multiscript: true,
        colspans: true
      });

      // Normalize any signal-red directive without leading colon: sig[...] -> :sig[...]
      md.core.ruler.before('linkify', 'sig_normalize', (state) => {
        state.tokens.forEach(token => {
          if (token.type === 'inline' && token.content && token.content.includes('sig[')) {
            token.content = token.content.replace(/(?<!:)sig\[/g, ':sig[');
            if (token.children) {
              token.children.forEach(c => {
                if (c.type === 'text' && c.content && c.content.includes('sig[')) {
                  c.content = c.content.replace(/(?<!:)sig\[/g, ':sig[');
                }
              });
            }
          }
        });
      });

      const blockContainers = [
        { name: 'grammar-box', className: 'grammar-box' },
        { name: 'grammarbox', className: 'grammar-box' },
        { name: 'warning-box', className: 'warning-box' },
        { name: 'warningbox', className: 'warning-box' },
        { name: 'verse-box', className: 'verse-box' },
        { name: 'versebox', className: 'verse-box' },
        { name: 'note-box', className: 'note-box' },
        { name: 'notebox', className: 'note-box' },
        { name: 'indent', className: 'indent' },
        { name: 'media', className: 'media' },
        { name: 'no-header', className: 'no-header' },
        { name: 'noheader', className: 'no-header' },

        // Graceful Aliasing für Alt-Container (Abwärtskompatibilität)
        { name: 'important', className: 'warning-box' },
        { name: 'literatur-box', className: 'note-box' },
        { name: 'literatur', className: 'note-box' },
        { name: 'compact', className: 'verse-box' },

        // Strukturelle & Redaktionelle Legacy-Container
        { name: 'grammar-box2', className: 'grammar-box2' },
        { name: 'grammarbox2', className: 'grammar-box2' },
        { name: 'metrik-schema', className: 'metrik-schema' },
        { name: 'metrikschema', className: 'metrik-schema' },
        { name: 'center', className: 'center' },
        { name: 'laut-table', className: 'laut-table' },
        { name: 'lauttable', className: 'laut-table' },
        { name: 'deleteme-box', className: 'deleteme-box' },
        { name: 'deletemebox', className: 'deleteme-box' }
      ];

      md.use(extensiblePlugin, { blockContainers });
    }
  },


  buildEnd: async (siteConfig) => {
    const fs = require('fs')
    const path = require('path')
    function copyMdFiles(src, out) {
      if (!fs.existsSync(src)) return
      const allowedDesktopDirs = new Set(['de', 'en', 'lektionen', 'public', 'qa'])
      for (const e of fs.readdirSync(src, { withFileTypes: true })) {
        if (e.name === '.vitepress' || e.name === 'deleteme') continue
        if (isDesktop && e.isDirectory() && !allowedDesktopDirs.has(e.name)) continue
        const s = path.join(src, e.name), d = path.join(out, e.name)
        if (e.isDirectory()) copyMdFiles(s, d)
        else if (e.name.endsWith('.md')) {
          fs.mkdirSync(path.dirname(d), { recursive: true })
          fs.copyFileSync(s, d)
        }
      }
    }
    copyMdFiles(siteConfig.srcDir, siteConfig.outDir)

    // Force copy qa_viewer.html to output dir
    const qaHtmlSrc = path.join(siteConfig.srcDir, 'public', 'qa_viewer.html')
    const qaHtmlDest = path.join(siteConfig.outDir, 'qa_viewer.html')
    if (fs.existsSync(qaHtmlSrc)) {
      fs.copyFileSync(qaHtmlSrc, qaHtmlDest)
    }
  }
})
