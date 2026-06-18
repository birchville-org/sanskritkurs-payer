export const zhCN = {
  label: '简体中文',
  lang: 'zh-CN',
  link: '/zh-CN/',
  title: 'Sanskrit Course',
  description: 'Grammar textbook by Alois Payer',
  themeConfig: {
    outline: { level: [2, 3], label: '本页内容' },
    returnToTopLabel: 'Return to top',
    sidebarMenuLabel: 'Menu',
    darkModeSwitchLabel: 'Appearance',
    lightModeSwitchTitle: 'Switch to light theme',
    darkModeSwitchTitle: 'Switch to dark theme',
    langMenuLabel: 'Change language',
    nav: [
      { text: 'Home', link: '/zh-CN/' },
      { text: 'TOC', link: '/zh-CN/lektionen/inhaltsverzeichnis' },
      { text: 'QA', link: '/qa_viewer.html', target: '_blank' },
      { text: 'Credits', link: '/zh-CN/impressum' },
      { text: '⚙️', link: '/zh-CN/settings', ariaLabel: 'Open Settings' }
    ],
    docFooter: {
      prev: 'Previous Lesson',
      next: 'Next Lesson'
    },
    sidebar: [
      { text: 'Table of Contents', link: '/zh-CN/lektionen/inhaltsverzeichnis' },
      { text: 'Grammar Topics', link: '/zh-CN/grammatik' },
            { text: 'Grammar Index', link: '/zh-CN/themen' },
      { text: 'Vocabulary', link: '/zh-CN/lektionen/wortliste' },
      { text: 'Glossary', link: '/zh-CN/lektionen/glossar' },
      { text: 'Lessons', collapsed: false, items: [] },
      { text: 'Script (Introduction)', collapsed: true, items: [] },
      { text: 'Exercises', collapsed: true, items: [] },
      { text: 'Legal', collapsed: true, items: [
          { text: 'Legal Notice & Citation', link: '/zh-CN/impressum' },
          { text: 'Image Licenses', link: '/zh-CN/licenses' },
      ]}
    ],
    footer: {
      message: "Part of Tüpfli's Global Village Library",
      copyright: 'Copyright © 2008-2010 Alois Payer'
    }
  }
}
