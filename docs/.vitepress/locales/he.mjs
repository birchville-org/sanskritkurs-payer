
export const he = {
  label: 'HE',
  lang: 'he',
  dir: 'rtl',
  link: '/he/',
  title: 'קורס סנסקריט',
  description: 'ספר לימוד מאת אלויס פאייר',
  themeConfig: {
    outline: { level: [2, 3], label: 'בדף זה' },
    nav: [
      { text: 'דף הבית', link: '/he/' },
      { text: 'תוכן עניינים', link: '/he/lektionen/inhaltsverzeichnis' },
      { text: 'דקדוק', link: '/he/grammatik' },
      { text: 'QA', link: '/qa_viewer.html', target: '_blank' },
      { text: 'קרדיטים', link: '/he/impressum' }
    ],
    docFooter: {
      prev: 'השיעור הקודם',
      next: 'השיעור הבא'
    },
    sidebar: [
      { text: 'תוכן עניינים', link: '/he/lektionen/inhaltsverzeichnis' },
      { text: 'מפתח דקדוקי', link: '/he/grammatik' },
      { text: 'רשימת מילים', link: '/he/lektionen/wortliste' },
      { text: 'שיעורים', collapsed: false, items: [] },
      { text: 'כתב', collapsed: true, items: [] },
      { text: 'תרגילים', collapsed: true, items: [] },
      { text: 'מידע משפטי', collapsed: true, items: [
          { text: 'קרדיטים וציטוט', link: '/he/impressum' },
          { text: 'רישיונות תמונות', link: '/he/licenses' }
      ]}
    ],
    footer: {
      message: 'חלק מ-Global Village Library של Tüpfli',
      copyright: 'זכויות יוצרים © 2008-2010 Alois Payer'
    }
  }
}
