import sys

file_path = 'docs/lektionen/lektion27.md'
with open(file_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

def fix_27_2_1(lines):
    new_table = [
        "### 27.2.1. Konsonatische Stämme\n",
        "\n",
        "::: grammar-box\n",
        "| Stamm | Lokativ Singular | Lokativ Plural |\n",
        "| :--- | :--- | :--- |\n",
        "| यजन्त् | यजति (yaj-at-i) | यजत्सु |\n",
        "| महान्त् | महति | महत्सु |\n",
        "| पशुमन्त् | पशुमति | पशुमत्सु |\n",
        "| गुणवन्त् | गुणवति | गुणवत्सु |\n",
        ":::\n"
    ]
    start = -1
    end = -1
    for i, line in enumerate(lines):
        if "### 27.2.1. Konsonatische Stämme" in line:
            start = i
        if start != -1 and i > start and "### 27.2.2" in line:
            end = i - 1
            break
    if start != -1 and end != -1:
        lines[start:end+1] = new_table
    return lines

def fix_27_2_3(lines):
    new_table = [
        "### 27.2.3. Vokalische Stämme\n",
        "\n",
        "::: grammar-box\n",
        "| Stamm | Lokativ Singular | Lokativ Plural |\n",
        "| :--- | :--- | :--- |\n",
        "| देव m. | देवे (deva + -i) | देवेषु |\n",
        "| कवि m. | कवौ | कविषु |\n",
        "| पशु m. | पशौ | पशुषु |\n",
        "| देवता f. | देवतायाम् | देवतासु |\n",
        "| देवी f. | देव्याम् | देवीषु |\n",
        "| श्रुति f. | श्रुतौ oder श्रुत्याम् (d.h. wie कवि oder देवी) | श्रुतिषु |\n",
        "| धेनु f. | धेनौ oder धेन्वाम् | धेनुषु |\n",
        ":::\n"
    ]
    start = -1
    end = -1
    for i, line in enumerate(lines):
        if "### 27.2.3. Vokalische Stämme" in line:
            start = i
        if start != -1 and i > start and "## 27.3" in line:
            end = i - 1
            break
    if start != -1 and end != -1:
        lines[start:end+1] = new_table
    return lines

lines = fix_27_2_1(lines)
lines = fix_27_2_3(lines)

with open(file_path, 'w', encoding='utf-8') as f:
    f.writelines(lines)
