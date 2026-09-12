export const no = {
  label: '🇳🇴 NO - Norsk',
  lang: 'nb-NO',
  link: '/no/',
  title: 'Sanskritkurs',
  description: 'Lærebok i sanskrit av Alois Payer',
  themeConfig: {
    outline: { level: [2, 3], label: 'På denne siden' },
    returnToTopLabel: 'Tilbake til toppen',
    sidebarMenuLabel: 'Meny',
    darkModeSwitchLabel: 'Utseende',
    lightModeSwitchTitle: 'Bytt til lyst tema',
    darkModeSwitchTitle: 'Bytt til mørkt tema',
    langMenuLabel: 'Endre språk',
    nav: [
      { text: 'Hjem', link: '/no/' },
      { text: 'Innholdsfortegnelse', link: '/no/lektionen/inhaltsverzeichnis' },
      { text: 'QA', link: '/qa_viewer.html', target: '_blank' },
      { text: 'Kolofon', link: '/no/impressum' },
      { text: '<span class="nav-gear-icon"></span>', link: '/no/settings', ariaLabel: 'Åpne innstillinger' }
    ],
    docFooter: {
      prev: 'Forrige leksjon',
      next: 'Neste leksjon'
    },
    sidebar: [
      { text: 'Innholdsfortegnelse', link: '/no/lektionen/inhaltsverzeichnis' },
      { text: 'Grammatikkemner', link: '/no/grammatik' },
      { text: 'Grammatikkindeks', link: '/no/themen' },
      { text: 'Ordliste', link: '/no/lektionen/wortliste' },
      { text: 'Glossar', link: '/no/lektionen/glossar' },
      { text: 'Leksjoner', collapsed: false, items: [] },
      { text: 'Skrift (Innledning)', collapsed: true, items: [] },
      { text: 'Oppgaver', collapsed: true, items: [] },
      { text: 'Juridisk', collapsed: true, items: [
          { text: 'Juridisk merknad & sitat', link: '/no/impressum' },
          { text: 'Bildelisenser', link: '/no/licenses' },
      ]}
    ],
    footer: {
      message: "Del av Tüpfli's Global Village Library",
      copyright: 'Opphavsrett © 2008-2010 Alois Payer'
    }
  }
}
