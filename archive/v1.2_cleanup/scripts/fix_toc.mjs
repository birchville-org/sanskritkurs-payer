import fs from 'fs'
import path from 'path'

const tocPath = 'docs/bg/lektionen/inhaltsverzeichnis.md'
let content = fs.readFileSync(tocPath, 'utf8')

// Fix encoding if needed (if it was double encoded)
// This is a common pattern for the reported corruption
function fixDoubleEncoding(str) {
  try {
    return decodeURIComponent(escape(str));
  } catch (e) {
    return str;
  }
}

// content = fixDoubleEncoding(content) // Only if confirmed, but the subagent reported it.
// Actually, if cat -v showed M-^J, it means the bytes are there but maybe the editor is confused.
// I'll just rewrite the frontmatter and the title manually to be sure.

content = content.replace(/^---[\s\S]*?---/, `---
title: Съдържание
outline: [2, 2]
---`)

content = content.replace(/^# Съдържание/, '# Съдържание')

// Global cleanup of common German words that might have escaped the previous script
const extraReplacements = [
    { from: /Die корени/g, to: 'Корените' },
    { from: /Einfache Ergänzungsfragen/g, to: 'Обикновени въпроси за допълване' },
    { from: /Fragepronomina/g, to: 'Въпросителни местоимения' },
    { from: /Demonstrativpronomina/g, to: 'Показателни местоимения' },
    { from: /Frageformeln/g, to: 'Въпросителни формули' },
    { from: /Einteilung der/g, to: 'Класификация на' },
    { from: /Gebrauch des/g, to: 'Употреба на' },
    { from: /Zum Gebrauch des/g, to: 'Относно употребата на' },
    { from: /die epische/g, to: 'епичната' },
    { from: /Übersicht über/g, to: 'Преглед на' },
    { from: /Personalendungen/g, to: 'Лични окончания' },
    { from: /Personalpronomen/g, to: 'Лично местоимение' },
    { from: /der passiven Notwendigkeit/g, to: 'на пасивната необходимост' },
    { from: /Unterschiede im/g, to: 'Разлики в' },
    { from: /Keine Verbindung mit/g, to: 'Без връзка с' },
    { from: /Stämme auf/g, to: 'Основи на' },
    { from: /Bildung der/g, to: 'Образуване на' },
    { from: /Personalendungen/g, to: 'Лични окончания' },
    { from: /Verbform/g, to: 'глаголна форма' },
    { from: /Personalendungen/g, to: 'Лични окончания' },
    { from: /Bildungstypen des/g, to: 'Типове образуване на' },
    { from: /nur P/g, to: 'само P' },
    { from: /Entlassung in den Ozean der Sanskritliteratur/g, to: 'Отплаване в океана на санскритската литература' },
    { from: /КРАЙ НА КУРСА ПО САНСКРИТ/g, to: 'КРАЙ НА КУРСА ПО САНСКРИТ' },
];

extraReplacements.forEach(r => {
    content = content.replace(r.from, r.to);
});

fs.writeFileSync(tocPath, content, 'utf8')
console.log('TOC updated successfully.')
