
export const ta = {
  label: 'TA',
  lang: 'ta-IN',
  link: '/ta/',
  title: 'சமஸ்கிருத பாடநெறி',
  description: 'ஆலோயிஸ் பயர் எழுதிய இலக்கண பாடநூல்',
  themeConfig: {
    outline: { level: [2, 3], label: 'இந்த பக்கத்தில்' },
    nav: [
      { text: 'முகப்பு', link: '/ta/' },
      { text: 'உள்ளடக்கம்', link: '/ta/lektionen/inhaltsverzeichnis' },
      { text: 'அகரவரிசை', link: '/ta/grammatik' },
      { text: 'QA', link: '/qa_viewer.html', target: '_blank' },
      { text: 'பங்களிப்பாளர்கள்', link: '/ta/impressum' }
    ],
    docFooter: {
      prev: 'முந்தைய பாடம்',
      next: 'அடுத்த பாடம்'
    },
    sidebar: [
      { text: 'உள்ளடக்கம்', link: '/ta/lektionen/inhaltsverzeichnis' },
      { text: 'இலக்கண தலைப்புகள் (அகரவரிசை)', link: '/ta/grammatik' },
      { text: 'சொற்களஞ்சியம்', link: '/ta/lektionen/wortliste' },
      { text: 'சொல்லகராதி', link: '/ta/lektionen/glossar' },
      { text: 'பாடங்கள்', collapsed: false, items: [] },
      { text: 'எழுத்து (அறிமுகம்)', collapsed: true, items: [] },
      { text: 'பயிற்சிகள்', collapsed: true, items: [] },
      { text: 'சட்ட தகவல்', collapsed: true, items: [
          { text: 'சட்ட அறிவிப்பு & மேற்கோள்', link: '/ta/impressum' },
          { text: 'படப் உரிமங்கள்', link: '/ta/licenses' }
      ]}
    ],
    footer: {
      message: "Tüpfli's Global Village Library-இன் பகுதி",
      copyright: 'Copyright © 2008-2010 Alois Payer'
    }
  }
}
