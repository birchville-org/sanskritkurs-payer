import sys

file_path = 'docs/lektionen/lektion27.md'
with open(file_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

new_table = [
    "## 27.3. Übersicht über die regulären Kasusendungen (विभक्ति)\n",
    "\n",
    "::: grammar-box\n",
    "| Kasus | Singular (एकवचनम्) | | Plural (बहुवचनम्) | |\n",
    "| :--- | :--- | :--- | :--- | :--- |\n",
    "| | m./f. (पुंस्/स्त्री) | n. (नपुंसकम्) | m./f. (पुंस्/स्त्री) | n. (नपुंसकम्) |\n",
    "| **1. Nom.** (प्रथमा) | -s | -Ø | -as | -i |\n",
    "| **2. Akk.** (द्वितीया) | -am | -Ø | -as | -i |\n",
    "| **3. Inst.** (तृतीया) | -ā | | -bhis | |\n",
    "| **4. Dat.** (चतुर्थी) | -e | | -bhyas | |\n",
    "| **5. Abl.** (पञ्चमी) | -as | | -bhyas | |\n",
    "| **6. Gen.** (षष्ठी) | -as | | -ām | |\n",
    "| **7. Lok.** (सप्तमी) | -i | | -su | |\n",
    ":::\n"
]

# Find section 27.3
# In view_file output it started around 149 (shifted to ~153)
start_line = -1
end_line = -1
for i, line in enumerate(lines):
    if "## 27.3. Übersicht über die regulären Kasusendungen" in line:
        start_line = i
    if start_line != -1 and "Unterstrichen: starke Kasus" in line:
        end_line = i - 1
        break

if start_line != -1 and end_line != -1:
    lines[start_line:end_line+1] = new_table

with open(file_path, 'w', encoding='utf-8') as f:
    f.writelines(lines)
