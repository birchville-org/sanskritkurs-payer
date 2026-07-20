
export const grc = {
  label: 'GRC - Ἀρχαία',
  lang: 'grc',
  link: '/grc/',
  title: 'Σανσκριτικὸν Μάθημα',
  description: 'Γραμματικὸν βιβλίον ὑπὸ Ἀλοΐσου Πάιερ',
  themeConfig: {
    outline: { level: [2, 3], label: 'Ἐν τῇδε τῇ σελίδι' },
    nav: [
      { text: 'Ἀρχή', link: '/grc/' },
      { text: 'Πίναξ περιεχομένων', link: '/grc/lektionen/inhaltsverzeichnis' },
      { text: 'Γραμματική', link: '/grc/grammatik' },
      { text: 'QA', link: '/qa_viewer.html', target: '_blank' },
      { text: '<span class="nav-gear-icon"></span>', link: '/grc/settings', ariaLabel: 'Settings' },
      { text: 'Τιμαί', link: '/grc/impressum' }
    ],
    docFooter: {
      prev: 'Πρότερον μάθημα',
      next: 'Ὕστερον μάθημα'
    },
    sidebar: [
      { text: 'Πίναξ περιεχομένων', link: '/grc/lektionen/inhaltsverzeichnis' },
      { text: 'Εὑρετήριον γραμματικῆς', link: '/grc/grammatik' },
      { text: 'Γλωσσάριον', link: '/grc/lektionen/wortliste' },
      { text: 'Μαθήματα', collapsed: false, items: [] },
      { text: 'Γραφή', collapsed: true, items: [] },
      { text: 'Ἀσκήσεις', collapsed: true, items: [] },
      { text: 'Νομικαὶ πληροφορίαι', collapsed: true, items: [
          { text: 'Τιμαὶ καὶ παραπομπή', link: '/grc/impressum' },
          { text: 'Ἄδειαι εἰκόνων', link: '/grc/licenses' }
      ]}
    ],
    footer: {
      message: 'Μέρος τῆς Global Village Library τοῦ Tüpfli',
      copyright: 'Πνευματικὰ δικαιώματα © 2008-2010 Alois Payer'
    }
  }
}
