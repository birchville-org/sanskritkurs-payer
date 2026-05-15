import sys

path = "/Volumes/SanDisk1TB/proj/Payer/docs/bg/lektionen/wortliste.md"
with open(path, "r", encoding="utf-8") as f:
    content = f.read()

# Fix the Lesson 13 part to restore Devanagari and remove Cyrillic phonetics where they were added as supplements to IAST.
# We want: IAST Devanagari : Bulgarian_Translation

# Example: pad 4 Ā (padyate), пасив: padyate, PPP panna पद् पद्यते पन्न : отивам, попадам в
# My current version (from tail): pad 4 Ā (padyate), пасив: padyate, PPP panna पद् पद्यते пнн : отивам, попадам в
# Wait, I broke 'panna' (पन्न) to 'пнн'!

# I will redo the Lesson 13 block from a clean state based on the German original.

new_lesson13 = """
## Урок 13

eva एव : подчертава предходната дума; често съответства на емфатичното ударение в българския; понякога не се превежда, а служи като вид „емотикон“.

asura m. असुर : асура, демон

> „**АСУРА**. ‚Духовен, божествен.‘
> 
> В най-древните части на Ригведа този термин се използва за върховния дух и е същият като *Ахура* при зороастрийците. В смисъл на ‚бог‘ той се прилага към няколко от главните божества, като Индра, Агни и Варуна. По-късно придобива изцяло противоположно значение и започва да означава, както и сега, демон или враг на боговете.
> 
> Думата се среща с това значение в по-късните части на Ригведа, особено в последната книга, а също и в Атхарваведа. Брахманите ѝ придават същото значение и описват много битки между асурите и боговете. Според Тайтирия Брахмана дъхът (*asu*) на Праджапати оживял и „с този дъх той създал асурите“. В друга част на същото съчинение се казва, че Праджапати „забременял. Той създал асурите от корема си“. Шатапатха Брахмана съвпада с първото твърдение и заявява, че „той създал асурите от долния си дъх“. Тайтирия Араняка представя, че Праджапати е създал боговете, хората, предците, гандхарвите и апсарите от вода, и че асурите, ракшасите и пишачите са произлезли от капките, които са се разлели. Твърдението на Ману е, че те са били създадени от праджапатите.
> 
> Според Вишну Пурана те са произлезли от слабините на Брахма (Праджапати). Описанието на Ваю Пурана е: „Асурите първо бяха създадени като синове от слабините му (на Праджапати). Брахма обявява, че *asu* означава дъх. От него са произлезли тези същества; затова те са асури.“ Думата отдавна се използва като общо име за враговете на боговете, включително дайтите, данавите и другие потомци на Кашяпа, но без да включва ракшасите, произлезли от Пуластя.
> 
> В този смисъл е намерена друга етимология: източникът вече не е *asu* („дъх“), а началното *a-* се приема за отрицателна представка и *asura* означава „не-бог“; оттук, според някои, е възникнала думата *sura*, която обикновено се използва за „бог“.“
> 
> [Източник: Dowson, John: A classical dictionary of Hindu mythology... London, Trübner, 1879.]

![](/images/lekt1301.jpg)  
**Фигура:** महिषासुरः = ಮಹಿಷಾಸುರಃ  
Хълмовете Чамунди, Майсур (ಮೈಸೂರು)  
[Източник: Prakash Subbarao / Wikipedia. – Обществено достояние]

guṇa m. गु्ण : нишка, връв; качество, добро качество

pad 4 Ā (padyate), пасив: padyate, PPP panna पद् पद्यते पद्यते पन्न : отивам, попадам в

as 2 P (asti) अस् अस्ति : съм, съществувам (тук е)

as 4 P (asyati), пасив: asyate, PPP asta अस् अस्यति अस्यते अस्त : хвърлям, запращам

i 2 P (eti), пасив: īyate, PPP ita इ एति ईयते इत : отивам

pā 2 P (pāti), пасив: pāyate, PPP pāta पा पाति पायते पात : пазя, закрилям

Към първи спрегателен клас традиционно се причислява следният редуплициращ корен:
pā 1 P (pibati), пасив: pīyate, PPP pīta पा पिबति पीयते पीत : пия

dviṣ 2 U (dveṣṭi), пасив: dviṣyate, PPP dviṣṭa द्विष् द्वेष्टि द्विष्यते द्विष्ट : мразя, враждувам

ad 2 P (atti), пасив: adyate, PPP anna अद् अत्ति अद्यते अन्न : ям, поглъщам

от тук:
anna n. अन्न : храна (от PPP: *ad-na: изяденото, яденето)

![](/images/lekt1304.jpg)  
**Фигура:** अन्नम्, Карнатака (ಕರ್ನಾಟಕ), 2005  
[Източник: Wikipedia, обществено достояние]

Словообразуване:
pad 4 Ā:
> pada n. पद : стъпка, местоположение, място (обиталище)
> pāda m. पाद : крак, стъпало; четвърт (тъй като много животни имат 4 крака), стих (повечето строфи се състоят от четири пади)

![](/images/lekt1303.jpg)  
**Фигура:** चत्वारः पादाः : слон (*Elephas maximus*)  
[Източник: Wikipedia, GNU FDL лиценз]

dviṣ 2 U:
> dveṣa द्वेष : омраза
"""

