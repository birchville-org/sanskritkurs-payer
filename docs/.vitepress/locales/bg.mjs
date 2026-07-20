
export const bg = {
  label: 'BG - Български',
  lang: 'bg-BG',
  link: '/bg/',
  title: 'Курс по санскрит',
  description: 'Граматичен учебник от Алоис Пайер',
  themeConfig: {
    outline: { level: [2, 3], label: 'На тази страница' },
    returnToTopLabel: 'Обратно към върха',
    sidebarMenuLabel: 'Меню',
    darkModeSwitchLabel: 'Изглед',
    lightModeSwitchTitle: 'Превключване към светла тема',
    darkModeSwitchTitle: 'Превключване към тъмна тема',
    langMenuLabel: 'Смяна на езика',
    nav: [
      { text: 'Начало', link: '/bg/' },
      { text: 'Съдържание', link: '/bg/lektionen/inhaltsverzeichnis' },
      { text: 'QA', link: '/qa_viewer.html', target: '_blank' },
      { text: 'Кредити', link: '/bg/impressum' },
      { text: '<span class="nav-gear-icon"></span>', link: '/bg/settings', ariaLabel: 'Отвори настройки' }
    ],
    docFooter: {
      prev: 'Предишен урок',
      next: 'Следващ урок'
    },
    sidebar: [
      { text: 'Съдържание', link: '/bg/lektionen/inhaltsverzeichnis' },
      { text: 'Граматически теми', link: '/bg/grammatik' },
            { text: 'Граматически индекс', link: '/bg/themen' },
      { text: 'Речник', link: '/bg/lektionen/wortliste' },
      { text: 'Речник', link: '/bg/lektionen/glossar' },
      { text: 'Уроци', collapsed: false, items: [] },
      { text: 'Писмо (Въведение)', collapsed: true, items: [] },
      { text: 'Упражнения', collapsed: true, items: [] },
      { text: 'Правни въпроси', collapsed: true, items: [
          { text: 'Импресуум и цитиране', link: '/bg/impressum' },
          { text: 'Лицензи на изображенията', link: '/bg/licenses' },
      ]}
    ],
    footer: {
      message: 'Част от Global Village Library на Tüpfli',
      copyright: 'Авторски права © 2008-2010 Алоис Пайер'
    }
  }
}
