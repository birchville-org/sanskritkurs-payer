export const sv = {
  label: '🇸🇪 SV - Svenska',
  lang: 'sv-SE',
  link: '/sv/',
  title: 'Sanskritkurs',
  description: 'Lärobok i sanskrit av Alois Payer',
  themeConfig: {
    outline: { level: [2, 3], label: 'På denna sida' },
    returnToTopLabel: 'Tillbaka till toppen',
    sidebarMenuLabel: 'Meny',
    darkModeSwitchLabel: 'Utseende',
    lightModeSwitchTitle: 'Växla till ljust tema',
    darkModeSwitchTitle: 'Växla till mörkt tema',
    langMenuLabel: 'Byt språk',
    nav: [
      { text: 'Hem', link: '/sv/' },
      { text: 'Innehållsförteckning', link: '/sv/lektionen/inhaltsverzeichnis' },
      { text: 'QA', link: '/qa_viewer.html', target: '_blank' },
      { text: 'Kolofon', link: '/sv/impressum' },
      { text: '<span class="nav-gear-icon"></span>', link: '/sv/settings', ariaLabel: 'Öppna inställningar' }
    ],
    docFooter: {
      prev: 'Föregående lektion',
      next: 'Nästa lektion'
    },
    sidebar: [
      { text: 'Innehållsförteckning', link: '/sv/lektionen/inhaltsverzeichnis' },
      { text: 'Grammatikämnen', link: '/sv/grammatik' },
      { text: 'Grammatikindex', link: '/sv/themen' },
      { text: 'Ordlista', link: '/sv/lektionen/wortliste' },
      { text: 'Glossar', link: '/sv/lektionen/glossar' },
      { text: 'Lektioner', collapsed: false, items: [] },
      { text: 'Skrift (Introduktion)', collapsed: true, items: [] },
      { text: 'Övningar', collapsed: true, items: [] },
      { text: 'Juridiskt', collapsed: true, items: [
          { text: 'Juridiskt meddelande & citat', link: '/sv/impressum' },
          { text: 'Bildlicenser', link: '/sv/licenses' },
      ]}
    ],
    footer: {
      message: "Del av Tüpfli's Global Village Library",
      copyright: 'Upphovsrätt © 2008-2010 Alois Payer'
    }
  }
}
