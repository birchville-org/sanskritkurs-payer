
export const cop = {
  label: 'COP - Coptic',
  lang: 'cop',
  link: '/cop/',
  title: 'ⲡⲓⲙⲁⲑⲏⲙⲁ ⲛ̀ⲥⲁⲛⲥⲕⲣⲓⲧ',
  description: 'ⲫⲓϫⲱⲙ ⲛ̀ⲅⲣⲁⲙⲙⲁⲣⲓⲟⲛ ⲛ̀ϧⲏⲧ ⲁⲗⲟⲓⲥ ⲡⲁⲓⲉⲣ',
  themeConfig: {
    outline: { level: [2, 3], label: 'ϩⲛ̀ ϯⲥⲉⲗⲓⲥ' },
    nav: [
      { text: 'ⲡⲓⲁⲣⲭⲏ', link: '/cop/' },
      { text: 'ⲡⲓⲡⲓⲛⲁⲝ', link: '/cop/lektionen/inhaltsverzeichnis' },
      { text: 'ⲅⲣⲁⲙⲙⲁⲣⲓⲟⲛ', link: '/cop/grammatik' },
      { text: 'QA', link: '/qa_viewer.html', target: '_blank' },
      { text: '<span class="nav-gear-icon"></span>', link: '/cop/settings', ariaLabel: 'Settings' },
      { text: 'ⲡⲓⲧⲁⲓⲟ', link: '/cop/impressum' }
    ],
    docFooter: {
      prev: 'ⲡⲓⲙⲁⲑⲏⲙⲁ ⲉⲧϩⲁϩⲧⲏϥ',
      next: 'ⲡⲓⲙⲁⲑⲏⲙⲁ ⲉⲧⲁϩⲉⲣⲁⲧϥ'
    },
    sidebar: [
      { text: 'ⲡⲓⲡⲓⲛⲁⲝ', link: '/cop/lektionen/inhaltsverzeichnis' },
      { text: 'ⲡⲓⲅⲣⲁⲙⲙⲁⲣⲓⲟⲛ', link: '/cop/grammatik' },
      { text: 'ⲛⲓϣⲁϫⲓ', link: '/cop/lektionen/wortliste' },
      { text: 'ⲛⲓⲙⲁⲑⲏⲙⲁⲧⲁ', collapsed: false, items: [] },
      { text: 'ⲡⲓⲥϧⲁⲓ', collapsed: true, items: [] },
      { text: 'ⲛⲓⲙⲉⲗⲉⲧⲏ', collapsed: true, items: [] },
      { text: 'ⲛⲓⲛⲟⲙⲟⲥ', collapsed: true, items: [
          { text: 'ⲡⲓⲧⲁⲓⲟ ⲛⲉⲙ ⲫⲓϩⲓⲕⲁⲛⲟⲥ', link: '/cop/impressum' },
          { text: 'ⲛⲓϩⲓⲥⲓ ⲛ̀ϩⲁⲛϩⲓⲕⲱⲛ', link: '/cop/licenses' }
      ]}
    ],
    footer: {
      message: 'ⲟⲩⲙⲉⲣⲟⲥ ⲛ̀ⲧⲉ Global Village Library ⲛ̀Tüpfli',
      copyright: 'ⲡⲓⲛⲟⲙⲟⲥ ⲛ̀ⲧⲉ ⲡⲓⲥϧⲁⲓ © 2008-2010 Alois Payer'
    }
  }
}