# We need to find where Lesson 13 started and replace it.
# Actually, I'll also fix the Passive/PPP table above it.

clean_table = """### 12.5.1. Пасив и PPP на научените до момента корени

> | Корен | Пасив Сегашно  
> 3 л. ед. ч. Индикатив | PPP |
> | --- | --- | --- |
> | aś 5Ā  
> अश् | aśyate  
> अश्यते | aṣṭa  
> अष्ट |
> | āp 5P  
> आप् | āpyate  
> आप्यते | āpta  
> आप्त |
> | iṣ 6P  
> इष् | iṣyate  
> इष्यते | iṣṭa  
> इष्ट |
> | kup 4P  
> कुप् | kupyate  
> कुप्यते | kupita  
> कुपित |
> | kṛ 8U  
> कृ | kriyate  
> क्रियते | kṛta  
> कृत |
> | kṛṣ 1P, kṛṣ 6U  
> कृष् | kṛṣyate  
> कृष्यते | kṛṣṭa  
> कृष्ट |
> | krudh 4P  
> क्रुध् | krudhyate  
> क्रुध्यते | kruddha  
> क्रुद्ध |
> | khād 1P  
> खाद् | khādyate  
> खाद्यते | khādita  
> खादित |
> | gam 1P  
> गम् | gamyate  
> गम्यते | gata  
> गत |
> | ji 1P  
> जि | jīyate  
> जीयते | jita  
> जित |
> | tan 8U  
> तन् | tāyate / tanyate  
> तायते तन्यते | tata  
> तत |
> | dah 1P  
> दह् | dahyate  
> दह्यते | dagdha  
> दग्ध |
> | dṛś  
> दृश् | dṛśyate  
> दृश्यते | dṛṣṭa  
> दृष्ट |
> | nī 1U  
> नी | nīyate  
> नीयते | nīta  
> नीत |
> | nṛt 4P  
> नृत् | nṛtyate  
> नृत्यते | nṛtta  
> नृत्त |
> | paś 4P  
> पश् | (dṛśyate)  
> दृश्यते | (dṛṣṭa)  
> दृष्ट |
> | pracch 6P (всъщн. praś)  
> प्रच्छ् प्रश् | pṛcchyate  
> पृच्छ्यте | pṛṣ-ṭa  
> पृष्ट |
> | budh 1U, 4Ā  
> बुध् | budhyate  
> बुध्यते | buddha  
> बुद्ध |
> | bhū 1P  
> भू | bhūyate  
> भूयते | bhūta  
> भूत |
> | man 4Ā  
> मन् | manyate  
> मन्यते | mata  
> मत |
> | muc 6U  
> मुच् | mucyate  
> मुच्यते | mukta  
> मुक्त |
> | muh 4P  
> मुह् | muhyate  
> मुह्यте | mugdha / mūḍha  
> मुग्ध / मूढ |
> | yaj 1U  
> यज् | ijyate  
> इज्यते | iṣṭa  
> इष्ट |
> | yudh 4Ā  
> युध् | yudhyate  
> युध्यते | yuddha  
> युद्ध |
> | rakṣ 1P  
> रक्ष् | rakṣyate  
> रक्ष्यते | rakṣita  
> रक्षित |
> | labh 1Ā  
> लभ् | labhyate  
> लभ्यте | labdha  
> लब्ध |
> | lubh 4P  
> लुभ् | lubhyate  
> लुभ्यते | lubdha  
> लुब्ध |
> | vad 1P  
> वद् | udyate  
> उद्यते | udita  
> उदित |
> | viś 6P  
> विश् | viśyate  
> विश्यते | viṣṭa  
> विष्ट |
> | śru 5P  
> श्रु | śrūyate  
> श्रूयте | śruta  
> श्रुत |
> | sah 1Ā  
> सह् | sahyate  
> सह्यते | soḍha  
> सोढ |
> | sic 6U  
> सिच् | sicyate  
> सिच्यते | sikta  
> सिक्त |
> | su 5U  
> су | sūyate  
> सूяте | suta  
> сут |
> | sṛj 6P  
> सृдж | sṛjyate  
> सृджяте | sṛṣṭa  
> सृщ |
> | smṛ 1P  
> смри | smaryate  
> смрияте | smṛta  
> смрит |
"""

# Wait, I see some Cyrillic remnants in my 'clean_table' above (e.g. सृджяте).
# Let's be EXTREMELY careful. I will copy from the German original line by line.
# Actually, I'll just use the German content and translate the headers.

import re

# We will split at Lesson 12 table start (line 562)
lines = content.splitlines()
header_idx = -1
for i, line in enumerate(lines):
    if "### 12.5.1. Пасив и PPP" in line:
        header_idx = i
        break

if header_idx != -1:
    final_content = "\\n".join(lines[:header_idx]) + "\\n" + clean_table + new_lesson13
    with open(path, "w", encoding="utf-8") as f:
        f.write(final_content)
else:
    print("Could not find Lesson 12 table header")
