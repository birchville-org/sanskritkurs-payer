
export const rm = {
  label: 'RM',
  lang: 'rm',
  link: '/rm/',
  title: 'Cors da sanskrit',
  description: 'Manual da grammatica dad Alois Payer',
  themeConfig: {
    returnToTopLabel: 'Enavos ensi',
    sidebarMenuLabel: 'Menu',
    darkModeSwitchLabel: 'Apparientscha',
    lightModeSwitchTitle: 'Midar al design cler',
    darkModeSwitchTitle: 'Midar al design stgir',
    langMenuLabel: 'Midar la lingua',
    outline: { level: [2, 3], label: 'Sin questa pagina' },
    nav: [
      { text: 'Pagina principala', link: '/rm/' },
      { text: 'Cuntegn', link: '/rm/lektionen/inhaltsverzeichnis' },
      { text: 'QA', link: '/qa_viewer.html', target: '_blank' },
      { text: 'Credits', link: '/rm/impressum' },
      { text: '⚙️', link: '/rm/settings', ariaLabel: 'Avrir parameters' }
    ],
    docFooter: {
      prev: 'Lecziun precedenta',
      next: 'Proxima lecziun'
    },
    sidebar: [
      { text: 'Cuntegn', link: '/rm/lektionen/inhaltsverzeichnis' },
      { text: 'Temas da grammatica', link: '/rm/grammatik' },
            { text: 'Index grammatical', link: '/rm/themen' },
      { text: 'Vocabulari', link: '/rm/lektionen/wortliste' },
      { text: 'Glossari', link: '/rm/lektionen/glossar' },
      { text: 'Lecziunas', collapsed: false, items: [] },
      { text: 'Scrittira (Introducziun)', collapsed: true, items: [] },
      { text: 'Exercizis', collapsed: true, items: [] },
      { text: 'Infurmaziuns giuridicas', collapsed: true, items: [
          { text: 'Impressum & citaziun', link: '/rm/impressum' },
          { text: "Licenzas d'immagins", link: '/rm/licenses' },
      ]}
    ],
    footer: {
      message: "Part da la Global Village Library da Tüpfli",
      copyright: 'Copyright © 2008-2010 Alois Payer'
    }
  }
}
