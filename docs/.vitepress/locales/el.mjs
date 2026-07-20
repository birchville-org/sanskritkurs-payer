
export const el = {
  label: 'EL - Ελληνικά',
  lang: 'el-GR',
  link: '/el/',
  title: 'Μάθημα Σανσκριτικής',
  description: 'Γραμματικό εγχειρίδιο του Alois Payer',
  themeConfig: {
    outline: { level: [2, 3], label: 'Σε αυτή τη σελίδα' },
    nav: [
      { text: 'Αρχική', link: '/el/' },
      { text: 'Πίνακας περιεχομένων', link: '/el/lektionen/inhaltsverzeichnis' },
      { text: 'Γραμματική', link: '/el/grammatik' },
      { text: 'QA', link: '/qa_viewer.html', target: '_blank' },
      { text: '<span class="nav-gear-icon"></span>', link: '/el/settings', ariaLabel: 'Settings' },
      { text: 'Πιστώσεις', link: '/el/impressum' }
    ],
    docFooter: {
      prev: 'Προηγούμενο μάθημα',
      next: 'Επόμενο μάθημα'
    },
    sidebar: [
      { text: 'Πίνακας περιεχομένων', link: '/el/lektionen/inhaltsverzeichnis' },
      { text: 'Γραμματικό ευρετήριο', link: '/el/grammatik' },
      { text: 'Λεξιλόγιο', link: '/el/lektionen/wortliste' },
      { text: 'Μαθήματα', collapsed: false, items: [] },
      { text: 'Γραφή', collapsed: true, items: [] },
      { text: 'Ασκήσεις', collapsed: true, items: [] },
      { text: 'Νομικές πληροφορίες', collapsed: true, items: [
          { text: 'Πιστώσεις και αναφορά', link: '/el/impressum' },
          { text: 'Άδειες εικόνων', link: '/el/licenses' }
      ]}
    ],
    footer: {
      message: 'Μέρος της Global Village Library του Tüpfli',
      copyright: 'Πνευματικά δικαιώματα © 2008-2010 Alois Payer'
    }
  }
}
