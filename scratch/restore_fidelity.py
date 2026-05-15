import sys

file_path = 'docs/lektionen/lektion27.md'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Remove the added headers while keeping the structure
content = content.replace('| Kasus |', '|   |')
content = content.replace('| Stamm |', '|   |')

# Also fix the labels in the row starts if they were added
# In 27.2.2 we had **m./n. Sg.** etc.
# Original likely had nothing or just the text without bolding.
# Let's check the original source again for 27.2.2.

# I will use a more precise replacement to match exactly what I added.
content = content.replace('| **m./n. Sg.** |', '| Maskulinum / Neutrum |')
content = content.replace('| **m./n. Pl.** |', '| |') # Original had empty cells or grouped headers
content = content.replace('| **f. Sg.** |', '| Femininum |')
content = content.replace('| **f. Pl.** |', '| |')

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
