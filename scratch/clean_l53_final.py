import os

filepath = 'docs/lektionen/lektion53.md'
with open(filepath, 'r', encoding='utf-8') as f:
    lines = f.readlines()

new_lines = []
skip = False
for line in lines:
    if line.strip() == "| Femininum |   |   |   |   |   |" or line.strip() == "| Femininum |   |   |   |   |   |":
        skip = True
    
    if not skip:
        new_lines.append(line)
    
    if skip and "| Rest wie Maskulinum |" in line:
        skip = False

with open(filepath, 'w', encoding='utf-8') as f:
    f.writelines(new_lines)
print("Success")
