import glob, re, os

translations = {
    "Wortliste": "词汇表",
    "Übung": "练习",
    "Leseverstehen und Übersetzungsübung": "阅读理解与翻译练习",
    "Fragepronomen": "疑问代词",
    "Demonstrativpronomina": "指示代词",
    "Sechste Präsensklasse": "第六类现在时",
    "Vierte Präsensklasse": "第四类现在时",
    "Fünfte Präsensklasse": "第五类现在时",
    "Achte Präsensklasse": "第八类现在时",
    "Siebte Präsensklasse": "第七类现在时",
    "Neunte Präsensklasse": "第九类现在时",
    "Passiv": "被动语态",
    "Verwendung des Parasmaipada": "Parasmaipada的使用",
    "und Ātmanepada": "与Ātmanepada",
    "im Kausativum": "在使役动词中",
    "Komposita vom Typ": "此类型的复合词",
    "Zur Nominalbildung: ⟪तद्धित⟫-Suffix": "关于名词构成：⟪तद्धित⟫后缀",
    "Das Neutrum": "中性",
    "Der Infinitiv": "不定式",
    "Endungen": "词尾",
    "Perfekt Typ III: Starker Stamm Hochstufe/Dehnstufe": "第三类完成时：强词干 强化/长音",
    "Perfekt Typ IIIa: Starker Stamm Hochstufe/Dehnstufe, schwacher Stamm Tiefstufe": "第三类完成时a：强词干 强化/长音，弱词干 弱化",
    "Das Adverb": "副词",
    "Akkusativ": "宾格",
    "Adverbiale Komposita": "副词性复合词",
    "Adverbial verwendeter": "作副词使用的",
    "Wortfragen (Ergänzungsfragen)": "疑问句（补充疑问）",
    "Grundzahlen": "基数词",
    "Ordinalzahlen": "序数词",
    "Zahladverbien": "数字副词",
    "Nominativ Singular auf -s": "以-s结尾的单数主格",
    "Nominativ Plural Maskulinum und Femininum": "阳性与阴性的复数主格",
    "Vokalsandhi": "元音连声",
    "Unregelmäßige Steigerung": "不规则比较级",
    "Der Nominativ Singular": "单数主格",
    "Sandhi": "连声",
    "Wörterverzeichnis": "词汇表",
    "Partizip Perfekt Passiv (PPP)": "被动完成分词 (PPP)",
    "Schema II für intransitive Verben und Verben der Bewegung": "不及物动词与移动动词的模式II",
    "Aorist 4: s-Aorist": "第四不定过去式：s-不定过去式",
    "Der Imperativ": "命令式",
    "Der Dual": "双数",
    "der Nomina": "名词的"
}

