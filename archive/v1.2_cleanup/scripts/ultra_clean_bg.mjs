import fs from 'fs'
import path from 'path'

const bgDir = 'docs/bg/lektionen'

const replacements = [
    // Articles & Basic Particles
    { from: /\b(das|die|der|dem|den|des|ein|eine|einer|einem|einen|eines|es|e|en|er|es|em)\b(?!\w)/gi, to: '' },
    
    // Grammatical Terms (with inflections)
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
    { from: /\bперфект(um)?\b/gi, to: 'перфект' },
    { from: /\bабсолютив(um)?\b/gi, to: 'абсолютив' },
    { from: /\bинтензитив(um)?\b/gi, to: 'интензитив' },
    { from: /\bдепозитив(um)?\b/gi, to: 'депозитив' },
    { from: /\bпредна част(s)?\b/gi, to: 'преден член' },
    { from: /\bзадна част(s)?\b/gi, to: 'заден член' },
    { from: /\bабсолютив(um|s)\b/gi, to: 'абсолютив' },
    { from: /\bAntworten\b/gi, to: 'Отговори' },
    { from: /\bSprichwörter\b/gi, to: 'Поговорки' },
    { from: /\bu\.s\.w\.\b/gi, to: 'и т.н.' },
    { from: /\bzum\b/gi, to: 'към' },
    { from: /\bKomparative\b/gi, to: 'степени за сравнение' },
    { from: /\bepische\b/gi, to: 'епичен' },
    { from: /\bSchlussglieds\b/gi, to: 'краен член' },
    { from: /\bes\b/gi, to: '' },
    { from: /\bvorderglied(er)?(s)?\b/gi, to: 'преден член' },
    { from: /\bhinterglied(er)?(s)?\b/gi, to: 'заден член' },
    { from: /\bschlussglied(er)?(s)?\b/gi, to: 'краен член' },
    { from: /\bвтора част\b/gi, to: 'втора част' },
    { from: /\bZweite\b/gi, to: 'Втори' },
    { from: /\bErste\b/gi, to: 'Първи' },
    { from: /\bDritte\b/gi, to: 'Трети' },
    { from: /\bVierte\b/gi, to: 'Четвърти' },
    { from: /\bFünfte\b/gi, to: 'Пети' },
    { from: /\bSechste\b/gi, to: 'Шести' },
    { from: /\bSiebte\b/gi, to: 'Седми' },
    { from: /\bAchte\b/gi, to: 'Осми' },
    { from: /\bNeunte\b/gi, to: 'Девети' },
    { from: /\bZehnte\b/gi, to: 'Десети' },
    { from: /\bVerben\b/gi, to: 'Глаголи' },
    { from: /\bTyp\b/gi, to: 'тип' },
    { from: /\bvom\b/gi, to: 'от' },
    { from: /\bstufen\b/gi, to: 'степени' },
    { from: /\bstufe\b/gi, to: 'степен' },
    { from: /\babstufung\b/gi, to: 'степенуване' },
    { from: /\boбща\b/gi, to: 'обща' },
    { from: /\bNominalbildungen\b/gi, to: 'Именни образувания' },
    { from: /\bkasuellem\b/gi, to: 'падежен' },
    { from: /\bandere\b/gi, to: 'друга' },
    { from: /\bArten\b/gi, to: 'видове' },
    { from: /\bVerhältnis\b/gi, to: 'отношение' },
    { from: /\bFlexion\b/gi, to: 'флексия (склонение)' },
    { from: /\bForm\b/gi, to: 'Форма' },
    { from: /\bSatz\b/gi, to: 'изречение' },
    { from: /\bSandhi\b/gi, to: 'сандхи' },
    { from: /\bWort\b/gi, to: 'дума' },
    { from: /\bЕinteilung\b/gi, to: 'Класификация' },
    { from: /\bGebrauch\b/gi, to: 'Употреба' },
    { from: /\bÜbersicht\b/gi, to: 'Преглед' },
    { from: /\bWortliste\b/gi, to: 'Речник' },
    { from: /\bÜbung\b/gi, to: 'Упражнение' },
    { from: /\bLektion\b/gi, to: 'Урок' },
    { from: /\bWeitere\b/gi, to: 'Още' },
    { from: /\bFragen\b/gi, to: 'въпроси' },
    { from: /\bВeispiel(e)?\b/gi, to: 'Пример(и)' },
    { from: /\bWiederholung\b/gi, to: 'Преговор' },
    { from: /\bBildung\b/gi, to: 'Образуване' },
    { from: /\bBildungen\b/gi, to: 'Образувания' },
    { from: /\bBesondere\b/gi, to: 'Особени' },
    { from: /\bperiphrastisch(es)?\b/gi, to: 'перифрастично' },
    { from: /\bпрезентен клас(n)?\b/gi, to: 'презентен клас' },
    { from: /\bкъм\b/g, to: 'към' }, // Conjunction already fixed
    { from: /\bи\b/g, to: 'и' },
];

const files = fs.readdirSync(bgDir).filter(f => f.endsWith('.md'));

files.forEach(file => {
    const filePath = path.join(bgDir, file);
    let content = fs.readFileSync(filePath, 'utf8');
    let original = content;

    replacements.forEach(r => {
        content = content.replace(r.from, r.to);
    });

    // Post-cleanup
    content = content.replace(/  +/g, ' ');
    content = content.replace(/ \./g, '.');
    content = content.replace(/ ,/g, ',');
    
    // Fix common Bulgarian typo patterns after multiple replaces
    content = content.replace(/преден членs/g, 'преден член');
    content = content.replace(/основастепенуване/g, 'степенуване на основата');
    content = content.replace(/презентен класn/g, 'презентни класове');

    if (content !== original) {
        fs.writeFileSync(filePath, content, 'utf8');
        console.log(`Ultra cleaned ${file}`);
    }
});
