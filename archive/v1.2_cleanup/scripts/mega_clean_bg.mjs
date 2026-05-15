import fs from 'fs'
import path from 'path'

const bgDir = 'docs/bg/lektionen'

const replacements = [
    // Articles & Particles (case insensitive with word boundaries)
    { from: /\b(das|die|der|dem|den|des)\b/gi, to: '' },
    { from: /\bein|eine|einer|einem|einen|eines\b/gi, to: '' },
    { from: /\bund\b/gi, to: 'и' },
    { from: /\boder\b/gi, to: 'или' },
    { from: /\bmit\b/gi, to: 'с' },
    { from: /\bvon\b/gi, to: 'от' },
    { from: /\bzu\b/gi, to: 'към' },
    { from: /\bbei\b/gi, to: 'при' },
    { from: /\bnach\b/gi, to: 'след' },
    { from: /\bvor\b/gi, to: 'пред' },
    { from: /\baus\b/gi, to: 'от' },
    { from: /\bauf\b/gi, to: 'върху' },
    { from: /\bfür\b/gi, to: 'за' },
    { from: /\bin\b/gi, to: 'в' },
    { from: /\bals\b/gi, to: 'като' },
    { from: /\bist\b/gi, to: 'е' },
    { from: /\bsind\b/gi, to: 'са' },

    // Pedagogical/Grammatical terms with inflections
    { from: /\battributiv(e|em|en|er|es)?\b/gi, to: 'атрибутивен' },
    { from: /\bappositionell(e|em|en|er|es)?\b/gi, to: 'апозиционен' },
    { from: /\badverbial(e|em|en|er|es)?\b/gi, to: 'адвербиален' },
    { from: /\bnominal(e|em|en|er|es)?\b/gi, to: 'номинален' },
    { from: /\bverbal(e|em|en|er|es)?\b/gi, to: 'глаголен' },
    { from: /\bthematisch(e|em|en|er|es)?\b/gi, to: 'тематичен' },
    { from: /\bathematisch(e|em|en|er|es)?\b/gi, to: 'атематичен' },
    { from: /\bstark(e|em|en|er|es)?\b/gi, to: 'силен' },
    { from: /\bschwach(e|em|en|er|es)?\b/gi, to: 'слаб' },
    { from: /\bvokalisch(e|em|en|er|es)?\b/gi, to: 'вокален' },
    { from: /\bkonsonantisch(e|em|en|er|es)?\b/gi, to: 'консонантен' },
    { from: /\bdeklination\b/gi, to: 'склонение' },
    { from: /\bkonjugation\b/gi, to: 'спрежение' },
    { from: /\bkomposita\b/gi, to: 'композити' },
    { from: /\bkompositum\b/gi, to: 'композит' },
    { from: /\bvorderglied(er)?(s)?\b/gi, to: 'преден член' },
    { from: /\bhinterglied(er)?(s)?\b/gi, to: 'заден член' },
    { from: /\bпредна част(s)?\b/g, to: 'преден член' }, // Fix previous partial translation
    { from: /\bзадна част(s)?\b/g, to: 'заден член' },
    { from: /\bкорени\b/g, to: 'корени' }, // Fix cases where it might have been half-translated
    { from: /\bкорен\b/g, to: 'корен' },

    // Specific leftover phrases from the screenshot
    { from: /\bBedeutungen от nañ-Tatpuruṣa\b/g, to: 'Значения на нан-татпуруша' },
    { from: /\babsolutivum\b/gi, to: 'абсолютив' },
    { from: /\bForm des преден членs\b/g, to: 'Форма на предния член' },
    { from: /\bв композити\b/g, to: 'в композити' },
    
    // More terms
    { from: /\bBesondere Bildungen\b/gi, to: 'Особени образувания' },
    { from: /\bperiphrastisch(e|em|en|er|es)?\b/gi, to: 'перифрастичен' },
    { from: /\bbisher gelernten\b/gi, to: 'научените досега' },
    { from: /\bÜbersetzungsübung\b/gi, to: 'Упражнение за превод' },
    { from: /\bWiederholungsübung\b/gi, to: 'Упражнение за преговор' },
    { from: /\bFormenlehre\b/gi, to: 'Морфология' },
    { from: /\bSatzsandhi\b/gi, to: 'Сандхи в изречението' },
    { from: /\bWortsandhi\b/gi, to: 'Сандхи в думата' },
    { from: /\bWortliste\b/gi, to: 'Речник' },
    { from: /\bÜbung\b/gi, to: 'Упражнение' },
    { from: /\bLektion\b/gi, to: 'Урок' },
];

const files = fs.readdirSync(bgDir).filter(f => f.endsWith('.md'));

files.forEach(file => {
    const filePath = path.join(bgDir, file);
    let content = fs.readFileSync(filePath, 'utf8');
    let original = content;

    replacements.forEach(r => {
        content = content.replace(r.from, r.to);
    });

    // Cleanup double spaces and common issues
    content = content.replace(/  +/g, ' ');
    content = content.replace(/ \./g, '.');
    content = content.replace(/ ,/g, ',');

    if (content !== original) {
        fs.writeFileSync(filePath, content, 'utf8');
        console.log(`Deep cleaned ${file}`);
    }
});
