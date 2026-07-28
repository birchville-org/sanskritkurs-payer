export const am = {
  label: '🇪🇹 AM - አማርኛ',
  lang: 'am-ET',
  link: '/am/',
  title: 'የሳንስክሪት ትምህርት',
  description: 'የሰዋሰው መጽሐፍ በአሎይስ ፓየር',
  themeConfig: {
    outline: { level: [2, 3], label: 'በዚህ ገጽ ላይ' },
    returnToTopLabel: 'ወደ ላይ ተመለስ',
    sidebarMenuLabel: 'ማውጫ',
    darkModeSwitchLabel: 'ገጽታ',
    lightModeSwitchTitle: 'ወደ ብሩህ ገጽታ ቀይር',
    darkModeSwitchTitle: 'ወደ ጨለማ ገጽታ ቀይር',
    langMenuLabel: 'ቋንቋ ቀይር',
    nav: [
      { text: 'መነሻ', link: '/am/' },
      { text: 'ማውጫ', link: '/am/lektionen/inhaltsverzeichnis' },
      { text: 'ጥያቄና መልስ', link: '/qa_viewer.html', target: '_blank' },
      { text: 'ክሬዲቶች', link: '/am/impressum' },
      { text: '<span class="nav-gear-icon"></span>', link: '/am/settings', ariaLabel: 'ቅንብሮችን ክፈት' }
    ],
    docFooter: {
      prev: 'ያለፈው ትምህርት',
      next: 'የሚቀጥለው ትምህርት'
    },
    sidebar: [
      { text: 'ማውጫ', link: '/am/lektionen/inhaltsverzeichnis' },
      { text: 'የሰዋሰው ርዕሶች', link: '/am/grammatik' },
      { text: 'የሰዋሰው ማውጫ', link: '/am/themen' },
      { text: 'የቃላት ዝርዝር', link: '/am/lektionen/wortliste' },
      { text: 'ቃላት መዝገብ', link: '/am/lektionen/glossar' },
      { text: 'ትምህርቶች', collapsed: false, items: [] },
      { text: 'ጽሕፈት (መግቢያ)', collapsed: true, items: [] },
      { text: 'መልመጃዎች', collapsed: true, items: [] },
      { text: 'ሕጋዊ', collapsed: true, items: [
          { text: 'ሕጋዊ ማስታወቂያ', link: '/am/impressum' },
          { text: 'የምስል ፈቃዶች', link: '/am/licenses' },
      ]}
    ],
    footer: {
      message: 'የTüpfli ዓለም አቀፍ ቤተ-መጽሐፍት አካል',
      copyright: 'የቅጂ መብት © 2008-2010 Alois Payer'
    }
  }
}
