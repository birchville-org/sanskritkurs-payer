
export const bg = {
  label: 'BG',
  lang: 'bg-BG',
  link: '/bg/',
  title: 'Курс по санскрит',
  description: 'Граматичен учебник от Алоис Пайер',
  themeConfig: {
    outline: { level: [2, 3], label: 'На тази страница' },
    nav: [
      { text: 'Начало', link: '/bg/' },
      { text: 'Съдържание', link: '/bg/lektionen/inhaltsverzeichnis' },
      { text: 'Индекс', link: '/bg/grammatik' },
      { text: 'QA', link: '/qa/viewer' },
      { text: 'QA', link: '/qa_viewer.html', target: '_blank' },
      { text: 'Кредити', link: '/bg/impressum' }
    ],
    docFooter: {
      prev: 'Предишен урок',
      next: 'Следващ урок'
    },
    sidebar: [
      { text: 'Съдържание', link: '/bg/lektionen/inhaltsverzeichnis' },
      { text: 'Граматични теми (Индекс)', link: '/bg/grammatik' },
      { text: 'Речник', link: '/bg/lektionen/wortliste' },
      { text: 'Уроци', collapsed: false, items: [] },
      { text: 'Писмо (Въведение)', collapsed: true, items: [] },
      { text: 'Упражнения', collapsed: true, items: [] },
      { text: 'Правни въпроси', collapsed: true, items: [
          { text: 'Импресуум и цитиране', link: '/bg/impressum' },
          { text: 'Лицензи на изображенията', link: '/bg/licenses' }
      ]}
    ],
    footer: {
      message: 'Част от Global Village Library на Tüpfli',
      copyright: 'Авторски права © 2008-2010 Алоис Пайер'
    }
  }
}
