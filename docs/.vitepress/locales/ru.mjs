
export const ru = {
  label: 'RU',
  lang: 'ru-RU',
  link: '/ru/',
  title: 'Курс санскрита',
  description: 'Учебник грамматики Алоиза Пайера',
  themeConfig: {
    outline: { level: [2, 3], label: 'На этой странице' },
    returnToTopLabel: 'Вернуться наверх',
    sidebarMenuLabel: 'Меню',
    darkModeSwitchLabel: 'Оформление',
    lightModeSwitchTitle: 'Переключить на светлую тему',
    darkModeSwitchTitle: 'Переключить на тёмную тему',
    langMenuLabel: 'Сменить язык',
    nav: [
      { text: 'Главная', link: '/ru/' },
      { text: 'Содержание', link: '/ru/lektionen/inhaltsverzeichnis' },
      { text: 'Указатель', link: '/ru/grammatik' },
      { text: 'QA', link: '/qa_viewer.html', target: '_blank' },
      { text: 'Авторы', link: '/ru/impressum' }
    ],
    docFooter: {
      prev: 'Предыдущая лекция',
      next: 'Следующая лекция'
    },
    sidebar: [
      { text: 'Содержание', link: '/ru/lektionen/inhaltsverzeichnis' },
      { text: 'Грамматические темы (Указатель)', link: '/ru/grammatik' },
      { text: 'Словарь', link: '/ru/lektionen/wortliste' },
      { text: 'Лекции', collapsed: false, items: [] },
      { text: 'Письмо (Вступление)', collapsed: true, items: [] },
      { text: 'Упражнения', collapsed: true, items: [] },
      { text: 'Правовая информация', collapsed: true, items: [
          { text: 'Выходные данные и цитирование', link: '/ru/impressum' },
          { text: 'Лицензии на изображения', link: '/ru/licenses' }
      ]}
    ],
    footer: {
      message: 'Часть Global Village Library Тюпфли',
      copyright: 'Copyright © 2008-2010 Алоиз Пайер'
    }
  }
}
