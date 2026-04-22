import { getSidebarItems } from '../utils.mjs'

export const de = {
  label: 'DE',
  lang: 'de-DE',
  themeConfig: {
    outline: { level: [2, 3], label: 'Auf dieser Seite' },
    nav: [
      { text: 'Home', link: '/' },
      { text: 'Inhaltsverzeichnis', link: '/lektionen/inhaltsverzeichnis' },
      { text: 'Themen-Index', link: '/grammatik' },
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
      { text: 'Lektionen', collapsed: false, items: getSidebarItems('lektion', 'Lektion', 'root', 10) },
      { text: 'Schrift (Einführung)', collapsed: true, items: getSidebarItems('schrift', 'Schrift', 'root') },
      { text: 'Übungen', collapsed: true, items: getSidebarItems('uebung', 'Übung', 'root', 10) },
      { text: 'Rechtliches', collapsed: true, items: [
          { text: 'Impressum & Zitieren', link: '/impressum' },
          { text: 'Bildlizenzen (Audit)', link: '/licenses' }
      ]}
    ]
  }
}
