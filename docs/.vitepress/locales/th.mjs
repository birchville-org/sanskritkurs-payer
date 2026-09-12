export const th = {
  label: '🇹🇭 TH - ไทย',
  lang: 'th-TH',
  link: '/th/',
  title: 'หลักสูตรสันสกฤต',
  description: 'หนังสือเรียนไวยากรณ์โดย Alois Payer',
  themeConfig: {
    outline: { level: [2, 3], label: 'ในหน้านี้' },
    returnToTopLabel: 'กลับสู่ด้านบน',
    sidebarMenuLabel: 'เมนู',
    darkModeSwitchLabel: 'ลักษณะ',
    lightModeSwitchTitle: 'เปลี่ยนเป็นธีมสว่าง',
    darkModeSwitchTitle: 'เปลี่ยนเป็นธีมมืด',
    langMenuLabel: 'เปลี่ยนภาษา',
    nav: [
      { text: 'หน้าหลัก', link: '/th/' },
      { text: 'สารบัญ', link: '/th/lektionen/inhaltsverzeichnis' },
      { text: 'QA', link: '/qa_viewer.html', target: '_blank' },
      { text: 'เครดิต', link: '/th/impressum' },
      { text: '<span class="nav-gear-icon"></span>', link: '/th/settings', ariaLabel: 'เปิดการตั้งค่า' }
    ],
    docFooter: {
      prev: 'บทก่อนหน้า',
      next: 'บทถัดไป'
    },
    sidebar: [
      { text: 'สารบัญ', link: '/th/lektionen/inhaltsverzeichnis' },
      { text: 'หัวข้อไวยากรณ์', link: '/th/grammatik' },
      { text: 'ดัชนีไวยากรณ์', link: '/th/themen' },
      { text: 'ศัพท์', link: '/th/lektionen/wortliste' },
      { text: 'คัมภีร์', link: '/th/lektionen/glossar' },
      { text: 'บทเรียน', collapsed: false, items: [] },
      { text: 'สคริปต์ (แนะนำ)', collapsed: true, items: [] },
      { text: 'การฝึกหัด', collapsed: true, items: [] },
      { text: 'กฎหมาย', collapsed: true, items: [
          { text: 'ประกาศและอ้างอิง', link: '/th/impressum' },
          { text: 'สิทธิ์ภาพ', link: '/th/licenses' },
      ]}
    ],
    footer: {
      message: "ส่วนหนึ่งของห้องสมุดหมู่บ้านทั่วโลกของ Tüpfli",
      copyright: 'ลิขสิทธิ์ © 2008-2010 Alois Payer'
    }
  }
}
