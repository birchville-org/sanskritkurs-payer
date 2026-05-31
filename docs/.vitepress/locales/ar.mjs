
export const ar = {
  label: 'AR',
  lang: 'ar',
  dir: 'rtl',
  link: '/ar/',
  title: 'دورة السنسكريتية',
  description: 'كتاب مدرسي من تأليف ألويس باير',
  themeConfig: {
    outline: { level: [2, 3], label: 'في هذه الصفحة' },
    nav: [
      { text: 'الرئيسية', link: '/ar/' },
      { text: 'فهرس المحتويات', link: '/ar/lektionen/inhaltsverzeichnis' },
      { text: 'النحو', link: '/ar/grammatik' },
      { text: 'QA', link: '/qa_viewer.html', target: '_blank' },
      { text: 'الاعتمادات', link: '/ar/impressum' }
    ],
    docFooter: {
      prev: 'الدرس السابق',
      next: 'الدرس التالي'
    },
    sidebar: [
      { text: 'فهرس المحتويات', link: '/ar/lektionen/inhaltsverzeichnis' },
      { text: 'دليل النحو', link: '/ar/grammatik' },
      { text: 'قائمة المفردات', link: '/ar/lektionen/wortliste' },
      { text: 'الدروس', collapsed: false, items: [] },
      { text: 'الكتابة', collapsed: true, items: [] },
      { text: 'التمارين', collapsed: true, items: [] },
      { text: 'المعلومات القانونية', collapsed: true, items: [
          { text: 'الاعتمادات', link: '/ar/impressum' },
          { text: 'تراخيص الصور', link: '/ar/licenses' }
      ]}
    ],
    footer: {
      message: 'جزء من مكتبة القرية العالمية لـ Tüpfli',
      copyright: 'حقوق النشر © 2008-2010 Alois Payer'
    }
  }
}
