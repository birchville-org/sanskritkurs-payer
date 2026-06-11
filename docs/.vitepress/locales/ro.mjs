export const ro = {
  label: 'RO',
  lang: 'ro-RO',
  link: '/ro/',
  title: 'Curs de Sanscrită',
  description: 'Manual de gramatică de Alois Payer',
  themeConfig: {
    outline: { level: [2, 3], label: 'Pe această pagină' },
    returnToTopLabel: 'Înapoi sus',
    sidebarMenuLabel: 'Meniu',
    darkModeSwitchLabel: 'Aspect',
    lightModeSwitchTitle: 'Comutare la tema deschisă',
    darkModeSwitchTitle: 'Comutare la tema închisă',
    langMenuLabel: 'Schimbă limba',
    nav: [
      { text: 'Acasă', link: '/ro/' },
      { text: 'Cuprins', link: '/ro/lektionen/inhaltsverzeichnis' },
      { text: 'Index', link: '/ro/themen' },
      { text: 'QA', link: '/qa_viewer.html', target: '_blank' },
      { text: 'Credite', link: '/ro/impressum' }
    ],
    docFooter: {
      prev: 'Lecția anterioară',
      next: 'Lecția următoare'
    },
    sidebar: [
      { text: 'Cuprins', link: '/ro/lektionen/inhaltsverzeichnis' },
      { text: 'Index gramatical', link: '/ro/grammatik' },
      { text: 'Vocabular', link: '/ro/lektionen/wortliste' },
      { text: 'Glosar', link: '/ro/lektionen/glossar' },
      { text: 'Lecții', collapsed: false, items: [] },
      { text: 'Scriere (Introducere)', collapsed: true, items: [] },
      { text: 'Exerciții', collapsed: true, items: [] },
      { text: 'Informații juridice', collapsed: true, items: [
          { text: 'Impresium & citare', link: '/ro/impressum' },
          { text: 'Licențe imagini', link: '/ro/licenses' }
      ]}
    ],
    footer: {
      message: 'Parte din Global Village Library a lui Tüpfli',
      copyright: 'Copyright © 2008-2010 Alois Payer'
    }
  }
}
