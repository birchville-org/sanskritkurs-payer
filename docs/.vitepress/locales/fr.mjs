
export const fr = {
  label: 'FR',
  lang: 'fr-FR',
  link: '/fr/',
  title: 'Cours de sanskrit',
  description: 'Manuel de grammaire par Alois Payer',
  themeConfig: {
    outline: { level: [2, 3], label: 'Sur cette page' },
    returnToTopLabel: 'Retour en haut',
    sidebarMenuLabel: 'Menu',
    darkModeSwitchLabel: 'Apparence',
    lightModeSwitchTitle: 'Passer au thème clair',
    darkModeSwitchTitle: 'Passer au thème sombre',
    langMenuLabel: 'Changer de langue',
    nav: [
      { text: 'Accueil', link: '/fr/' },
      { text: 'Table des matières', link: '/fr/lektionen/inhaltsverzeichnis' },
      { text: 'Index', link: '/fr/grammatik' },
      { text: 'QA', link: '/qa_viewer.html', target: '_blank' },
      { text: 'Crédits', link: '/fr/impressum' }
    ],
    docFooter: {
      prev: 'Leçon précédente',
      next: 'Leçon suivante'
    },
    sidebar: [
      { text: 'Table des matières', link: '/fr/lektionen/inhaltsverzeichnis' },
      { text: 'Sujets de grammaire (Index)', link: '/fr/grammatik' },
      { text: 'Vocabulaire', link: '/fr/lektionen/wortliste' },
      { text: 'Leçons', collapsed: false, items: [] },
      { text: 'Écriture (Introduction)', collapsed: true, items: [] },
      { text: 'Exercices', collapsed: true, items: [] },
      { text: 'Mentions légales', collapsed: true, items: [
          { text: 'Notice légale & citation', link: '/fr/impressum' },
          { text: "Licences d'images", link: '/fr/licenses' }
      ]}
    ],
    footer: {
      message: "Partie de la Bibliothèque globale du village de Tüpfli",
      copyright: 'Copyright © 2008-2010 Alois Payer'
    }
  }
}
