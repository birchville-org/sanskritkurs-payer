export const te = {
  label: '🇮🇳 TE - తెలుగు',
  lang: 'te-IN',
  link: '/te/',
  title: 'సంస్కృత పాఠ్యక్రమం',
  description: 'ఆలోయిస్ పాయర్ రచించిన వ్యాకరణ పాఠ్యపుస్తకం',
  themeConfig: {
    outline: { level: [2, 3], label: 'ఈ పేజీలో' },
    returnToTopLabel: 'పైకి వెళ్లండి',
    sidebarMenuLabel: 'మెనూ',
    darkModeSwitchLabel: 'రూపురేఖలు',
    lightModeSwitchTitle: 'లైట్ థీమ్‌కు మారండి',
    darkModeSwitchTitle: 'డార్క్ థీమ్‌కు మారండి',
    langMenuLabel: 'భాషను మార్చండి',
    nav: [
      { text: 'ముఖ్యాంశాలు', link: '/te/' },
      { text: 'విషయసూచిక', link: '/te/lektionen/inhaltsverzeichnis' },
      { text: 'QA', link: '/qa_viewer.html', target: '_blank' },
      { text: 'కృతజ్ఞతలు', link: '/te/impressum' },
      { text: '<span class="nav-gear-icon"></span>', link: '/te/settings', ariaLabel: 'సెట్టింగ్‌లను తెరవండి' }
    ],
    docFooter: {
      prev: 'మునుపటి పాఠం',
      next: 'తర్వాతి పాఠం'
    },
    sidebar: [
      { text: 'విషయసూచిక', link: '/te/lektionen/inhaltsverzeichnis' },
      { text: 'వ్యాకరణ అంశాలు', link: '/te/grammatik' },
      { text: 'వ్యాకరణ పట్టిక', link: '/te/themen' },
      { text: 'పదకోశం', link: '/te/lektionen/wortliste' },
      { text: 'శబ్దార్థ సంగ్రహం', link: '/te/lektionen/glossar' },
      { text: 'పాఠాలు', collapsed: false, items: [] },
      { text: 'లిపి (పరిచయం)', collapsed: true, items: [] },
      { text: 'అభ్యాసాలు', collapsed: true, items: [] },
      { text: 'చట్టపరమైన సమాచారం', collapsed: true, items: [
          { text: 'ప్రచురణ వివరాలు & ఉల్లేఖన', link: '/te/impressum' },
          { text: 'చిత్ర లైసెన్సులు', link: '/te/licenses' },
      ]}
    ],
    footer: {
      message: "Tüpfli's Global Village Library లో భాగం",
      copyright: 'Copyright © 2008-2010 Alois Payer'
    }
  }
}
