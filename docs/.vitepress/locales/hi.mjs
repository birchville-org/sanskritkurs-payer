
export const hi = {
  label: 'HI',
  lang: 'hi-IN',
  link: '/hi/',
  title: 'संस्कृत पाठ्यक्रम',
  description: 'आलोइस पायर द्वारा व्याकरण पाठ्यपुस्तक',
  themeConfig: {
    outline: { level: [2, 3], label: 'इस पृष्ठ पर' },
    returnToTopLabel: 'शीर्ष पर वापस जाएं',
    sidebarMenuLabel: 'मेनू',
    darkModeSwitchLabel: 'रूप-रंग',
    lightModeSwitchTitle: 'हल्के थीम पर जाएं',
    darkModeSwitchTitle: 'गहरे थीम पर जाएं',
    langMenuLabel: 'भाषा बदलें',
    nav: [
      { text: 'मुखपृष्ठ', link: '/hi/' },
      { text: 'विषय-सूची', link: '/hi/lektionen/inhaltsverzeichnis' },
      { text: 'अनुक्रमणिका', link: '/hi/grammatik' },
      { text: 'QA', link: '/qa_viewer.html', target: '_blank' },
      { text: 'श्रेय', link: '/hi/impressum' }
    ],
    docFooter: {
      prev: 'पिछला पाठ',
      next: 'अगला पाठ'
    },
    sidebar: [
      { text: 'विषय-सूची', link: '/hi/lektionen/inhaltsverzeichnis' },
      { text: 'व्याकरण विषय (अनुक्रमणिका)', link: '/hi/grammatik' },
      { text: 'शब्दावली', link: '/hi/lektionen/wortliste' },
      { text: 'शब्दकोश', link: '/hi/lektionen/glossar' },
      { text: 'पाठ', collapsed: false, items: [] },
      { text: 'लिपि (परिचय)', collapsed: true, items: [] },
      { text: 'अभ्यास', collapsed: true, items: [] },
      { text: 'कानूनी', collapsed: true, items: [
          { text: 'प्रकाशन विवरण एवं उद्धरण', link: '/hi/impressum' },
          { text: 'छवि लाइसेंस', link: '/hi/licenses' }
      ]}
    ],
    footer: {
      message: "Tüpfli's Global Village Library का हिस्सा",
      copyright: 'Copyright © 2008-2010 Alois Payer'
    }
  }
}
