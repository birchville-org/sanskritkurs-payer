
export const akk = {
  label: 'AKK',
  lang: 'akk',
  link: '/akk/',
  title: 'Ṭupšarrūtu ša Sanskriti',
  description: 'Ṭuppu ša lišāni ša Aloisī Pāyeri',
  themeConfig: {
    outline: { level: [2, 3], label: 'Ina ṭuppi annî' },
    nav: [
      { text: 'Rēštu', link: '/akk/' },
      { text: 'Qibītu ša ṭuppī', link: '/akk/lektionen/inhaltsverzeichnis' },
      { text: 'Grammaṭu', link: '/akk/grammatik' },
      { text: 'QA', link: '/qa_viewer.html', target: '_blank' },
      { text: '<span class="nav-gear-icon"></span>', link: '/akk/settings', ariaLabel: 'Settings' },
      { text: 'Tâmartum', link: '/akk/impressum' }
    ],
    docFooter: {
      prev: 'Ṭupšarru pānûm',
      next: 'Ṭupšarru arkûm'
    },
    sidebar: [
      { text: 'Qibītu ša ṭuppī', link: '/akk/lektionen/inhaltsverzeichnis' },
      { text: 'Grammaṭu', link: '/akk/grammatik' },
      { text: 'Qibīt awātī', link: '/akk/lektionen/wortliste' },
      { text: 'Ṭupšarrūtu', collapsed: false, items: [] },
      { text: 'Šiṭru', collapsed: true, items: [] },
      { text: 'Birkū', collapsed: true, items: [] },
      { text: 'Šimātu ša dīnim', collapsed: true, items: [
          { text: 'Tâmartum u zakārum', link: '/akk/impressum' },
          { text: 'Lišānāt ṣalmī', link: '/akk/licenses' }
      ]}
    ],
    footer: {
      message: 'Zittu ša Global Village Library ša Tüpfli',
      copyright: 'Bēl šarrūti © 2008-2010 Alois Payer'
    }
  }
}
