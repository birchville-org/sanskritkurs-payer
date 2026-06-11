
export const es = {
  label: 'ES',
  lang: 'es-ES',
  link: '/es/',
  title: 'Curso de Sánscrito',
  description: 'Libro de texto de Alois Payer',
  themeConfig: {
    outline: { level: [2, 3], label: 'En esta página' },
    nav: [
      { text: 'Inicio', link: '/es/' },
      { text: 'Contenido', link: '/es/lektionen/inhaltsverzeichnis' },
      { text: 'Índice', link: '/es/themen' },
      { text: 'QA', link: '/qa_viewer.html', target: '_blank' },
      { text: 'Créditos', link: '/es/impressum' }
    ],
    docFooter: {
      prev: 'Lección anterior',
      next: 'Próxima lección'
    },
    sidebar: [
      { text: 'Tabla de contenidos', link: '/es/lektionen/inhaltsverzeichnis' },
      { text: 'Índice gramatical', link: '/es/grammatik' },
      { text: 'Vocabulario', link: '/es/lektionen/wortliste' },
      { text: 'Glosario', link: '/es/lektionen/glossar' },
      { text: 'Lecciones', collapsed: false, items: [] },
      { text: 'Escritura', collapsed: true, items: [] },
      { text: 'Ejercicios', collapsed: true, items: [] },
      { text: 'Legal', collapsed: true, items: [
          { text: 'Aviso legal y citación', link: '/es/impressum' },
          { text: 'Licencias de imágenes', link: '/es/licenses' }
      ]}
    ],
    footer: {
      message: 'Parte de la Global Village Library de Tüpfli',
      copyright: 'Copyright © 2008-2010 Alois Payer'
    }
  }
}
