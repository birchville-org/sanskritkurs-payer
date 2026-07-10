
export const la = {
  label: 'LA',
  lang: 'la',
  link: '/la/',
  title: 'Cursus Sanscriticus',
  description: 'Liber grammaticus ab Aloysio Payer compositus',
  themeConfig: {
    outline: { level: [2, 3], label: 'In hac pagina' },
    nav: [
      { text: 'Principium', link: '/la/' },
      { text: 'Index rerum', link: '/la/lektionen/inhaltsverzeichnis' },
      { text: 'QA', link: '/qa_viewer.html', target: '_blank' },
      { text: 'Laudes', link: '/la/impressum' },
      { text: '<span class="nav-gear-icon"></span>', link: '/la/settings', ariaLabel: 'Aperi Configurationes' }
    ],
    docFooter: {
      prev: 'Lectio prior',
      next: 'Lectio sequens'
    },
    sidebar: [
      { text: 'Index rerum', link: '/la/lektionen/inhaltsverzeichnis' },
      { text: 'Index grammaticus', link: '/la/grammatik' },
      { text: 'Glossarium', link: '/la/lektionen/wortliste' },
      { text: 'Lexicon', link: '/la/lektionen/glossar' },
      { text: 'Lectiones', collapsed: false, items: [] },
      { text: 'Scriptura', collapsed: true, items: [] },
      { text: 'Exercitationes', collapsed: true, items: [] },
      { text: 'Notitiae iuridicae', collapsed: true, items: [
          { text: 'Laudes et citatio', link: '/la/impressum' },
          { text: 'Licentiae imaginum', link: '/la/licenses' },
      ]}
    ],
    footer: {
      message: 'Pars Bibliothecae Globalis Vici Tüpfli',
      copyright: 'Ius auctoris © MMVIII–MMX Aloisius Payer'
    }
  }
}
