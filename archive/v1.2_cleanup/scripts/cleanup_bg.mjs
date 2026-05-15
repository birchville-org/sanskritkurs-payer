import fs from 'fs';
import path from 'path';

const bgDir = './docs/bg/lektionen';

const replacements = [
    // Cases and Numbers (Title Case)
    { from: /Nominativ/g, to: 'Именителен падеж' },
    { from: /Akkusativ/g, to: 'Винителен падеж' },
    { from: /Instrumentalis/g, to: 'Творителен падеж' },
    { from: /Dativ/g, to: 'Дателен падеж' },
    { from: /Ablativ/g, to: 'Отложителен падеж' },
    { from: /Genetiv/g, to: 'Родителен падеж' },
    { from: /Lokativ/g, to: 'Местен падеж' },
  // Conjunctions and common particles
  { from: /\bund\b/g, to: 'и' },
  { from: /\boder\b/g, to: 'или' },
  { from: /\bnach\b/g, to: 'след' },
  { from: /\bmit\b/g, to: 'с' },
  { from: /\bvon\b/g, to: 'от' },
  { from: /\bals\b/g, to: 'като' },
  { from: /\bfür\b/g, to: 'за' },
  { from: /\bdie\b/g, to: 'тези' },
  { from: /\bzu\b/g, to: 'към' },
  { from: /\bbei\b/g, to: 'при' },
  { from: /\bsowie\b/g, to: 'както и' },

  // Grammatical terms
  { from: /Determinativkomposita/g, to: 'Детерминативни композити' },
  { from: /Possesivkomposita/g, to: 'Посесивни композити' },
  { from: /Nominalkomposita/g, to: 'Номинални композити' },
  { from: /Verbalkomposita/g, to: 'Глаголни композити' },
  { from: /Relativsatz/g, to: 'Относително изречение' },
  { from: /Relativpronomen/g, to: 'Относително местоимение' },
  { from: /Personalpronomen/g, to: 'Лично местоимение' },
  { from: /Demonstrativpronomina/g, to: 'Показателни местоимения' },
  { from: /Fragepronomen/g, to: 'Въпросително местоимение' },
  { from: /Indefinitpronomina/g, to: 'Неопределителни местоимения' },
  { from: /Vorderglied/g, to: 'преден член' },
  { from: /Hinterglied/g, to: 'заден член' },
  { from: /Präsensstamm/g, to: 'презентна основа' },
  { from: /Präsensklasse/g, to: 'презентен клас' },
  { from: /Indikativ/g, to: 'индикатив' },
  { from: /Präsens/g, to: 'презент (сегашно време)' },
  { from: /Futur/g, to: 'футур (бъдеще време)' },
  { from: /Aorist/g, to: 'аорист' },
  { from: /Perfekt/g, to: 'перфект' },
  { from: /Imperfekt/g, to: 'имперфект' },
  { from: /Optativ/g, to: 'оптатив' },
  { from: /Imperativ/g, to: 'императив' },
  { from: /Passiv/g, to: 'пасив' },
  { from: /Kausativ/g, to: 'каузатив' },
  { from: /Desiderativ/g, to: 'дезидератив' },
  { from: /Intensiv/g, to: 'интензитив' },
  { from: /Denominativ/g, to: 'деноминатив' },
  { from: /Gerundivum/g, to: 'герундивум' },
  { from: /Absolutiv/g, to: 'абсолютив' },
  { from: /Infinitiv/g, to: 'инфинитив' },
  { from: /Partizip/g, to: 'причастие' },
  { from: /Nominalstamm/g, to: 'именна основа' },
  { from: /Vokal/g, to: 'гласна' },
  { from: /Konsonant/g, to: 'съгласна' },
  { from: /Suffix/g, to: 'суфикс' },
  { from: /Präfix/g, to: 'префикс' },
  { from: /Wurzel/g, to: 'корен' },
  { from: /Stamm/g, to: 'основа' },
  { from: /Endung/g, to: 'окончание' },
  { from: /Kasus/g, to: 'падеж' },
  { from: /Singular/g, to: 'единствено число' },
  { from: /Plural/g, to: 'множествено число' },
  { from: /Dual/g, to: 'двойствено число' },
  { from: /Person/g, to: 'лице' },
  { from: /Maskulinum/g, to: 'мъжки род' },
  { from: /Femininum/g, to: 'женски род' },
  { from: /Neutrum/g, to: 'среден род' },
  { from: /Zahlwort/g, to: 'числително име' },
  { from: /Adverb/g, to: 'наречие' },
  { from: /Präposition/g, to: 'предлог' },
  { from: /Partikel/g, to: 'частица' },
  { from: /Satz/g, to: 'изречение' },
  { from: /Wort/g, to: 'дума' },
  { from: /Laut/g, to: 'звук' },
  { from: /Silbe/g, to: 'сричка' },

  // Special pedagogical terms
  { from: /Ablaut/g, to: 'аблаут (степенуване на гласните)' },
  { from: /Hochstufe/g, to: 'висока степен' },
  { from: /Tiefstufe/g, to: 'ниска степен' },
  { from: /Dehnstufe/g, to: 'удължена степен' },
  { from: /Bindevokal/g, to: 'съединителна гласна' },
  { from: /Vollstufe/g, to: 'пълна степен' },
  { from: /Reduplikation/g, to: 'редупликация' },
  { from: /Augment/g, to: 'аугмент' },

  // Boilerplate and structure
  { from: /Inhaltsverzeichnis/g, to: 'Съдържание' },
  { from: /Wortliste/g, to: 'Речник (Списък с думи)' },
  { from: /Übung/g, to: 'Упражнение' },
  { from: /Übersetzungsübung/g, to: 'Упражнение за превод' },
  { from: /Wiederholungsübung/g, to: 'Упражнение за преговор' },
  { from: /Wochenspruch/g, to: 'Стихотворение за седмицата' },
  { from: /Abbildung/g, to: 'Фигура' },
  { from: /Quelle/g, to: 'Източник' },
  { from: /Bildquelle/g, to: 'Източник на изображението' },
  { from: /Lizenz/g, to: 'Лиценз' },
  { from: /Urheberrecht/g, to: 'Авторско право' },
  { from: /Impressum/g, to: 'Импресуум' },
  { from: /Zitierweise/g, to: 'Начин на цитиране' },

  // Phrases
  { from: /zu den bisher gelernten/g, to: 'към научените досега' },
  { from: /am Ende von/g, to: 'в края на' },
  { from: /im engeren Sinn/g, to: 'в тесен смисъл' },
  { from: /mit einem/g, to: 'с един' },
  { from: /ohne besonderes/g, to: 'без специален' },
  { from: /auslautender/g, to: 'краен' },
  { from: /anlautender/g, to: 'начален' },
  { from: /vokalisch/g, to: 'вокален (гласен)' },
  { from: /konsonantisch/g, to: 'консонантен (съгласен)' },
  { from: /thematischer/g, to: 'тематичен' },
  { from: /athematischer/g, to: 'атематичен' },
  { from: /starker/g, to: 'силен' },
  { from: /schwacher/g, to: 'слаб' },
];

const files = fs.readdirSync(bgDir).filter(f => f.endsWith('.md'));

for (const file of files) {
    let content = fs.readFileSync(path.join(bgDir, file), 'utf8');
    let originalContent = content;

    for (const r of replacements) {
        content = content.replace(r.from, r.to);
    }

    if (content !== originalContent) {
        fs.writeFileSync(path.join(bgDir, file), content);
        console.log(`Updated ${file}`);
    }
}

console.log('Final bulk cleanup complete.');
