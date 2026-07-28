export const sq = {
  label: '🇦🇱 SQ - Shqip',
  lang: 'sq-AL',
  link: '/sq/',
  title: 'Kurs Sanskritisht',
  description: 'Tekst shkollore gramatike nga Alois Payer',
  themeConfig: {
    outline: { level: [2, 3], label: 'Në këtë faqe' },
    returnToTopLabel: 'Kthehu në krye',
    sidebarMenuLabel: 'Menyja',
    darkModeSwitchLabel: 'Pamja',
    lightModeSwitchTitle: 'Ndrysho në temë të ndritshme',
    darkModeSwitchTitle: 'Ndrysho në temë të errët',
    langMenuLabel: 'Ndrysho gjuhën',
    nav: [
      { text: 'Kryefaqja', link: '/sq/' },
      { text: 'TOC', link: '/sq/lektionen/inhaltsverzeichnis' },
      { text: 'Pyetje & Përgjigje', link: '/qa_viewer.html', target: '_blank' },
      { text: 'Falënderime', link: '/sq/impressum' },
      { text: '<span class="nav-gear-icon"></span>', link: '/sq/settings', ariaLabel: 'Hap Cilësimet' }
    ],
    docFooter: {
      prev: 'Mësimi i mëparshëm',
      next: 'Mësimi i ardhshëm'
    },
    sidebar: [
      { text: 'Përmbajtja', link: '/sq/lektionen/inhaltsverzeichnis' },
      { text: 'Temat e Gramatikës', link: '/sq/grammatik' },
            { text: 'Indeksi i Gramatikës', link: '/sq/themen' },
      { text: 'Fjalor', link: '/sq/lektionen/wortliste' },
      { text: 'Glosar', link: '/sq/lektionen/glossar' },
      { text: 'Mësimet', collapsed: false, items: [] },
      { text: 'Shkrimi (Hyrje)', collapsed: true, items: [] },
      { text: 'Ushtrime', collapsed: true, items: [] },
      { text: 'Juridik', collapsed: true, items: [
          { text: 'Njoftim Juridik & Citim', link: '/sq/impressum' },
          { text: 'Licencat e Imazheve', link: '/sq/licenses' },
      ]}
    ],
    footer: {
      message: "Pjesë e Bibliotekës së Fshatit Global të Tüpfli",
      copyright: 'Të drejtat e autorit © 2008-2010 Alois Payer'
    }
  }
}
