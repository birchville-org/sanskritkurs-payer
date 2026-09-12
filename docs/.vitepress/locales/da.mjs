export const da = {
  label: '🇩🇰 DA - Dansk',
  lang: 'da-DK',
  link: '/da/',
  title: 'Sanskritkursus',
  description: 'Grammatikbog af Alois Payer',
  themeConfig: {
    outline: { level: [2, 3], label: 'På denne side' },
    returnToTopLabel: 'Tilbage til toppen',
    sidebarMenuLabel: 'Menu',
    darkModeSwitchLabel: 'Udseende',
    lightModeSwitchTitle: 'Skift til lyst tema',
    darkModeSwitchTitle: 'Skift til mørkt tema',
    langMenuLabel: 'Skift sprog',
    nav: [
      { text: 'Hjem', link: '/da/' },
      { text: 'Indholdsfortegnelse', link: '/da/lektionen/inhaltsverzeichnis' },
      { text: 'QA', link: '/qa_viewer.html', target: '_blank' },
      { text: 'Kolofon', link: '/da/impressum' },
      { text: '<span class="nav-gear-icon"></span>', link: '/da/settings', ariaLabel: 'Åbn indstillinger' }
    ],
    docFooter: {
      prev: 'Forrige lektion',
      next: 'Næste lektion'
    },
    sidebar: [
      { text: 'Indholdsfortegnelse', link: '/da/lektionen/inhaltsverzeichnis' },
      { text: 'Grammatiske emner', link: '/da/grammatik' },
      { text: 'Grammatikindeks', link: '/da/themen' },
      { text: 'Ordliste', link: '/da/lektionen/wortliste' },
      { text: 'Glossar', link: '/da/lektionen/glossar' },
      { text: 'Lektioner', collapsed: false, items: [] },
      { text: 'Skrift (Introduktion)', collapsed: true, items: [] },
      { text: 'Øvelser', collapsed: true, items: [] },
      { text: 'Juridisk', collapsed: true, items: [
          { text: 'Juridisk meddelelse & citat', link: '/da/impressum' },
          { text: 'Billedlicenser', link: '/da/licenses' },
      ]}
    ],
    footer: {
      message: "Del af Tüpfli's Global Village Library",
      copyright: 'Ophavsret © 2008-2010 Alois Payer'
    }
  }
}
