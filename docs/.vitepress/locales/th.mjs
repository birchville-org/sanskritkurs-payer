export const th = {
  label: '🇹🇭 TH - ไทย',
  lang: 'th-TH',
  link: '/th/',
  title: 'Sanskrit Course',
  description: 'Grammar textbook by Alois Payer',
  themeConfig: {
    outline: { level: [2, 3], label: 'ในหน้านี้' },
    returnToTopLabel: 'กลับสู่ด้านบน',
    sidebarMenuLabel: 'เมนู',
    darkModeSwitchLabel: 'ลักษณะ',
    lightModeSwitchTitle: 'เปลี่ยนเป็นธีมสว่าง',
    darkModeSwitchTitle: 'เปลี่ยนเป็นธีมมืด',
    langMenuLabel: 'เปลี่ยนภาษา',
    nav: [
      { text: 'Home', link: '/th/' },
      { text: 'TOC', link: '/th/lektionen/inhaltsverzeichnis' },
      { text: 'QA', link: '/qa_viewer.html', target: '_blank' },
      { text: 'Credits', link: '/th/impressum' },
      { text: '<span class="nav-gear-icon"></span>', link: '/th/settings', ariaLabel: 'Open Settings' }
    ],
    docFooter: {
      prev: 'บทก่อนหน้า',
      next: 'บทถัดไป'
    },
    sidebar: [
      { text: 'Table of Contents', link: '/th/lektionen/inhaltsverzeichnis' },
      { text: 'Grammar Topics', link: '/th/grammatik' },
            { text: 'Grammar Index', link: '/th/themen' },
      { text: 'Vocabulary', link: '/th/lektionen/wortliste' },
      { text: 'Glossary', link: '/th/lektionen/glossar' },
      { text: 'Lessons', collapsed: false, items: [] },
      { text: 'Script (Introduction)', collapsed: true, items: [] },
      { text: 'Exercises', collapsed: true, items: [] },
      { text: 'Legal', collapsed: true, items: [
          { text: 'Legal Notice & Citation', link: '/th/impressum' },
          { text: 'Image Licenses', link: '/th/licenses' },
      ]}
    ],
    footer: {
      message: "Part of Tüpfli's Global Village Library",
      copyright: 'Copyright © 2008-2010 Alois Payer'
    }
  }
}
