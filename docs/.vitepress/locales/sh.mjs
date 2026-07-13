export const sh = {
  label: 'SH',
  lang: 'sh-BA',
  link: '/sh/',
  title: 'Sanskrit Kurs',
  description: 'Gramatički udžbenik Aloisa Payera',
  themeConfig: {
    outline: { level: [2, 3], label: 'Na ovoj stranici' },
    returnToTopLabel: 'Nazad na vrh',
    sidebarMenuLabel: 'Meni',
    darkModeSwitchLabel: 'Izgled',
    lightModeSwitchTitle: 'Prebaci na svijetlu temu',
    darkModeSwitchTitle: 'Prebaci na tamnu temu',
    langMenuLabel: 'Promijeni jezik',
    nav: [
      { text: 'Početna', link: '/sh/' },
      { text: 'Sadržaj', link: '/sh/lektionen/inhaltsverzeichnis' },
      { text: 'Pitanja', link: '/qa_viewer.html', target: '_blank' },
      { text: 'Zasluge', link: '/sh/impressum' },
      { text: '<span class="nav-gear-icon"></span>', link: '/sh/settings', ariaLabel: 'Otvori postavke' }
    ],
    docFooter: {
      prev: 'Prethodna lekcija',
      next: 'Sljedeća lekcija'
    },
    sidebar: [
      { text: 'Sadržaj', link: '/sh/lektionen/inhaltsverzeichnis' },
      { text: 'Gramatičke teme', link: '/sh/grammatik' },
            { text: 'Gramatički indeks', link: '/sh/themen' },
      { text: 'Rječnik', link: '/sh/lektionen/wortliste' },
      { text: 'Glosar', link: '/sh/lektionen/glossar' },
      { text: 'Lekcije', collapsed: false, items: [] },
      { text: 'Pismo (Uvod)', collapsed: true, items: [] },
      { text: 'Vježbe', collapsed: true, items: [] },
      { text: 'Pravne informacije', collapsed: true, items: [
          { text: 'Pravna napomena i citiranje', link: '/sh/impressum' },
          { text: 'Licence slika', link: '/sh/licenses' },
      ]}
    ],
    footer: {
      message: "Dio Tüpflijeve biblioteke globalnog sela",
      copyright: 'Autorska prava © 2008-2010 Alois Payer'
    }
  }
}
