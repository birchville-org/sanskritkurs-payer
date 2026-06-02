
export const pa = {
  label: 'PA',
  lang: 'pa-IN',
  link: '/pa/',
  title: 'ਸੰਸਕ੍ਰਿਤ ਕੋਰਸ',
  description: 'ਅਲੋਇਸ ਪਾਏਰ ਦੀ ਵਿਆਕਰਨ ਪਾਠ ਪੁਸਤਕ',
  themeConfig: {
    outline: { level: [2, 3], label: 'ਇਸ ਪੰਨੇ \'ਤੇ' },
    nav: [
      { text: 'ਮੁੱਖ ਪੰਨਾ', link: '/pa/' },
      { text: 'ਵਿਸ਼ਾ ਸੂਚੀ', link: '/pa/lektionen/inhaltsverzeichnis' },
      { text: 'ਵਿਆਕਰਨ ਸੂਚਕਾਂਕ', link: '/pa/grammatik' },
      { text: 'QA', link: '/qa_viewer.html', target: '_blank' },
      { text: 'ਯੋਗਦਾਨੀ', link: '/pa/impressum' }
    ],
    docFooter: {
      prev: 'ਪਿਛਲਾ ਪਾਠ',
      next: 'ਅਗਲਾ ਪਾਠ'
    },
    sidebar: [
      { text: 'ਵਿਸ਼ਾ ਸੂਚੀ', link: '/pa/lektionen/inhaltsverzeichnis' },
      { text: 'ਵਿਆਕਰਨ ਵਿਸ਼ੇ (ਵਰਣਮਾਲਾ ਅਨੁਸਾਰ)', link: '/pa/grammatik' },
      { text: 'ਸ਼ਬਦ ਸੂਚੀ', link: '/pa/lektionen/wortliste' },
      { text: 'ਸ਼ਬਦਕੋਸ਼', link: '/pa/lektionen/glossar' },
      { text: 'ਪਾਠ', collapsed: false, items: [] },
      { text: 'ਲਿਪੀ (ਜਾਣ-ਪਛਾਣ)', collapsed: true, items: [] },
      { text: 'ਅਭਿਆਸ', collapsed: true, items: [] },
      { text: 'ਕਾਨੂੰਨੀ', collapsed: true, items: [
          { text: 'ਕਾਨੂੰਨੀ ਸੂਚਨਾ ਅਤੇ ਹਵਾਲਾ', link: '/pa/impressum' },
          { text: 'ਚਿੱਤਰ ਲਾਇਸੈਂਸ', link: '/pa/licenses' }
      ]}
    ],
    footer: {
      message: "Tüpfli's Global Village Library ਦਾ ਹਿੱਸਾ",
      copyright: 'Copyright © 2008-2010 Alois Payer'
    }
  }
}
