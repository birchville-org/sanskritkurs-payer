export const he = {
  label: 'HE - עברית',
  lang: 'he-IL',
  dir: 'rtl',
  link: '/he/',
  title: 'Sanskrit Course',
  description: 'Grammar textbook by Alois Payer',
  themeConfig: {
    outline: { level: [2, 3], label: 'בדף זה' },
    returnToTopLabel: 'חזרה למעלה',
    sidebarMenuLabel: 'תפריט',
    darkModeSwitchLabel: 'מראה',
    lightModeSwitchTitle: 'מעבר לערכת נושא בהירה',
    darkModeSwitchTitle: 'מעבר לערכת נושא כהה',
    langMenuLabel: 'שינוי שפה',
    nav: [
      { text: 'דף הבית', link: '/he/' },
      { text: 'תוכן עניינים', link: '/he/lektionen/inhaltsverzeichnis' },
      { text: 'שאלות ותשובות', link: '/qa_viewer.html', target: '_blank' },
      { text: 'אחריות', link: '/he/impressum' },
      { text: '<span class="nav-gear-icon"></span>', link: '/he/settings', ariaLabel: 'פתח הגדרות' }
    ],
    docFooter: {
      prev: 'שיעור קודם',
      next: 'שיעור הבא'
    },
    sidebar: [
      { text: 'תוכן עניינים', link: '/he/lektionen/inhaltsverzeichnis' },
      { text: 'נושאי דקדוק', link: '/he/grammatik' },
            { text: 'מפתח דקדוק', link: '/he/themen' },
      { text: 'אוצר מילים', link: '/he/lektionen/wortliste' },
      { text: 'לקסיקון', link: '/he/lektionen/glossar' },
      { text: 'שיעורים', collapsed: false, items: [] },
      { text: 'כתב (הקדמה)', collapsed: true, items: [] },
      { text: 'תרגילים', collapsed: true, items: [] },
      { text: 'משפטי', collapsed: true, items: [
          { text: 'הודעת אחריות וציטוט', link: '/he/impressum' },
          { text: 'רישיונות תמונה', link: '/he/licenses' },
      ]}
    ],
    footer: {
      message: "חלק מספריית הכפר הגלובלי של Tüpfli",
      copyright: 'זכויות יוצרים © 2008-2010 Alois Payer'
    }
  }
}
