export const id = {
  label: 'ID',
  lang: 'id-ID',
  link: '/id/',
  title: 'Kursus Sanskerta',
  description: 'Buku teks tata bahasa oleh Alois Payer',
  themeConfig: {
    outline: { level: [2, 3], label: 'Di halaman ini' },
    returnToTopLabel: 'Return to top',
    sidebarMenuLabel: 'Menu',
    darkModeSwitchLabel: 'Appearance',
    lightModeSwitchTitle: 'Switch to light theme',
    darkModeSwitchTitle: 'Switch to dark theme',
    langMenuLabel: 'Change language',
    nav: [
      { text: 'Home', link: '/en/' },
      { text: 'TOC', link: '/en/lektionen/inhaltsverzeichnis' },
      { text: 'QA', link: '/qa_viewer.html', target: '_blank' },
      { text: 'Credits', link: '/en/impressum' },
      { text: '<span class="nav-gear-icon"></span>', link: '/en/settings', ariaLabel: 'Open Settings' }
    ],
    docFooter: {
      prev: 'Previous Lesson',
      next: 'Next Lesson'
    },
    sidebar: [
      { text: 'Table of Contents', link: '/en/lektionen/inhaltsverzeichnis' },
      { text: 'Grammar Topics', link: '/en/grammatik' },
            { text: 'Grammar Index', link: '/en/themen' },
      { text: 'Vocabulary', link: '/en/lektionen/wortliste' },
      { text: 'Glossary', link: '/en/lektionen/glossar' },
      { text: 'Lessons', collapsed: false, items: [] },
      { text: 'Script (Introduction)', collapsed: true, items: [] },
      { text: 'Exercises', collapsed: true, items: [] },
      { text: 'Legal', collapsed: true, items: [
          { text: 'Legal Notice & Citation', link: '/en/impressum' },
          { text: 'Image Licenses', link: '/en/licenses' },
      ]}
    ],
    footer: {
      message: "Part of Tüpfli's Global Village Library",
      copyright: 'Copyright © 2008-2010 Alois Payer'
    }
  }
}
