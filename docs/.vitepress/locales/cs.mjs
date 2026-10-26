export const cs = {
  label: '🇨🇿 CS - Čeština',
  lang: 'cs-CZ',
  link: '/cs/',
  title: 'Sanskrtský kurz',
  description: 'Učebnice gramatiky Aloise Payera',
  themeConfig: {
    outline: { level: [2, 3], label: 'Na této stránce' },
    returnToTopLabel: 'Zpět nahoru',
    sidebarMenuLabel: 'Menu',
    darkModeSwitchLabel: 'Vzhled',
    lightModeSwitchTitle: 'Přepnout na světlý motiv',
    darkModeSwitchTitle: 'Přepnout na tmavý motiv',
    langMenuLabel: 'Změnit jazyk',
    nav: [
      { text: 'Hlavní stránka', link: '/cs/' },
      { text: 'Obsah', link: '/cs/lektionen/inhaltsverzeichnis' },
      { text: 'QA', link: '/qa_viewer.html', target: '_blank' },
      { text: 'Tiráž', link: '/cs/impressum' },
      { text: '<span class="nav-gear-icon"></span>', link: '/cs/settings', ariaLabel: 'Otevřít nastavení' }
    ],
    docFooter: {
      prev: 'Předchozí lekce',
      next: 'Následující lekce'
    },
    sidebar: [
      { text: 'Obsah', link: '/cs/lektionen/inhaltsverzeichnis' },
      { text: 'Témata gramatiky', link: '/cs/grammatik' },
      { text: 'Gramatický rejstřík', link: '/cs/themen' },
      { text: 'Slovíčka', link: '/cs/lektionen/wortliste' },
      { text: 'Glosář', link: '/cs/lektionen/glossar' },
      { text: 'Lekce', collapsed: false, items: [] },
      { text: 'Písmo', collapsed: true, items: [] },
      { text: 'Cvičení', collapsed: true, items: [] },
      { text: 'Právní informace', collapsed: true, items: [
          { text: 'Tiráž a citace', link: '/cs/impressum' },
          { text: 'Licence obrázků', link: '/cs/licenses' },
      ]}
    ],
    footer: {
      message: "Součást Global Village Library od Tüpfliho",
      copyright: 'Copyright © 2008-2010 Alois Payer'
    }
  }
}
