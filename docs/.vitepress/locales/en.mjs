
export const en = {
  label: 'EN',
  lang: 'en-US',
  link: '/en/',
  title: 'Sanskrit Course',
  description: 'Grammar textbook by Alois Payer',
  themeConfig: {
    outline: { level: [2, 3], label: 'On this page' },
    returnToTopLabel: 'Return to top',
    sidebarMenuLabel: 'Menu',
    darkModeSwitchLabel: 'Appearance',
    lightModeSwitchTitle: 'Switch to light theme',
    darkModeSwitchTitle: 'Switch to dark theme',
    langMenuLabel: 'Change language',
    nav: [
      { text: 'Home', link: '/en/' },
      { text: 'TOC', link: '/en/lektionen/inhaltsverzeichnis' },
      { text: 'Index', link: '/en/grammatik' },
      { text: 'QA', link: '/qa_viewer.html', target: '_blank' },
      { text: 'Credits', link: '/en/impressum' }
    ],
    docFooter: {
      prev: 'Previous Lesson',
      next: 'Next Lesson'
    },
    sidebar: [
      { text: 'Table of Contents', link: '/en/lektionen/inhaltsverzeichnis' },
      { text: 'Grammar Topics (Index)', link: '/en/grammatik' },
      { text: 'Vocabulary', link: '/en/lektionen/wortliste' },
      { text: 'Glossary', link: '/en/lektionen/glossar' },
      { text: 'Lessons', collapsed: false, items: [] },
      { text: 'Script (Introduction)', collapsed: true, items: [] },
      { text: 'Exercises', collapsed: true, items: [] },
      { text: 'Legal', collapsed: true, items: [
          { text: 'Legal Notice & Citation', link: '/en/impressum' },
          { text: 'Image Licenses', link: '/en/licenses' }
      ]}
    ],
    footer: {
      message: "Part of Tüpfli's Global Village Library",
      copyright: 'Copyright © 2008-2010 Alois Payer'
    }
  }
}
