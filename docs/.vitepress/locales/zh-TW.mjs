export const zhTW = {
  label: 'zh-TW',
  lang: 'zh-TW',
  link: '/zh-TW/',
  title: 'Sanskrit Course',
  description: 'Grammar textbook by Alois Payer',
  themeConfig: {
    outline: { level: [2, 3], label: '本頁內容' },
    returnToTopLabel: 'Return to top',
    sidebarMenuLabel: 'Menu',
    darkModeSwitchLabel: 'Appearance',
    lightModeSwitchTitle: 'Switch to light theme',
    darkModeSwitchTitle: 'Switch to dark theme',
    langMenuLabel: 'Change language',
    nav: [
      { text: 'Home', link: '/zh-TW/' },
      { text: 'TOC', link: '/zh-TW/lektionen/inhaltsverzeichnis' },
      { text: 'QA', link: '/qa_viewer.html', target: '_blank' },
      { text: 'Credits', link: '/zh-TW/impressum' },
      { text: '⚙️', link: '/zh-TW/settings', ariaLabel: 'Open Settings' }
    ],
    docFooter: {
      prev: 'Previous Lesson',
      next: 'Next Lesson'
    },
    sidebar: [
      { text: 'Table of Contents', link: '/zh-TW/lektionen/inhaltsverzeichnis' },
      { text: 'Grammar Topics', link: '/zh-TW/grammatik' },
            { text: 'Grammar Index', link: '/zh-TW/themen' },
      { text: 'Vocabulary', link: '/zh-TW/lektionen/wortliste' },
      { text: 'Glossary', link: '/zh-TW/lektionen/glossar' },
      { text: 'Lessons', collapsed: false, items: [] },
      { text: 'Script (Introduction)', collapsed: true, items: [] },
      { text: 'Exercises', collapsed: true, items: [] },
      { text: 'Legal', collapsed: true, items: [
          { text: 'Legal Notice & Citation', link: '/zh-TW/impressum' },
          { text: 'Image Licenses', link: '/zh-TW/licenses' },
      ]}
    ],
    footer: {
      message: "Part of Tüpfli's Global Village Library",
      copyright: 'Copyright © 2008-2010 Alois Payer'
    }
  }
}
