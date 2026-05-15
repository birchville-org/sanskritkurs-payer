import sys

file_path = 'docs/lektionen/lektion27.md'
with open(file_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

new_table = [
    "### 27.2.2. Frage-, Demonstrativ- und Relativpronomina\n",
    "\n",
    "| Kasus | किम् | यद् | तद् | एतद् | इदम् |\n",
    "| :--- | :--- | :--- | :--- | :--- | :--- |\n",
    "| **m./n. Sg.** | कस्मिन् | यस्मिन् | तस्मिन् | एतस्मिन् | अस्मिन् |\n",
    "| **m./n. Pl.** | केषु | येषु | तेषु | एतेषु | एषु |\n",
    "| **f. Sg.** | कस्याम् | यस्याम् | तस्याम् | एतस्याम् | अस्याम् |\n",
    "| **f. Pl.** | कासु | यासु | तासु | एतासु | आसु |\n"
]

# Section 27.2.2 starts at line 106 (1-indexed, so index 105)
# Ends at line 138 (index 137)
start_idx = 105
end_idx = 138

lines[start_idx:end_idx+1] = new_table

with open(file_path, 'w', encoding='utf-8') as f:
    f.writelines(lines)
