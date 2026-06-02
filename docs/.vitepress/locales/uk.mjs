
export const uk = {
  label: 'UK',
  lang: 'uk-UA',
  link: '/uk/',
  title: 'Курс санскриту',
  description: 'Підручник граматики Алоїза Пайєра',
  themeConfig: {
    outline: { level: [2, 3], label: 'На цій сторінці' },
    returnToTopLabel: 'Повернутися вгору',
    sidebarMenuLabel: 'Меню',
    darkModeSwitchLabel: 'Вигляд',
    lightModeSwitchTitle: 'Перейти на світлу тему',
    darkModeSwitchTitle: 'Перейти на темну тему',
    langMenuLabel: 'Змінити мову',
    nav: [
      { text: 'Головна', link: '/uk/' },
      { text: 'Зміст', link: '/uk/lektionen/inhaltsverzeichnis' },
      { text: 'Покажчик', link: '/uk/grammatik' },
      { text: 'QA', link: '/qa_viewer.html', target: '_blank' },
      { text: 'Автори', link: '/uk/impressum' }
    ],
    docFooter: {
      prev: 'Попередня лекція',
      next: 'Наступна лекція'
    },
    sidebar: [
      { text: 'Зміст', link: '/uk/lektionen/inhaltsverzeichnis' },
      { text: 'Граматичні теми (Покажчик)', link: '/uk/grammatik' },
      { text: 'Словник', link: '/uk/lektionen/wortliste' },
      { text: 'Глосарій', link: '/uk/lektionen/glossar' },
      { text: 'Лекції', collapsed: false, items: [] },
      { text: 'Письмо (Вступ)', collapsed: true, items: [] },
      { text: 'Вправи', collapsed: true, items: [] },
      { text: 'Правова інформація', collapsed: true, items: [
          { text: 'Вихідні дані та цитування', link: '/uk/impressum' },
          { text: 'Ліцензії на зображення', link: '/uk/licenses' }
      ]}
    ],
    footer: {
      message: 'Частина Global Village Library Тюпфлі',
      copyright: 'Copyright © 2008-2010 Алоїз Пайєр'
    }
  }
}
