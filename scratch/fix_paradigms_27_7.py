import sys

file_path = 'docs/lektionen/lektion27.md'
with open(file_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

def get_pronoun_table(title, stem, data):
    table = [
        f"### {title}\n",
        "\n",
        "::: grammar-box\n",
        f"| Kasus | Singular (एकवचनम्) | | | Plural (बहुवचनम्) | | |\n",
        "| :--- | :--- | :--- | :--- | :--- | :--- | :--- |\n",
        "| | Mask. (पुंस्) | Neut. (नपुंसकम्) | Fem. (स्त्री) | Mask. (पुंस्) | Neut. (नपुंसकम्) | Fem. (स्त्री) |\n"
    ]
    for row in data:
        table.append(f"| {row[0]} | {row[1]} | {row[2]} | {row[3]} | {row[4]} | {row[5]} | {row[6]} |\n")
    table.append(":::\n")
    return table

# Data for yad
yad_data = [
    ["**1. Nom.**", "यस्", "यत्", "या", "ये", "यानि", "यास्"],
    ["**2. Akk.**", "यम्", "यत्", "याम्", "यान्", "यानि", "यास्"],
    ["**3. Inst.**", "येन", "", "यया", "यैस्", "", "याभिस्"],
    ["**4. Dat.**", "यस्मै", "", "यस्यै", "येभ्यस्", "", "याभ्यस्"],
    ["**5. Abl.**", "यस्मात्", "", "यस्यास्", "येभ्यस्", "", "याभ्यस्"],
    ["**6. Gen.**", "यस्य", "", "यस्यास्", "येषाम्", "", "यासाम्"],
    ["**7. Lok.**", "यस्मिन्", "", "यस्याम्", "येषु", "", "यासु"]
]

# Data for kim
kim_data = [
    ["**1. Nom.**", "कस्", "किम्", "का", "के", "कानि", "कास्"],
    ["**2. Akk.**", "कम्", "किम्", "काम्", "कान्", "कानि", "कास्"],
    ["**3. Inst.**", "केन", "", "कया", "कैस्", "", "काभिस्"],
    ["**4. Dat.**", "कस्मै", "", "कस्यै", "केभ्यस्", "", "काभ्यस्"],
    ["**5. Abl.**", "कस्मात्", "", "कस्यास्", "केभ्यस्", "", "काभ्यस्"],
    ["**6. Gen.**", "कस्य", "", "कस्यास्", "केषाम्", "", "कासाम्"],
    ["**7. Lok.**", "कस्मिन्", "", "कस्याम्", "केषु", "", "कासु"]
]

# Replacement for 27.7.13
start_13 = -1
end_13 = -1
for i, line in enumerate(lines):
    if "### 27.7.13. Relativpronomen: यद्" in line:
        start_13 = i
    if start_13 != -1 and "### 27.7.14. Fragepronomen: किम्" in line:
        end_13 = i - 1
        break

if start_13 != -1 and end_13 != -1:
    lines[start_13:end_13+1] = get_pronoun_table("27.7.13. Relativpronomen: यद्", "यद्", yad_data)

# Replacement for 27.7.14
start_14 = -1
end_14 = -1
for i, line in enumerate(lines):
    if "### 27.7.14. Fragepronomen: किम्" in line:
        start_14 = i
    if start_14 != -1 and i > start_14 and "::: media" in line:
        end_14 = i - 1
        break
# If no media at end, go to end of file
if end_14 == -1: end_14 = len(lines) - 1

if start_14 != -1:
    lines[start_14:end_14+1] = get_pronoun_table("27.7.14. Fragepronomen: किम्", "किम्", kim_data)

with open(file_path, 'w', encoding='utf-8') as f:
    f.writelines(lines)
