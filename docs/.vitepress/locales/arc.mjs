
export const arc = {
  label: 'ARC',
  lang: 'arc',
  dir: 'rtl',
  link: '/arc/',
  title: 'ܝܘܠܦܢܐ ܕܣܢܣܩܪܝܛ',
  description: 'ܟܬܒܐ ܕܝܘܠܦܢܐ ܡܢ ܐܠܘܝܣ ܦܝܝܪ',
  themeConfig: {
    outline: { level: [2, 3], label: 'ܒܗܢ ܦܐܬܐ' },
    nav: [
      { text: 'ܪܝܫܐ', link: '/arc/' },
      { text: 'ܠܘܚܐ ܕܣܘܟܠ̈ܐ', link: '/arc/lektionen/inhaltsverzeichnis' },
      { text: 'ܕܩܕܘܩܝܐ', link: '/arc/grammatik' },
      { text: 'QA', link: '/qa_viewer.html', target: '_blank' },
      { text: '<span class="nav-gear-icon"></span>', link: '/arc/settings', ariaLabel: 'Settings' },
      { text: 'ܙܘܗܪ̈ܐ', link: '/arc/impressum' }
    ],
    docFooter: {
      prev: 'ܡܠܦܢܘܬܐ ܕܩܕܡ',
      next: 'ܡܠܦܢܘܬܐ ܕܒܬܪ'
    },
    sidebar: [
      { text: 'ܠܘܚܐ ܕܣܘܟܠ̈ܐ', link: '/arc/lektionen/inhaltsverzeichnis' },
      { text: 'ܕܩܕܘܩܝܐ', link: '/arc/grammatik' },
      { text: 'ܡܠ̈ܐ', link: '/arc/lektionen/wortliste' },
      { text: 'ܡܠܦܢܘ̈ܬܐ', collapsed: false, items: [] },
      { text: 'ܟܬܒ̈ܬܐ', collapsed: true, items: [] },
      { text: 'ܬܪ̈ܓܘܡܐ', collapsed: true, items: [] },
      { text: 'ܙܘܗܪ̈ܐ', collapsed: true, items: [
          { text: 'ܙܘܗܪ̈ܐ ܘܐܝܩܪ̈ܐ', link: '/arc/impressum' },
          { text: 'ܙܕܩ̈ܐ ܕܨܘܪ̈ܐ', link: '/arc/licenses' }
      ]}
    ],
    footer: {
      message: 'ܡܢ Global Village Library ܕ Tüpfli',
      copyright: 'ܙܕܩ̈ܐ ܕܟܬܒܐ © 2008-2010 Alois Payer'
    }
  }
}
