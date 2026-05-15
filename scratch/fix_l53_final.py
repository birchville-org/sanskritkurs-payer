import sys
import re

def fix_l53(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Wrap 53.1 in grammar-box
    content = re.sub(
        r'(## 53\.1\. Der Dual \(द्विवचन n\.\) der Nomina\n\n)(.*?)(?=\n\n::: media)',
        r'\1::: grammar-box\n\2\n:::',
        content,
        flags=re.DOTALL
    )

    # 2. Fix सुमनस्, हविस्, दीर्धायुस् tables
    content = content.replace(
        '> |   | Maskulininum/Femininum  \n> पुंस्/स्त्री | Neutrum  \n> नपुंसक |\n> | --- | --- | --- |\n> | प्रथमा, द्वितीया, आमन्त्रितम् | सुमनसौ | सुमनसी |\n> | तृतीया, चतुर्थी, पञ्चमी | सुमनोभ्याम् |\n> | सष्ठी, सप्तमी | सुमनसोस् |',
        '::: grammar-box\n|   | Maskulininum/Femininum (पुंस्/स्त्री) | Neutrum (नपुंसक) |\n| --- | --- | --- |\n| प्रथमा, द्वितीया, आमन्त्रितम् | सुमनसौ | सुमनसी |\n| तृतीया, चतुर्थी, पञ्चमी | सुमनोभ्याम् | |\n| सष्ठी, सप्तमी | सुमनसोस् | |\n:::'
    )

    content = content.replace(
        '> |   | Neutrum  \n> नपुंसक |\n> | --- | --- |\n> | प्रथमा, द्वितीया, आमन्त्रितम् | हविषी |\n> | तृतीया, चतुर्थी, पञ्चमी | हविर्भ्याम् |\n> | सष्ठी, सप्तमी | हविषोस् |',
        '::: grammar-box\n|   | Neutrum (नपुंसक) |\n| --- | --- |\n| प्रथमा, द्वितीया, आमन्त्रितम् | हविषी |\n| तृतीया, चतुर्थी, पञ्चमी | हविर्भ्याम् |\n| सष्ठी, सप्तमी | हविषोस् |\n:::'
    )

    content = content.replace(
        '> |   | Maskulininum/Femininum  \n> पुंस्/स्त्री | Neutrum  \n> नपुंसक |\n> | --- | --- | --- |\n> | प्रथमा, द्वितीया, आमन्त्रितम् | दीर्घायुषौ | दीर्घायुषी |\n> | तृतीया, चतुर्थी, पञ्चमी | दीर्घायुर्भ्याम् |\n> | सष्ठी, सप्तमी | दीर्घायुषोस् |',
        '::: grammar-box\n|   | Maskulininum/Femininum (पुंस्/स्त्री) | Neutrum (नपुंसक) |\n| --- | --- | --- |\n| प्रथमा, द्वितीया, आमन्त्रितम् | दीर्घायुषौ | दीर्घायुषी |\n| तृतीया, चतुर्थी, पञ्चमी | दीर्घायुर्भ्याम् | |\n| सष्ठी, सप्तमी | दीर्घायुषोस् | |\n:::'
    )

    # 3. Fix Devanagari typos
    content = content.replace('| **6., 7.** | सीम्noस् |', '| **6., 7.** | सीम्नोस् |')
    content = content.replace('| **3., 4., 5.** | अग्निभ्याम् | मतिभ्याम् | वारiभ्याम् |', '| **3., 4., 5.** | अग्निभ्याम् | मतिभ्याम् | वारिभ्याम् |')
    content = content.replace('| **3., 4., 5.** | शत्रुभ्याम् | धेnuभ्याम् | मधुभ्याम् |', '| **3., 4., 5.** | शत्रुभ्याम् | धेनुभ्याम् | मधुभ्याम् |')

    # 4. Fix Steigerung tables (The ones causing errors)
    steigerung_old = r'\| Wurzel \| Adjektiv \| Komparativ \| Superlativ \|\n\| --- \| --- \| --- \| --- \|\n\| क्षिप् 6P "werfen" \| क्षिप्र 3 "schnell \| क्षेपीयस् 3 "schneller"  \nक्षिप्रतर 3 \| क्षेपिष्ठ 3 "am schnellsten"  \nक्षिप्रतम 3 \|\n\| स्था 1P "stehen" \| स्थिर 3 "beständig, fest" \| स्थेयस् 3 "fester"  \nस्थिरतर 3 \| स्थेष्ठ 3 "am festesten"  \nस्थिरतम 3 \|'
    steigerung_new = '::: grammar-box\n| Wurzel | Adjektiv | Komparativ | Superlativ |\n| --- | --- | --- | --- |\n| क्षिप् 6P "werfen" | क्षिप्र 3 "schnell" | क्षेपीयस् 3 "schneller" [[br]] क्षिप्रतर 3 | क्षेपिष्ठ 3 "am schnellsten" [[br]] क्षिप्रतम 3 |\n| स्था 1P "stehen" | स्थिर 3 "beständig, fest" | स्थेयस् 3 "fester" [[br]] स्थिरतर 3 | स्थेष्ठ 3 "am festesten" [[br]] स्थिरतम 3 |\n:::'
    content = re.sub(steigerung_old, steigerung_new, content)

    # 5. Fix Verzeichnis table
    verzeichnis_old = r'> \| Adjektiv \| Komparativ \| Superlativ \|\n> \| --- \| --- \| --- \|\n> \| अल्प 3 "klein, wenig" \| अल्पीयस् \| अल्पिष्ठ \|\n> \| क्षिप्र 3 "schnell"  \n> \(zu क्षिप्\) \| क्षेपीयस् \| क्षेपिष्ठ \|\n> \| गुरु 3 "schwer"  \n> \(zu \*गृ\) \| गरीयस् \| गरिष्ठ \|\n> \| दीर्घ 3 "lang"  \n> \(zu \*दृघ्\) \| द्राघीयस् \| d्राघिष्ठ \|\n> \| दूर 3 "fern"  \n> \(zu \*दु/\*दू\) \| दवीयस् \| दविष्ठ \|\n> \| धनवन्त् 3 "reich" \| धनीयस् \| धनिष्ठ \|\n> \| पाप 3 "böse" \| पापीयस् \| पापिष्ठ \|\n> \| पृथु 3 "breit" \| प्रथीयस् \| प्रथीष्ठ \|\n> \| प्रिय 3 "lieb" \| प्रेयस् \| प्रेष्ठ \|\n> \| बलिन् 3 "\(besonders\) stark" \| बलीयस् \| बलिष्ठ \|\n> \| महान्त् 3 "groß" \| महीयस् \| महिष्ठ \|\n> \| युवन् 3 "jung" \| यवीयस् \| यविष्ठ \|\n> \| स्थिर 3 "fest"  \n> \(zu स्था\) \| स्थेयस् \| स्थेष्ठ \|\n> \| ह्रस्व 3 "kurz" \| ह्रसीयस् \| ह्रसिष्ठ \|'
    verzeichnis_new = '::: grammar-box\n| Adjektiv | Komparativ | Superlativ |\n| --- | --- | --- |\n| अल्प 3 "klein, wenig" | अल्पीयस् | अल्पिष्ठ |\n| क्षिप्र 3 "schnell" [[br]] (zu क्षिप्) | क्षेपीयस् | क्षेपिष्ठ |\n| गुरु 3 "schwer" [[br]] (zu *गृ) | गरीयस् | गरिष्ठ |\n| दीर्घ 3 "lang" [[br]] (zu *दृघ्) | द्राघीयस् | द्राघिष्ठ |\n| दूर 3 "fern" [[br]] (zu *दु/*दू) | दवीयस् | दविष्ठ |\n| धनवन्त् 3 "reich" | धनीयस् | धनिष्ठ |\n| पाप 3 "böse" | पापीयस् | पापिष्ठ |\n| पृथु 3 "breit" | प्रथीयस् | प्रथीष्ठ |\n| प्रिय 3 "lieb" | प्रेयस् | प्रेष्ठ |\n| बलिन् 3 "(besonders) stark" | बलीयस् | बलिष्ठ |\n| महान्त् 3 "groß" | महीयस् | महिष्ठ |\n| युवन् 3 "jung" | यवीयस् | यविष्ठ |\n| स्थिर 3 "fest" [[br]] (zu स्था) | स्थेयस् | स्थेष्ठ |\n| ह्रस्व 3 "kurz" | ह्रसीयस् | ह्रसिष्ठ |\n:::'
    content = re.sub(verzeichnis_old, verzeichnis_new, content)

    # 6. Fix Defektiv table
    defektiv_old = r'> \| \(Adjektiv\) \| Komparativ \| Superlativ \|\n> \| --- \| --- \| --- \|\n> \| \(अल्प 3 "klein, wenig"\) \| कनीयस्  \n> vgl\.  कन्या f\. "Mädchen = die Kleine" \| कनिष्ठ \|\n> \| \(प्रशस्य 3 "lobenswert, gut"\) \| श्रेयस्  \n> zu श्री f\. "Glanz" \| श्रेष्ठ \|\n> \| \(प्रशस्य 3 "lobenswert, gut"\) \| ज्यायस्  \n> auch: "älter"  \n> zu ज्या f\. "Übergewalt" \| ज्येष्ठ  \n> auch: "am ältesten" \|\n> \| \(बहु 3 "viel"\) \| भूयस् \| भूयिष्ठ \|\n> \| \(वृद्ध 3 "alt"\) \| वर्षीयस्  \n> zu वर्ष n\.m\. "Regenzeit, Jahr" \| वर्षiष्ठ \|\n> \| \(वृद्ध 3 "alt"\) \| ज्यायस्  \n> auch: "besser"  \n> zu ज्या f\. "Übergewalt" \| ज्येष्ठ  \n> auch: "bester" \|'
    defektiv_new = '::: grammar-box\n| (Adjektiv) | Komparativ | Superlativ |\n| --- | --- | --- |\n| (अल्प 3 "klein, wenig") | कनीयस् [[br]] vgl. कन्या f. "Mädchen = die Kleine" | कनिष्ठ |\n| (प्रशस्य 3 "lobenswert, gut") | श्रेयस् [[br]] zu श्री f. "Glanz" | श्रेष्ठ |\n| (प्रशस्य 3 "lobenswert, gut") | ज्यायस् [[br]] auch: "älter" [[br]] zu ज्या f. "Übergewalt" | ज्येष्ठ [[br]] auch: "am ältesten" |\n| (बहु 3 "viel") | भूयस् | भूयिष्ठ |\n| (वृद्ध 3 "alt") | वर्षीयस् [[br]] zu वर्ष n.m. "Regenzeit, Jahr" | वर्षिष्ठ |\n| (वृद्ध 3 "alt") | ज्यायस् [[br]] auch: "besser" [[br]] zu ज्या f. "Übergewalt" | ज्येष्ठ [[br]] auch: "bester" |\n:::'
    content = re.sub(defektiv_old, defektiv_new, content)

    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)

if __name__ == "__main__":
    fix_l53(sys.argv[1])
