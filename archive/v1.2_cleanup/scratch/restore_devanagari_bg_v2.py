import sys

de_path = "/Volumes/SanDisk1TB/proj/Payer/docs/lektionen/wortliste.md"
bg_path = "/Volumes/SanDisk1TB/proj/Payer/docs/bg/lektionen/wortliste.md"

with open(de_path, "r", encoding="utf-8") as f:
    de_lines = f.readlines()

with open(bg_path, "r", encoding="utf-8") as f:
    bg_lines = f.readlines()

# Extract Lesson 12 table and Lesson 13 from German
# Lesson 12 table starts around 584
# Lesson 13 starts around 731

de_table_start = 583 # 0-indexed index for line 584
de_lesson13_start = 730 # 0-indexed index for line 731
# We'll take until Lesson 14 starts around 801
de_lesson14_start = 800 # 0-indexed index for line 801

table_part = de_lines[de_table_start:de_lesson13_start]
lesson13_part = de_lines[de_lesson13_start:de_lesson14_start]

# Translate headers in table_part
table_part[0] = "### 12.5.1. Пасив и PPP на научените до момента корени\n"
table_part[2] = "> | Корен | Пасив Сегашно  \n"
table_part[3] = "> 3 л. ед. ч. Индикатив | PPP |\n"

# Translate Lesson 13 content while preserving Sanskrit
lesson13_text = "".join(lesson13_part)

# Selective translations (preserving Sanskrit/IAST/Devanagari)
lesson13_text = lesson13_text.replace("## Lektion 13", "## Урок 13")
lesson13_text = lesson13_text.replace("hebt das vorhergehende Wort hervor; entspricht oft dem emphatischen Tonfall im Deutschen; wird zuweilen nicht übersetzt, sondern dient als eine Art \"Smiley\".", "подчертава предходната дума; често съответства на емфатичното ударение в българския; понякога не се превежда, а служи като вид „емотикон“.")
lesson13_text = lesson13_text.replace("Asura, Dämon", "асура, демон")
lesson13_text = lesson13_text.replace("„**ASURA**. `Geistig, göttlich.'", "„**АСУРА**. ‚Духовен, божествен.‘")
# ... and so on. To be safe, I'll do the same translations I had before but carefully.

# Actually, I have the translated Bulgarian text for Lesson 13 ready. 
# I just need to make sure the Sanskrit parts match exactly.

# I'll just manually assemble it in the script to be 100% sure.
bg_lesson13 = """
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

pad 4 Ā (padyate), Pass.: padyate, PPP panna पद् पद्यते पद्यते पन्न : отивам, попадам в

as 2 P (asti) अस् अस्ति : съм, съществувам (тук е)

as 4 P (asyati), Pass.: asyate, PPP asta अस् अस्यти अस्यте аст : хвърлям, запращам
# Wait! I am doing it again! I'll just use the German Sanskrit strings.
"""

# NEW STRATEGY: 
# Replace German words with Bulgarian words in the German source lines.

def translate_line(line):
    # This is a very simple mapping for the wordlist lines
    line = line.replace("sein, da sein", "съм, съществувам (тук е)")
    line = line.replace("schleudern, (weg-)werfen", "хвърлям, запращам")
    line = line.replace("gehen, geraten in", "отивам, попадам в")
    line = line.replace("gehen", "отивам")
    line = line.replace("schützen, behüten", "пазя, закрилям")
    line = line.replace("trinken", "пия")
    line = line.replace("hassen, anfeinden", "мразя, враждувам")
    line = line.replace("essen, verzehren", "ям, поглъщам")
    line = line.replace("Speise (aus PPP: *ad-na: das Gegessene, das Essen)", "храна (от PPP: *ad-na: изяденото, яденето)")
    line = line.replace("Abb.:", "**Фигура:**")
    line = line.replace("Bildquelle:", "Източник:")
    line = line.replace("Wortbildung:", "Словообразуване:")
    line = line.replace("Schritt, Standort, Stätte", "стъпка, местоположение, място (обиталище)")
    line = line.replace("Fuß, ein Viertel (da viele Tiere 4 Füße haben), Verszeile (die meisten Verse bestehen aus vier Pādas)", "крак, стъпало; четвърт (тъй като много животни имат 4 крака), стих (повечето строфи се състоят от четири пади)")
    line = line.replace("Hass", "омраза")
    line = line.replace("Anm.: die Konjugation der 2. Präsensklasse folgt später.", "Забележка: спрежението на 2-ри сегашен клас следва по-късно.")
    return line

translated_lesson13 = [translate_line(l) for l in lesson13_part]

# Assemble final
header_idx = -1
for i, line in enumerate(bg_lines):
    if "### 12.5.1. Пасив и PPP" in line:
        header_idx = i
        break

if header_idx != -1:
    final_bg_lines = bg_lines[:header_idx] + table_part + translated_lesson13
    with open(bg_path, "w", encoding="utf-8") as f:
        f.writelines(final_bg_lines)
else:
    print("Header not found")
