export const is = {
  label: '🇮🇸 IS - Íslenska',
  lang: 'is-IS',
  link: '/is/',
  title: 'Sanskritnámskeið',
  description: 'Málfræðikver eftir Alois Payer',
  themeConfig: {
    outline: { level: [2, 3], label: 'Á þessari síðu' },
    returnToTopLabel: 'Aftur efst',
    sidebarMenuLabel: 'Valmynd',
    darkModeSwitchLabel: 'Útlit',
    lightModeSwitchTitle: 'Skipta yfir í ljóst þema',
    darkModeSwitchTitle: 'Skipta yfir í dökkt þema',
    langMenuLabel: 'Breyta tungumáli',
    nav: [
      { text: 'Forsíða', link: '/is/' },
      { text: 'Efnisyfirlit', link: '/is/lektionen/inhaltsverzeichnis' },
      { text: 'QA', link: '/qa_viewer.html', target: '_blank' },
      { text: 'Ritstjórn', link: '/is/impressum' },
      { text: '<span class="nav-gear-icon"></span>', link: '/is/settings', ariaLabel: 'Opna stillingar' }
    ],
    docFooter: {
      prev: 'Fyrri kennslustund',
      next: 'Næsta kennslustund'
    },
    sidebar: [
      { text: 'Efnisyfirlit', link: '/is/lektionen/inhaltsverzeichnis' },
      { text: 'Málfræðiefni', link: '/is/grammatik' },
      { text: 'Málfræðiyfirlit', link: '/is/themen' },
      { text: 'Orðalisti', link: '/is/lektionen/wortliste' },
      { text: 'Orðskýringar', link: '/is/lektionen/glossar' },
      { text: 'Kennslustundir', collapsed: false, items: [] },
      { text: 'Skrift (Inngangur)', collapsed: true, items: [] },
      { text: 'Æfingar', collapsed: true, items: [] },
      { text: 'Lögfræðilegt', collapsed: true, items: [
          { text: 'Lögfræðileg fyrirvari & tilvitnun', link: '/is/impressum' },
          { text: 'Myndaleyfi', link: '/is/licenses' },
      ]}
    ],
    footer: {
      message: "Hluti af Tüpfli's Global Village Library",
      copyright: 'Höfundarréttur © 2008-2010 Alois Payer'
    }
  }
}