def translate_line(line):
    # Special exact matches or substring replacements
    if "Wortliste" in line: line = line.replace("Wortliste", "词汇表")
    if "Übung" in line and "Übungs" not in line: line = line.replace("Übung", "练习")
    if "Leseverstehen und Übersetzungsübung" in line: line = line.replace("Leseverstehen und Übersetzungsübung", "阅读理解与翻译练习")
    if "Fragepronomen" in line: line = line.replace("Fragepronomen", "疑问代词")
    if "Demonstrativpronomina" in line: line = line.replace("Demonstrativpronomina", "指示代词")
    if "Sechste Präsensklasse" in line: line = line.replace("Sechste Präsensklasse", "第六类现在时")
    if "Vierte Präsensklasse" in line: line = line.replace("Vierte Präsensklasse", "第四类现在时")
    if "Passiv (Suffix" in line: line = line.replace("Passiv (Suffix", "被动语态 (后缀")
    if "Fünfte Präsensklasse" in line: line = line.replace("Fünfte Präsensklasse", "第五类现在时")
    if "Achte Präsensklasse" in line: line = line.replace("Achte Präsensklasse", "第八类现在时")
    if "Siebte Präsensklasse" in line: line = line.replace("Siebte Präsensklasse", "第七类现在时")
    if "Neunte Präsensklasse" in line: line = line.replace("Neunte Präsensklasse", "第九类现在时")
    
    if "Verwendung des Parasmaipada" in line:
        line = line.replace("Verwendung des Parasmaipada", "Parasmaipada 的使用").replace("und Ātmanepada", "以及 Ātmanepada").replace("im Kausativum", "在使役动词中")
    
    if "Komposita vom Typ" in line: line = line.replace("Komposita vom Typ", "此类型的复合词")
    if "Zur Nominalbildung: ⟪तद्धित⟫-Suffix -in" in line: line = line.replace("Zur Nominalbildung: ⟪तद्धित⟫-Suffix -in", "关于名词构成：⟪तद्धित⟫-后缀 -in")
    if "Das Neutrum (napuṃsaka n. = ⟪नपुंसक⟫)" in line: line = line.replace("Das Neutrum", "中性")
    if "Der Infinitiv" in line: line = line.replace("Der Infinitiv", "不定式")
    if "Endungen" in line: line = line.replace("Endungen", "词尾")
    
    if "Perfekt Typ IIIa" in line:
        line = line.replace("Perfekt Typ IIIa: Starker Stamm Hochstufe/Dehnstufe, schwacher Stamm Tiefstufe", "第三类完成时a：强词干 强化/长音，弱词干 弱化")
    elif "Perfekt Typ III" in line:
        line = line.replace("Perfekt Typ III: Starker Stamm Hochstufe/Dehnstufe", "第三类完成时：强词干 强化/长音")
        
    if "Das Adverb" in line: line = line.replace("Das Adverb", "副词")
    if "Akkusativ" in line: line = line.replace("Akkusativ", "宾格")
    if "Adverbiale Komposita" in line: line = line.replace("Adverbiale Komposita", "副词性复合词")
    if "Adverbial verwendeter" in line: line = line.replace("Adverbial verwendeter", "作副词使用的")
    if "Komposita" in line and "Adverbiale" not in line and "Kopulative" not in line: line = line.replace("Komposita", "复合词")
    
    if "Wortfragen (Ergänzungsfragen)" in line: line = line.replace("Wortfragen (Ergänzungsfragen)", "疑问句（补充疑问）")
    if "Grundzahlen" in line: line = line.replace("Grundzahlen", "基数词")
    if "Ordinalzahlen" in line: line = line.replace("Ordinalzahlen", "序数词")
    if "Zahladverbien" in line: line = line.replace("Zahladverbien", "数字副词")
    
    if "Nominativ Singular auf -s" in line: line = line.replace("Nominativ Singular auf -s", "以 -s 结尾的单数主格")
    if "Nominativ Plural Maskulinum und Femininum" in line: line = line.replace("Nominativ Plural Maskulinum und Femininum", "阳性与阴性的复数主格")
    if "Vokalsandhi" in line: line = line.replace("Vokalsandhi", "元音连声")
    if "Unregelmäßige Steigerung" in line: line = line.replace("Unregelmäßige Steigerung", "不规则比较级")
    
    if "Der Nominativ Singular" in line: line = line.replace("Der Nominativ Singular", "单数主格")
    if "Sandhi" in line: line = line.replace("Sandhi", "连声")
    if "Wörterverzeichnis" in line: line = line.replace("Wörterverzeichnis", "词汇表")
    if "Partizip Perfekt Passiv (PPP)" in line: line = line.replace("Partizip Perfekt Passiv (PPP)", "被动完成分词 (PPP)")
    if "Schema II für intransitive Verben und Verben der Bewegung" in line: line = line.replace("Schema II für intransitive Verben und Verben der Bewegung", "不及物动词与移动动词的模式II")
    if "PPP auf -ta" in line: line = line.replace("PPP auf -ta", "以 -ta 结尾的PPP")
    
    if "Aorist 4: s-Aorist" in line: line = line.replace("Aorist 4: s-Aorist", "第四不定过去式：s-不定过去式")
    if "iṣ-Aorist" in line: line = line.replace("iṣ-Aorist", "iṣ-不定过去式")
    if "Der Imperativ" in line: line = line.replace("Der Imperativ", "命令式")
    if "Der Dual" in line and "der Nomina" in line: line = line.replace("Der Dual", "双数").replace("der Nomina", "名词的")
    
    # ⟪...⟫ prefixes that are raw rules
    if "⟪१⟫. ⟪मनुस्मृति⟫" in line: return line
    if "⟪महाभारत⟫" in line: return line
    if "⟪योगसूत्र⟫" in line: return line
    if "⟪कौटिलीयार्थशास्त्र⟫" in line: return line
    if "⟪अ⟫" in line and len(line) < 15: return line # Glossar headings

    return line

files = glob.glob("docs/zh-CN/lektionen/*.md")
for f in files:
    with open(f, 'r', encoding='utf-8') as file:
        lines = file.readlines()
        
    changed = False
    for i, line in enumerate(lines):
        if line.startswith('#') and not re.search(r'[\u4e00-\u9fff]', line):
            # Check if it contains DE words
            if re.search(r'[a-zA-Z]', line) and "⟪" in line or not "⟪" in line:
                new_line = translate_line(line)
                if new_line != line:
                    lines[i] = new_line
                    changed = True
                    print(f"Changed in {f}: {line.strip()} -> {new_line.strip()}")
                    
    if changed:
        with open(f, 'w', encoding='utf-8') as file:
            file.writelines(lines)
