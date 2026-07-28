export const nl = {
  label: '🇳🇱 NL - Nederlands',
  lang: 'nl-NL',
  link: '/nl/',
  title: 'Sanskritcursus',
  description: 'Grammatica-leerboek van Alois Payer',
  themeConfig: {
    outline: { level: [2, 3], label: 'Op deze pagina' },
    returnToTopLabel: 'Terug naar boven',
    sidebarMenuLabel: 'Menu',
    darkModeSwitchLabel: 'Weergave',
    lightModeSwitchTitle: 'Schakelen naar licht thema',
    darkModeSwitchTitle: 'Schakelen naar donker thema',
    langMenuLabel: 'Taal wijzigen',
    nav: [
      { text: 'Home', link: '/nl/' },
      { text: 'Inhoudsopgave', link: '/nl/lektionen/inhaltsverzeichnis' },
      { text: 'QA', link: '/qa_viewer.html', target: '_blank' },
      { text: 'Credits', link: '/nl/impressum' },
      { text: '<span class="nav-gear-icon"></span>', link: '/nl/settings', ariaLabel: 'Instellingen openen' }
    ],
    docFooter: {
      prev: 'Vorige les',
      next: 'Volgende les'
    },
    sidebar: [
      { text: 'Inhoudsopgave', link: '/nl/lektionen/inhaltsverzeichnis' },
      { text: 'Grammaticathema\'s', link: '/nl/grammatik' },
            { text: 'Grammaticaindex', link: '/nl/themen' },
      { text: 'Woordenlijst', link: '/nl/lektionen/wortliste' },
      { text: 'Glossarium', link: '/nl/lektionen/glossar' },
      { text: 'Lessen', collapsed: false, items: [] },
      { text: 'Schrift (Inleiding)', collapsed: true, items: [] },
      { text: 'Oefeningen', collapsed: true, items: [] },
      { text: 'Juridisch', collapsed: true, items: [
          { text: 'Juridische verklaring & bronvermelding', link: '/nl/impressum' },
          { text: 'Afbeeldingslicenties', link: '/nl/licenses' },
      ]}
    ],
    footer: {
      message: "Een deel van de Bibliotheek van Tüpfli's Global Village",
      copyright: 'Copyright © 2008-2010 Alois Payer'
    }
  }
}
