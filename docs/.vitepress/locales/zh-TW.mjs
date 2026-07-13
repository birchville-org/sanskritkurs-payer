export const zhTW = {
  label: 'zh-TW',
  lang: 'zh-TW',
  link: '/zh-TW/',
  title: '梵文課程',
  description: 'Alois Payer 的語法教科書',
  themeConfig: {
    outline: { level: [2, 3], label: '本頁目錄' },
    returnToTopLabel: '返回頂部',
    sidebarMenuLabel: '選單',
    darkModeSwitchLabel: '外觀',
    lightModeSwitchTitle: '切換至淺色主題',
    darkModeSwitchTitle: '切換至深色主題',
    langMenuLabel: '切換語言',
    nav: [
      { text: '首頁', link: '/zh-TW/' },
      { text: '目錄', link: '/zh-TW/lektionen/inhaltsverzeichnis' },
      { text: '問答', link: '/qa_viewer.html', target: '_blank' },
      { text: '致謝', link: '/zh-TW/impressum' },
      { text: '<span class="nav-gear-icon"></span>', link: '/zh-TW/settings', ariaLabel: '開啟設定' }
    ],
    docFooter: {
      prev: '上一課',
      next: '下一課'
    },
    sidebar: [
      { text: '目錄', link: '/zh-TW/lektionen/inhaltsverzeichnis' },
      { text: '語法主題', link: '/zh-TW/grammatik' },
            { text: '語法索引', link: '/zh-TW/themen' },
      { text: '詞彙', link: '/zh-TW/lektionen/wortliste' },
      { text: '術語表', link: '/zh-TW/lektionen/glossar' },
      { text: '課程', collapsed: false, items: [] },
      { text: '文字（簡介）', collapsed: true, items: [] },
      { text: '練習', collapsed: true, items: [] },
      { text: '法律資訊', collapsed: true, items: [
          { text: '法律聲明與引用', link: '/zh-TW/impressum' },
          { text: '圖片授權', link: '/zh-TW/licenses' },
      ]}
    ],
    footer: {
      message: "Tüpfli 全球村圖書館的一部分",
      copyright: '版權所有 © 2008-2010 Alois Payer'
    }
  }
}
