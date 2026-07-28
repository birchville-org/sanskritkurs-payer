
export const fa = {
  label: '🇮🇷 FA - فارسی',
  lang: 'fa',
  dir: 'rtl',
  link: '/fa/',
  title: 'دوره سانسکریت',
  description: 'کتاب درسی دستور زبان اثر آلوئیس پایر',
  themeConfig: {
    outline: { level: [2, 3], label: 'در این صفحه' },
    nav: [
      { text: 'خانه', link: '/fa/' },
      { text: 'فهرست مطالب', link: '/fa/lektionen/inhaltsverzeichnis' },
      { text: 'دستور زبان', link: '/fa/grammatik' },
      { text: 'QA', link: '/qa_viewer.html', target: '_blank' },
      { text: '<span class="nav-gear-icon"></span>', link: '/fa/settings', ariaLabel: 'Settings' },
      { text: 'اعتبارات', link: '/fa/impressum' }
    ],
    docFooter: {
      prev: 'درس قبلی',
      next: 'درس بعدی'
    },
    sidebar: [
      { text: 'فهرست مطالب', link: '/fa/lektionen/inhaltsverzeichnis' },
      { text: 'نمایه دستور زبان', link: '/fa/grammatik' },
      { text: 'فهرست واژگان', link: '/fa/lektionen/wortliste' },
      { text: 'درس‌ها', collapsed: false, items: [] },
      { text: 'خط', collapsed: true, items: [] },
      { text: 'تمرین‌ها', collapsed: true, items: [] },
      { text: 'اطلاعات حقوقی', collapsed: true, items: [
          { text: 'اعتبارات و استناد', link: '/fa/impressum' },
          { text: 'مجوزهای تصویر', link: '/fa/licenses' }
      ]}
    ],
    footer: {
      message: 'بخشی از کتابخانه دهکده جهانی Tüpfli',
      copyright: 'حق نشر © ۲۰۰۸-۲۰۱۰ Alois Payer'
    }
  }
}
