export const vi = {
  label: '🇻🇳 VI - Tiếng Việt',
  lang: 'vi-VN',
  title: 'Khóa học Phạn văn',
  description: 'Sách giáo khoa Ngữ pháp của Alois Payer',
  themeConfig: {
    outline: { level: [2, 3], label: 'Trên trang này' },
    returnToTopLabel: 'Trở lại đầu trang',
    sidebarMenuLabel: 'Menu',
    darkModeSwitchLabel: 'Giao diện',
    lightModeSwitchTitle: 'Chuyển sang giao diện sáng',
    darkModeSwitchTitle: 'Chuyển sang giao diện tối',
    langMenuLabel: 'Đổi ngôn ngữ',
    nav: [
      { text: 'Trang chủ', link: '/vi/' },
      { text: 'Mục lục', link: '/vi/lektionen/inhaltsverzeichnis' },
      { text: 'Thông tin pháp lý', link: '/vi/impressum' },
      { text: '<span class="nav-gear-icon"></span>', link: '/vi/settings', ariaLabel: 'Mở cài đặt' }
    ],
    docFooter: {
      prev: 'Bài học trước',
      next: 'Bài học tiếp theo'
    },
    sidebar: [
      { text: 'Mục lục', link: '/vi/lektionen/inhaltsverzeichnis' },
      { text: 'Chủ đề ngữ pháp', link: '/vi/grammatik' },
      { text: 'Chỉ mục ngữ pháp', link: '/vi/themen' },
      { text: 'Danh sách từ vựng', link: '/vi/lektionen/wortliste' },
      { text: 'Thuật ngữ', link: '/vi/lektionen/glossar' },
      { text: 'Bài học', collapsed: false, items: [] },
      { text: 'Chữ viết (Giới thiệu)', collapsed: true, items: [] },
      { text: 'Bài tập', collapsed: true, items: [] },
      { text: 'Pháp lý', collapsed: true, items: [
          { text: 'Thông tin pháp lý & Trích dẫn', link: '/vi/impressum' },
          { text: 'Bản quyền hình ảnh', link: '/vi/licenses' },
      ]}
    ],
    footer: {
      message: "Teil der Tüpfli's Global Village Library",
      copyright: 'Copyright © 2008-2010 Alois Payer'
    }
  }
}
