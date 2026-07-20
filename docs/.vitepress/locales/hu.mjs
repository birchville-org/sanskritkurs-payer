export const hu = {
  label: 'HU - Magyar',
  lang: 'hu-HU',
  link: '/hu/',
  title: 'Szanszkrit tanfolyam',
  description: 'Szanszkrit nyelvtan tankönyv, írta Alois Payer',
  themeConfig: {
    outline: { level: [2, 3], label: 'Ezen az oldalon' },
    returnToTopLabel: 'Vissza a tetejére',
    sidebarMenuLabel: 'Menü',
    darkModeSwitchLabel: 'Megjelenés',
    lightModeSwitchTitle: 'Váltás világos témára',
    darkModeSwitchTitle: 'Váltás sötét témára',
    langMenuLabel: 'Nyelvváltás',
    nav: [
      { text: 'Főoldal', link: '/hu/' },
      { text: 'Tartalomjegyzék', link: '/hu/lektionen/inhaltsverzeichnis' },
      { text: 'QA', link: '/qa_viewer.html', target: '_blank' },
      { text: 'Impresszum', link: '/hu/impressum' },
      { text: '<span class="nav-gear-icon"></span>', link: '/hu/settings', ariaLabel: 'Beállítások' }
    ],
    docFooter: {
      prev: 'Előző lecke',
      next: 'Következő lecke'
    },
    sidebar: [
      { text: 'Tartalomjegyzék', link: '/hu/lektionen/inhaltsverzeichnis' },
      { text: 'Nyelvtani témák', link: '/hu/grammatik' },
      { text: 'Nyelvtani mutató', link: '/hu/themen' },
      { text: 'Szójegyzék', link: '/hu/lektionen/wortliste' },
      { text: 'Glosszárium', link: '/hu/lektionen/glossar' },
      { text: 'Leckék', collapsed: false, items: [] },
      { text: 'Írásrendszer', collapsed: true, items: [] },
      { text: 'Gyakorlatok', collapsed: true, items: [] },
      { text: 'Jogi információk', collapsed: true, items: [
          { text: 'Jogi nyilatkozat és hivatkozás', link: '/hu/impressum' },
          { text: 'Képek licencei', link: '/hu/licenses' },
      ]}
    ],
    footer: {
      message: "A Tüpfli Global Village könyvtár része",
      copyright: 'Copyright © 2008-2010 Alois Payer'
    }
  }
}
