export const af = {
  label: 'AF - Afrikaans',
  lang: 'af-ZA',
  link: '/af/',
  title: 'Sanskrit-kurs',
  description: 'Grammatikaleerboek deur Alois Payer',
  themeConfig: {
    outline: { level: [2, 3], label: 'Op hierdie bladsy' },
    returnToTopLabel: 'Terug na bo',
    sidebarMenuLabel: 'Kieslys',
    darkModeSwitchLabel: 'Voorkoms',
    lightModeSwitchTitle: 'Skakel oor na ligte tema',
    darkModeSwitchTitle: 'Skakel oor na donker tema',
    langMenuLabel: 'Verander taal',
    nav: [
      { text: 'Tuis', link: '/af/' },
      { text: 'TOC', link: '/af/lektionen/inhaltsverzeichnis' },
      { text: 'V&A', link: '/qa_viewer.html', target: '_blank' },
      { text: 'Krediete', link: '/af/impressum' },
      { text: '<span class="nav-gear-icon"></span>', link: '/af/settings', ariaLabel: 'Maak Instellings oop' }
    ],
    docFooter: {
      prev: 'Vorige Lesing',
      next: 'Volgende Lesing'
    },
    sidebar: [
      { text: 'Inhoudsopgawe', link: '/af/lektionen/inhaltsverzeichnis' },
      { text: 'Grammatikateeme', link: '/af/grammatik' },
            { text: 'Grammatika-indeks', link: '/af/themen' },
      { text: 'Woordeskat', link: '/af/lektionen/wortliste' },
      { text: 'Glosarium', link: '/af/lektionen/glossar' },
      { text: 'Lesings', collapsed: false, items: [] },
      { text: 'Skrif (Inleiding)', collapsed: true, items: [] },
      { text: 'Oefeninge', collapsed: true, items: [] },
      { text: 'Regtelik', collapsed: true, items: [
          { text: 'Regtelike Kennisgewing & Sitasie', link: '/af/impressum' },
          { text: 'Beeldlisensies', link: '/af/licenses' },
      ]}
    ],
    footer: {
      message: "Deel van Tüpfli se Globale Dorpsbiblioteek",
      copyright: 'Kopiereg © 2008-2010 Alois Payer'
    }
  }
}
