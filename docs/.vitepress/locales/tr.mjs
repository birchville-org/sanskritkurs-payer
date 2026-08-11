export const tr = {
  label: '🇹🇷 TR - Türkçe',
  lang: 'tr-TR',
  title: 'Sanskrit Kursu',
  description: 'Alois Payer Gramer Ders Kitabı',
  themeConfig: {
    outline: { level: [2, 3], label: 'Bu sayfada' },
    returnToTopLabel: 'Başa dön',
    sidebarMenuLabel: 'Menü',
    darkModeSwitchLabel: 'Görünüm',
    lightModeSwitchTitle: 'Açık temaya geç',
    darkModeSwitchTitle: 'Karanlık temaya geç',
    langMenuLabel: 'Dil değiştir',
    nav: [
      { text: 'Ana Sayfa', link: '/tr/' },
      { text: 'İçindekiler', link: '/tr/lektionen/inhaltsverzeichnis' },
      { text: 'Künye', link: '/tr/impressum' },
      { text: '<span class="nav-gear-icon"></span>', link: '/tr/settings', ariaLabel: 'Ayarları aç' }
    ],
    docFooter: {
      prev: 'Önceki Ders',
      next: 'Sonraki Ders'
    },
    sidebar: [
      { text: 'İçindekiler', link: '/tr/lektionen/inhaltsverzeichnis' },
      { text: 'Gramer Konuları', link: '/tr/grammatik' },
      { text: 'Gramer İndeksi', link: '/tr/themen' },
      { text: 'Kelime Listesi', link: '/tr/lektionen/wortliste' },
      { text: 'Sözlük', link: '/tr/lektionen/glossar' },
      { text: 'Dersler', collapsed: false, items: [] },
      { text: 'Yazı (Giriş)', collapsed: true, items: [] },
      { text: 'Egzersizler', collapsed: true, items: [] },
      { text: 'Yasal', collapsed: true, items: [
          { text: 'Künye & Atıf', link: '/tr/impressum' },
          { text: 'Görsel Lisansları (Denetim)', link: '/tr/licenses' },
      ]}
    ],
    footer: {
      message: "Teil der Tüpfli's Global Village Library",
      copyright: 'Copyright © 2008-2010 Alois Payer'
    }
  }
}
