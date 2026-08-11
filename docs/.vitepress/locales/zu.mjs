export const zu = {
  label: '🇿🇦 ZU - isiZulu',
  lang: 'zu-ZA',
  title: 'Isifundo seSanskrit',
  description: 'Incwadi yeLulwimi lweLulwimi nguAlois Payer',
  themeConfig: {
    outline: { level: [2, 3], label: 'Kule khasi' },
    returnToTopLabel: 'Buyela phezulu',
    sidebarMenuLabel: 'Imenyu',
    darkModeSwitchLabel: 'Ukwenzeka',
    lightModeSwitchTitle: 'Shintshela kuklanywa okukhanyayo',
    darkModeSwitchTitle: 'Shintshela kuklanywa okumnyama',
    langMenuLabel: 'Shintsha ulimi',
    nav: [
      { text: 'Ikhasi elikhulu', link: '/zu/' },
      { text: 'Okuqukethwe', link: '/zu/lektionen/inhaltsverzeichnis' },
      { text: 'Imithetho', link: '/zu/impressum' },
      { text: '<span class="nav-gear-icon"></span>', link: '/zu/settings', ariaLabel: 'Vula izilungiselelo' }
    ],
    docFooter: {
      prev: 'Isifundo esedlule',
      next: 'Isifundo esilandelayo'
    },
    sidebar: [
      { text: 'Okuqukethwe', link: '/zu/lektionen/inhaltsverzeichnis' },
      { text: 'Izihloko zohlelo lolimi', link: '/zu/grammatik' },
      { text: 'Inkomba yohlelo lolimi', link: '/zu/themen' },
      { text: 'Uhlu lwamagama', link: '/zu/lektionen/wortliste' },
      { text: 'Incazelo yamagama', link: '/zu/lektionen/glossar' },
      { text: 'Izifundo', collapsed: false, items: [] },
      { text: 'Ukubhala (Isingeniso)', collapsed: true, items: [] },
      { text: 'Ukuzivocavoca', collapsed: true, items: [] },
      { text: 'Imithetho', collapsed: true, items: [
          { text: 'Imithetho necaphuna', link: '/zu/impressum' },
          { text: 'Izincwadi zezithombe', link: '/zu/licenses' },
      ]}
    ],
    footer: {
      message: "Teil der Tüpfli's Global Village Library",
      copyright: 'Copyright © 2008-2010 Alois Payer'
    }
  }
}
