export const pt = {
  label: 'PT - Português',
  lang: 'pt-PT',
  link: '/pt/',
  title: 'Curso de Sânscrito',
  description: 'Livro de texto de Alois Payer',
  themeConfig: {
    outline: { level: [2, 3], label: 'Nesta página' },
    nav: [
      { text: 'Início', link: '/pt/' },
      { text: 'Índice', link: '/pt/lektionen/inhaltsverzeichnis' },
      { text: 'Perguntas e Respostas', link: '/qa_viewer.html', target: '_blank' },
      { text: 'Créditos', link: '/pt/impressum' },
      { text: '<span class="nav-gear-icon"></span>', link: '/pt/settings', ariaLabel: 'Abrir definições' }
    ],
    docFooter: {
      prev: 'Lição anterior',
      next: 'Próxima lição'
    },
    sidebar: [
      { text: 'Índice de conteúdos', link: '/pt/lektionen/inhaltsverzeichnis' },
      { text: 'Tópicos gramaticais', link: '/pt/grammatik' },
      { text: 'Índice gramatical', link: '/pt/themen' },
      { text: 'Vocabulário', link: '/pt/lektionen/wortliste' },
      { text: 'Glossário', link: '/pt/lektionen/glossar' },
      { text: 'Lições', collapsed: false, items: [] },
      { text: 'Escrita', collapsed: true, items: [] },
      { text: 'Exercícios', collapsed: true, items: [] },
      { text: 'Legal', collapsed: true, items: [
          { text: 'Aviso legal e citação', link: '/pt/impressum' },
          { text: 'Licenças de imagens', link: '/pt/licenses' },
      ]}
    ],
    footer: {
      message: 'Parte da Biblioteca da Aldeia Global de Tüpfli',
      copyright: 'Direitos de autor © 2008-2010 Alois Payer'
    }
  }
}
