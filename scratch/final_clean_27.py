import sys
import re

file_path = 'docs/lektionen/lektion27.md'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Replace non-breaking spaces
content = content.replace('\u00a0', ' ')

def fix_3col_table(title, stem, data):
    table = [
        f"### {title}\n",
        "\n",
        "::: grammar-box\n",
        "| Kasus | Singular (एकवचनम्) | Plural (बहुवचनम्) |\n",
        "| :--- | :--- | :--- |\n"
    ]
    for row in data:
        table.append(f"| {row[0]} | {row[1]} | {row[2]} |\n")
    table.append(":::\n")
    return "".join(table)

# 27.7.1 - 27.7.8
# I'll use a mapping of case names
cases = [
    "**1. Nom.** (प्रथमा)",
    "**2. Akk.** (द्वितीया)",
    "**3. Inst.** (तृतीया)",
    "**4. Dat.** (चतुर्थी)",
    "**5. Abl.** (पञ्चमी)",
    "**6. Gen.** (षष्ठी)",
    "**7. Lok.** (सप्तमी)"
]

# For simplicity and safety, I'll only replace the most broken parts
# by searching for the start of each section and replacing until the end of the grammar box.

def replace_section(content, start_pattern, new_table):
    # Match the section from start_pattern until the first ::: after grammar-box
    pattern = re.escape(start_pattern) + r".*?::: grammar-box.*?:::"
    return re.sub(pattern, new_table, content, flags=re.DOTALL)

# Data for simple tables (extracted from view_file output)
# 27.7.1 नर
ner_table = fix_3col_table("27.7.1. Maskulina auf -a: नर", "नर", [
    [cases[0], "नरस्", "नरास्"],
    [cases[1], "नरम्", "नरान्"],
    [cases[2], "नरेण", "नरैस्"],
    [cases[3], "नराय", "नरेभ्यस्"],
    [cases[4], "नरात्", "नरेभ्यस्"],
    [cases[5], "नरस्य", "नराणाम्"],
    [cases[6], "नरे", "नरेषु"]
])

# 27.7.2 फल
phel_table = fix_3col_table("27.7.2. Neutra auf -a: फल", "फल", [
    [cases[0], "फलम्", "फलानि"],
    [cases[1], "फलम्", "फलानि"],
    [cases[2], "फलेन", "फलैस्"],
    [cases[3], "फलाय", "फलेभ्यस्"],
    [cases[4], "फलात्", "फलेभ्यस्"],
    [cases[5], "फलस्य", "फलानाम्"],
    [cases[6], "फले", "फलेषु"]
])

# 27.7.3 क्षत्रिया
ksatriya_table = fix_3col_table("27.7.3. Feminina auf -ā: क्षत्रिया", "क्षत्रिया", [
    [cases[0], "क्षत्रिया", "क्षत्रियास्"],
    [cases[1], "क्षत्रियाम्", "क्षत्रियास्"],
    [cases[2], "क्षत्रियया", "क्षत्रियाभिस्"],
    [cases[3], "क्षत्रियायै", "क्षत्रियाभ्यस्"],
    [cases[4], "क्षत्रियायास्", "क्षत्रियाभ्यस्"],
    [cases[5], "क्षत्रियायास्", "क्षत्रियाणाम्"],
    [cases[6], "क्षत्रियायाम्", "क्षत्रियासु"]
])

# 27.7.4 अरि
ari_table = fix_3col_table("27.7.4. Maskulina auf -i: अरि", "अरि", [
    [cases[0], "अरिस्", "अरयस्"],
    [cases[1], "अरिम्", "अरीन्"],
    [cases[2], "अरिणा", "अरिभिस्"],
    [cases[3], "अरये", "अरिभ्यस्"],
    [cases[4], "अरेस्", "अरिभ्यस्"],
    [cases[5], "अरेस्", "अरीणाम्"],
    [cases[6], "अरौ", "अरिषु"]
])

