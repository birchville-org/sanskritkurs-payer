export const zhCN = {
  label: '🇨🇳 ZH-CN - 简体中文',
  lang: 'zh-CN',
  link: '/zh-CN/',
  title: '梵语课程',
  description: 'Alois Payer 编写的语法教材',
  themeConfig: {
    outline: { level: [2, 3], label: '本页目录' },
    returnToTopLabel: '回到顶部',
    sidebarMenuLabel: '菜单',
    darkModeSwitchLabel: '外观',
    lightModeSwitchTitle: '切换到浅色主题',
    darkModeSwitchTitle: '切换到深色主题',
    langMenuLabel: '切换语言',
    nav: [
      { text: '首页', link: '/zh-CN/' },
      { text: '目录', link: '/zh-CN/lektionen/inhaltsverzeichnis' },
      { text: '问答', link: '/qa_viewer.html', target: '_blank' },
      { text: '鸣谢', link: '/zh-CN/impressum' },
      { text: '<span class="nav-gear-icon"></span>', link: '/zh-CN/settings', ariaLabel: '打开设置' }
    ],
    docFooter: {
      prev: '上一课',
      next: '下一课'
    },
    sidebar: [
      { text: '目录', link: '/zh-CN/lektionen/inhaltsverzeichnis' },
      { text: '语法主题', link: '/zh-CN/grammatik' },
            { text: '语法索引', link: '/zh-CN/themen' },
      { text: '词汇表', link: '/zh-CN/lektionen/wortliste' },
      { text: '术语表', link: '/zh-CN/lektionen/glossar' },
      { text: '课程', collapsed: false, items: [] },
      { text: '脚本（简介）', collapsed: true, items: [] },
      { text: '练习', collapsed: true, items: [] },
      { text: '法律声明', collapsed: true, items: [
          { text: '法律声明与引用', link: '/zh-CN/impressum' },
          { text: '图片许可', link: '/zh-CN/licenses' },
      ]}
    ],
    footer: {
      message: "Tüpfli 全球村图书馆的一部分",
      copyright: '版权所有 © 2008-2010 Alois Payer'
    }
  }
}
