export const id = {
  label: 'ID',
  lang: 'id-ID',
  link: '/id/',
  title: 'Kursus Sanskerta',
  description: 'Buku teks tata bahasa oleh Alois Payer',
  themeConfig: {
    outline: { level: [2, 3], label: 'Di halaman ini' },
    returnToTopLabel: 'Kembali ke atas',
    sidebarMenuLabel: 'Menu',
    darkModeSwitchLabel: 'Tampilan',
    lightModeSwitchTitle: 'Beralih ke tema terang',
    darkModeSwitchTitle: 'Beralih ke tema gelap',
    langMenuLabel: 'Ubah bahasa',
    nav: [
      { text: 'Beranda', link: '/en/' },
      { text: 'Daftar Isi', link: '/en/lektionen/inhaltsverzeichnis' },
      { text: 'QA', link: '/qa_viewer.html', target: '_blank' },
      { text: 'Kredit', link: '/en/impressum' },
      { text: '<span class="nav-gear-icon"></span>', link: '/en/settings', ariaLabel: 'Buka Pengaturan' }
    ],
    docFooter: {
      prev: 'Pelajaran Sebelumnya',
      next: 'Pelajaran Selanjutnya'
    },
    sidebar: [
      { text: 'Daftar Isi', link: '/en/lektionen/inhaltsverzeichnis' },
      { text: 'Topik Tata Bahasa', link: '/en/grammatik' },
            { text: 'Indeks Tata Bahasa', link: '/en/themen' },
      { text: 'Kosakata', link: '/en/lektionen/wortliste' },
      { text: 'Glosarium', link: '/en/lektionen/glossar' },
      { text: 'Pelajaran', collapsed: false, items: [] },
      { text: 'Naskah (Pendahuluan)', collapsed: true, items: [] },
      { text: 'Latihan', collapsed: true, items: [] },
      { text: 'Hukum', collapsed: true, items: [
          { text: 'Pemberitahuan Hukum & Kutipan', link: '/en/impressum' },
          { text: 'Lisensi Gambar', link: '/en/licenses' },
      ]}
    ],
    footer: {
      message: "Bagian dari Perpustakaan Desa Global Tüpfli",
      copyright: 'Hak Cipta © 2008-2010 Alois Payer'
    }
  }
}
