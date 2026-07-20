export const fi = {
  label: 'FI - Suomi',
  lang: 'fi-FI',
  link: '/fi/',
  title: 'Sanskrit-kurssi',
  description: 'Sanskritin kieliopin oppikirja, laatinut Alois Payer',
  themeConfig: {
    outline: { level: [2, 3], label: 'Tällä sivulla' },
    returnToTopLabel: 'Palaa alkuun',
    sidebarMenuLabel: 'Valikko',
    darkModeSwitchLabel: 'Ulkoasu',
    lightModeSwitchTitle: 'Vaihda vaaleaan teemaan',
    darkModeSwitchTitle: 'Vaihda tummaan teemaan',
    langMenuLabel: 'Vaihda kieltä',
    nav: [
      { text: 'Koti', link: '/fi/' },
      { text: 'Sisällysluettelo', link: '/fi/lektionen/inhaltsverzeichnis' },
      { text: 'QA', link: '/qa_viewer.html', target: '_blank' },
      { text: 'Kiitokset', link: '/fi/impressum' },
      { text: '<span class="nav-gear-icon"></span>', link: '/fi/settings', ariaLabel: 'Asetukset' }
    ],
    docFooter: {
      prev: 'Edellinen oppitunti',
      next: 'Seuraava oppitunti'
    },
    sidebar: [
      { text: 'Sisällysluettelo', link: '/fi/lektionen/inhaltsverzeichnis' },
      { text: 'Kielioppiaiheet', link: '/fi/grammatik' },
      { text: 'Kieliopin hakemisto', link: '/fi/themen' },
      { text: 'Sanasto', link: '/fi/lektionen/wortliste' },
      { text: 'Sanakirja', link: '/fi/lektionen/glossar' },
      { text: 'Oppitunnit', collapsed: false, items: [] },
      { text: 'Kirjoitusjärjestelmä', collapsed: true, items: [] },
      { text: 'Harjoitukset', collapsed: true, items: [] },
      { text: 'Lakitiedot', collapsed: true, items: [
          { text: 'Julkaisutiedot & viittaukset', link: '/fi/impressum' },
          { text: 'Kuvien lisenssit', link: '/fi/licenses' },
      ]}
    ],
    footer: {
      message: "Osa Tüpflin Global Village -kirjastoa",
      copyright: 'Copyright © 2008-2010 Alois Payer'
    }
  }
}
