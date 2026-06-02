export const de = {
  label: 'DE',
  lang: 'de-DE',
  title: 'Sanskritkurs',
  description: 'Grammatik Lehrbuch von Alois Payer',
  themeConfig: {
    outline: { level: [2, 3], label: 'Auf dieser Seite' },
    returnToTopLabel: 'Zurück nach oben',
    sidebarMenuLabel: 'Menü',
    darkModeSwitchLabel: 'Erscheinungsbild',
    lightModeSwitchTitle: 'Zum hellen Design wechseln',
    darkModeSwitchTitle: 'Zum dunklen Design wechseln',
    langMenuLabel: 'Sprache wechseln',
    nav: [
      { text: 'Home', link: '/' },
      { text: 'Inhaltsverzeichnis', link: '/lektionen/inhaltsverzeichnis' },
      { text: 'Themen-Index', link: '/grammatik' },
      { text: 'QA', link: '/qa_viewer.html', target: '_blank' },
      { text: 'Impressum', link: '/impressum' }
    ],
    docFooter: {
      prev: 'Vorherige Lektion',
      next: 'Nächste Lektion'
    },
    sidebar: [
      { text: 'Inhaltsverzeichnis', link: '/lektionen/inhaltsverzeichnis' },
      { text: 'Grammatik Themen (Index)', link: '/grammatik' },
      { text: 'Wortliste', link: '/lektionen/wortliste' },
      { text: 'Glossar', link: '/lektionen/glossar' },
      { text: 'Lektionen', collapsed: false, items: [] },
      { text: 'Schrift (Einführung)', collapsed: true, items: [] },
      { text: 'Übungen', collapsed: true, items: [] },
      { text: 'Rechtliches', collapsed: true, items: [
          { text: 'Impressum & Zitieren', link: '/impressum' },
          { text: 'Bildlizenzen (Audit)', link: '/licenses' }
      ]}
    ],
    footer: {
      message: "Teil der Tüpfli's Global Village Library",
      copyright: 'Copyright © 2008-2010 Alois Payer'
    }
  }
}
