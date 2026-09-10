export const no = {
  label: '🇳🇴 NO - Norsk',
  lang: 'nb-NO',
  link: '/no/',
  title: 'Sanskritkurs',
  description: 'Grammatikbok av Alois Payer',
  themeConfig: {
    outline: { level: [2, 3], label: 'På denne siden' },
    returnToTopLabel: 'Tilbake til toppen',
    sidebarMenuLabel: 'Meny',
    darkModeSwitchLabel: 'Utseende',
    lightModeSwitchTitle: 'Skift til lys tema',
    darkModeSwitchTitle: 'Skift til mørkt tema',
    langMenuLabel: 'Endre språk',
    nav: [
      { text: 'Hjem', link: '/no/' },
      { text: 'TOC', link: '/no/lektionen/inhaltsverzeichnis' },
      { text: 'QA', link: '/qa_viewer.html', target: '_blank' },
      { text: 'Kreditter', link: '/no/impressum' },
      { text: '<span class="nav-gear-icon"></span>', link: '/no/settings', ariaLabel: 'Åpne Innstillinger' }
    ],
    docFooter: {
      prev: 'Forrige Lektion',
      next: 'Neste Lektion'
    },
    sidebar: [
      { text: 'Innholdsfortegnelse', link: '/no/lektionen/inhaltsverzeichnis' },
      { text: 'Grammatikkemner', link: '/no/grammatik' },
      { text: 'Grammatikkindeks', link: '/no/themen' },
      { text: 'Vokabular', link: '/no/lektionen/wortliste' },
      { text: 'Glossar', link: '/no/lektionen/glossar' },
      { text: 'Lektioner', collapsed: false, items: [] },
      { text: 'Skript (Innledning)', collapsed: true, items: [] },
      { text: 'Oppgaver', collapsed: true, items: [] },
      { text: 'Juridisk', collapsed: true, items: [
          { text: 'Juridisk merknad & Sitat', link: '/no/impressum' },
          { text: 'Bildelisenser', link: '/no/licenses' },
      ]}
    ],
    footer: {
      message: "Del av Tüpfli's Globale Bibliotek",
      copyright: 'Opphavsrett © 2008-2010 Alois Payer'
    }
  }
}