# 27.7.5 मति
mati_table = fix_3col_table("27.7.5. Feminina auf -i: मति", "मति", [
    [cases[0], "मतिस्", "मतयस्"],
    [cases[1], "मतिम्", "मतीस्"],
    [cases[2], "मत्या", "मतिभिस्"],
    [cases[3], "मतये / मत्यै", "मतिभ्यस्"],
    [cases[4], "मतेस् / मत्यास्", "मतिभ्यस्"],
    [cases[5], "मतेस् / मत्यास्", "मतीनाम्"],
    [cases[6], "मतौ / मत्याम्", "मतिषु"]
])

# 27.7.6 गुरु
guru_table = fix_3col_table("27.7.6. Maskulina auf -u: गुरु", "गुरु", [
    [cases[0], "गुरुस्", "गुरवस्"],
    [cases[1], "गुरुम्", "गुरून्"],
    [cases[2], "गुरुणा", "गुरुभिस्"],
    [cases[3], "गुरवे", "गुरुभ्यस्"],
    [cases[4], "गुरोस्", "गुरुभ्यस्"],
    [cases[5], "गुरोस्", "गुरूणाम्"],
    [cases[6], "गुरौ", "गुरुषु"]
])

# 27.7.7 धेनु
dhenu_table = fix_3col_table("27.7.7. Feminina auf -u: धेनु", "धेनु", [
    [cases[0], "धेनुस्", "धेनवस्"],
    [cases[1], "धेnuम्", "धेनूस्"],
    [cases[2], "धेन्वा", "धेनुभिस्"],
    [cases[3], "धेनवे / धेन्वै", "धेनुभ्यस्"],
    [cases[4], "धेनोस् / धेन्वास्", "धेनुभ्यस्"],
    [cases[5], "धेनोस् / धेन्वास्", "धेनूनाम्"],
    [cases[6], "धेनौ / धेन्वाम्", "धेनुषु"]
])

# 27.7.8 देवी
devi_table = fix_3col_table("27.7.8. Mehrsilbige Feminina auf -ī: देवी", "देवी", [
    [cases[0], "देवी", "देव्यस्"],
    [cases[1], "देवीम्", "देवीस्"],
    [cases[2], "देव्या", "देवीभिस्"],
    [cases[3], "देव्यै", "देवीभ्यस्"],
    [cases[4], "देव्यास्", "देवीभ्यस्"],
    [cases[5], "देव्यास्", "देवीनाम्"],
    [cases[6], "देव्याम्", "देवीषु"]
])

# Apply replacements
content = replace_section(content, "### 27.7.1. Maskulina auf -a: नर", ner_table)
content = replace_section(content, "### 27.7.2. Neutra auf -a: फल", phel_table)
content = replace_section(content, "### 27.7.3. Feminina auf -ā: क्षत्रिया", ksatriya_table)
content = replace_section(content, "### 27.7.4. Maskulina auf -i: अरि", ari_table)
content = replace_section(content, "### 27.7.5. Feminina auf -i: मति", mati_table)
content = replace_section(content, "### 27.7.6. Maskulina auf -u: गुरु", guru_table)
content = replace_section(content, "### 27.7.7. Feminina auf -u: धेनु", dhenu_table)
content = replace_section(content, "### 27.7.8. Mehrsilbige Feminina auf -ī: देवी", devi_table)

# Fix 27.7.9 (sant), 27.7.10 (mahat), 27.7.11 (gunavant)
# These have 4 columns of data (m, n, m, n)

def fix_4col_table(title, stem, data):
    table = [
        f"### {title}\n",
        "\n",
        "::: grammar-box\n",
        "| Kasus | Singular (एकवचनम्) | | Plural (बहुवचनम्) | |\n",
        "| :--- | :--- | :--- | :--- | :--- |\n",
        "| | Mask. (पुंस्) | Neut. (नपुंसकम्) | Mask. (पुंस्) | Neut. (नपुंसकम्) |\n"
    ]
    for row in data:
        table.append(f"| {row[0]} | {row[1]} | {row[2]} | {row[3]} | {row[4]} |\n")
    table.append(":::\n")
    return "".join(table)

