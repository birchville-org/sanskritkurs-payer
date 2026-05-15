import re
import sys

file_path = 'docs/lektionen/lektion16.md'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Find Latin letters mixed with Devanagari
mixed_pattern = re.compile(r'([\u0900-\u097F]+[a-zA-Z]+|[a-zA-Z]+[\u0900-\u097F]+)')
matches = mixed_pattern.findall(content)

if matches:
    print(f"Found mixed patterns in L16: {matches}")
    # Fix specific cases
    content = content.replace('सुखवल्lok', 'सुखवल्लोक')
    content = content.replace('आप्nuवन्ति', 'आप्नुवन्ति')
    content = content.replace('धेnu', 'धेनु')

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
