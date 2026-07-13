export const lt = {
  label: 'LT',
  lang: 'lt-LT',
  link: '/lt/',
  title: 'Sanskrito kursas',
  description: 'Aloiso Payerio gramatikos vadovėlis',
  themeConfig: {
    outline: { level: [2, 3], label: 'Šiame puslapyje' },
    returnToTopLabel: 'Grįžti į viršų',
    sidebarMenuLabel: 'Meniu',
    darkModeSwitchLabel: 'Išvaizda',
    lightModeSwitchTitle: 'Perjungti į šviesią temą',
    darkModeSwitchTitle: 'Perjungti į tamsią temą',
    langMenuLabel: 'Keisti kalbą',
    nav: [
      { text: 'Pradžia', link: '/lt/' },
      { text: 'Turinys', link: '/lt/lektionen/inhaltsverzeichnis' },
      { text: 'DU', link: '/qa_viewer.html', target: '_blank' },
      { text: 'Ačiū', link: '/lt/impressum' },
      { text: '<span class="nav-gear-icon"></span>', link: '/lt/settings', ariaLabel: 'Atidaryti nustatymus' }
    ],
    docFooter: {
      prev: 'Ankstesnė pamoka',
      next: 'Kita pamoka'
    },
    sidebar: [
      { text: 'Turinys', link: '/lt/lektionen/inhaltsverzeichnis' },
      { text: 'Gramatikos temos', link: '/lt/grammatik' },
            { text: 'Gramatikos rodyklė', link: '/lt/themen' },
      { text: 'Žodynas', link: '/lt/lektionen/wortliste' },
      { text: 'Glosarijus', link: '/lt/lektionen/glossar' },
      { text: 'Pamokos', collapsed: false, items: [] },
      { text: 'Raštas (Įvadas)', collapsed: true, items: [] },
      { text: 'Užduotys', collapsed: true, items: [] },
      { text: 'Teisinė informacija', collapsed: true, items: [
          { text: 'Teisinis pranešimas ir citavimas', link: '/lt/impressum' },
          { text: 'Nuotraukų licencijos', link: '/lt/licenses' },
      ]}
    ],
    footer: {
      message: "Dalies Tüpfli Globaliosios kaimo bibliotekos",
      copyright: 'Autorinės teisės © 2008-2010 Alois Payer'
    }
  }
}