sant_table = fix_4col_table("27.7.9. Partizip Präsens Parasmaipada auf -ant: सन्त्", "सन्त्", [
    [cases[0], "सन्", "सत्", "सन्तस्", "सन्ति"],
    [cases[1], "सन्तम्", "सत्", "सतस्", "सन्ति"],
    [cases[2], "सता", "सद्भिस्", "सता", "सद्भिस्"], # Wait, Inst. is same for m/n
    [cases[3], "सते", "सद्भ्यस्", "सते", "सद्भ्यस्"],
    [cases[4], "सतस्", "सद्भ्यस्", "सतस्", "सद्भ्यस्"],
    [cases[5], "सतस्", "सताम्", "सतस्", "सताम्"],
    [cases[6], "सति", "सत्सु", "सति", "सत्सु"]
])
# Correcting Inst/Dat/Abl/Gen/Lok for 4col
def fix_4col_table_v2(title, stem, data):
    table = [
        f"### {title}\n",
        "\n",
        "::: grammar-box\n",
        "| Kasus | Singular (एकवचनम्) | | Plural (बहुवचनम्) | |\n",
        "| :--- | :--- | :--- | :--- | :--- |\n",
        "| | Mask. (पुंस्) | Neut. (नपुंसकम्) | Mask. (पुंस्) | Neut. (नपुंसकम्) |\n"
    ]
    for row in data:
        if len(row) == 5:
            table.append(f"| {row[0]} | {row[1]} | {row[2]} | {row[3]} | {row[4]} |\n")
        else: # Case where m and n are identical
            table.append(f"| {row[0]} | {row[1]} | | {row[2]} | |\n")
    table.append(":::\n")
    return "".join(table)

sant_data = [
    [cases[0], "सन्", "सत्", "सन्तस्", "सन्ति"],
    [cases[1], "सन्तम्", "सत्", "सतस्", "सन्ति"],
    [cases[2], "सता", "सद्भिस्"],
    [cases[3], "सते", "सद्भ्यस्"],
    [cases[4], "सतस्", "सद्भ्यस्"],
    [cases[5], "सतस्", "सताम्"],
    [cases[6], "सति", "सत्सु"]
]
mahat_data = [
    [cases[0], "महान्", "महत्", "महान्तस्", "महान्ति"],
    [cases[1], "महान्तम्", "महत्", "महतस्", "महान्ति"],
    [cases[2], "महता", "महद्भिस्"],
    [cases[3], "महते", "महद्भ्यस्"],
    [cases[4], "महतस्", "महद्भ्यस्"],
    [cases[5], "महतस्", "महताम्"],
    [cases[6], "महति", "महत्सु"]
]
gunavant_data = [
    [cases[0], "गुणवान्", "गुणवत्", "गुणवन्तस्", "गुणवन्ति"],
    [cases[1], "गुणवन्तम्", "गुणवत्", "गुणवतस्", "गुणवन्ति"],
    [cases[2], "गुणवता", "गुणवद्भिस्"],
    [cases[3], "गुणवते", "गुणवद्भ्यस्"],
    [cases[4], "गुणवतस्", "गुणवद्भ्यस्"],
    [cases[5], "गुणवतस्", "गुणवताम्"],
    [cases[6], "गुणवति", "गुणवत्सु"]
]

content = replace_section(content, "### 27.7.9. Partizip Präsens Parasmaipada auf -ant: सन्त्", fix_4col_table_v2("27.7.9. Partizip Präsens Parasmaipada auf -ant: सन्त्", "सन्त्", sant_data))
content = replace_section(content, "### 27.7.10. महान्त्", fix_4col_table_v2("27.7.10. महान्त्", "महान्त्", mahat_data))
content = replace_section(content, "### 27.7.11. Maskulina und Neutra auf -vant / -mant: गुणवन्त्", fix_4col_table_v2("27.7.11. Maskulina und Neutra auf -vant / -mant: गुणवन्त्", "गुणवन्त्", gunavant_data))

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
