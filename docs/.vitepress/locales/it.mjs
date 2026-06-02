
export const it = {
  label: 'IT',
  lang: 'it-IT',
  link: '/it/',
  title: 'Corso di Sanscrito',
  description: 'Libro di testo di Alois Payer',
  themeConfig: {
    outline: { level: [2, 3], label: 'In questa pagina' },
    returnToTopLabel: 'Torna su',
    sidebarMenuLabel: 'Menu',
    darkModeSwitchLabel: 'Aspetto',
    lightModeSwitchTitle: 'Passa al tema chiaro',
    darkModeSwitchTitle: 'Passa al tema scuro',
    langMenuLabel: 'Cambia lingua',
    nav: [
      { text: 'Home', link: '/it/' },
      { text: 'Sommario', link: '/it/lektionen/inhaltsverzeichnis' },
      { text: 'Indice', link: '/it/grammatik' },
      { text: 'QA', link: '/qa_viewer.html', target: '_blank' },
      { text: 'Crediti', link: '/it/impressum' }
    ],
    docFooter: {
      prev: 'Lezione precedente',
      next: 'Lezione successiva'
    },
    sidebar: [
      { text: 'Sommario', link: '/it/lektionen/inhaltsverzeichnis' },
      { text: 'Indice Grammaticale', link: '/it/grammatik' },
      { text: 'Vocabolario', link: '/it/lektionen/wortliste' },
      { text: 'Glossario', link: '/it/lektionen/glossar' },
      { text: 'Lezioni', collapsed: false, items: [] },
      { text: 'Scrittura', collapsed: true, items: [] },
      { text: 'Esercizi', collapsed: true, items: [] },
      { text: 'Note legali', collapsed: true, items: [
          { text: 'Crediti e citazione', link: '/it/impressum' },
          { text: 'Licenze immagini', link: '/it/licenses' }
      ]}
    ],
    footer: {
      message: "Parte della Global Village Library di Tüpfli",
      copyright: 'Copyright © 2008-2010 Alois Payer'
    }
  }
}
