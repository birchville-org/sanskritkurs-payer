
export const zh = {
  label: 'ZH - 中文',
  lang: 'zh-Hans',
  link: '/zh/',
  title: '梵语课程',
  description: '阿洛伊斯·帕耶尔的语法教材',
  themeConfig: {
    outline: { level: [2, 3], label: '本页内容' },
    nav: [
      { text: '首页', link: '/zh/' },
      { text: '目录', link: '/zh/lektionen/inhaltsverzeichnis' },
      { text: '语法', link: '/zh/grammatik' },
      { text: 'QA', link: '/qa_viewer.html', target: '_blank' },
      { text: '<span class="nav-gear-icon"></span>', link: '/zh/settings', ariaLabel: 'Settings' },
      { text: '致谢', link: '/zh/impressum' }
    ],
    docFooter: {
      prev: '上一课',
      next: '下一课'
    },
    sidebar: [
      { text: '目录', link: '/zh/lektionen/inhaltsverzeichnis' },
      { text: '语法索引', link: '/zh/grammatik' },
      { text: '词汇表', link: '/zh/lektionen/wortliste' },
      { text: '课程', collapsed: false, items: [] },
      { text: '书写', collapsed: true, items: [] },
      { text: '练习', collapsed: true, items: [] },
      { text: '法律信息', collapsed: true, items: [
          { text: '致谢与引用', link: '/zh/impressum' },
          { text: '图片许可证', link: '/zh/licenses' }
      ]}
    ],
    footer: {
      message: 'Tüpfli 全球村庄图书馆的一部分',
      copyright: '版权所有 © 2008-2010 Alois Payer'
    }
  }
}
