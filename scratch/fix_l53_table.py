import os
import re

filepath = 'docs/lektionen/lektion53.md'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# Match the table from its header down to the last 'Rest wie Maskulinum'
pattern = r'\|\s* \s*\|\s*तद्\s*\|\s*एतद्\s*\|\s*इदम्\s*\|\s*यद्\s*\|\s*किम्\s*\|.*?Rest wie Maskulinum\s*\|'
replacement = """::: grammar-box
|   | तद् | एतद् | इदम् | यद् | किम् |
| --- | --- | --- | --- | --- | --- |
| **Maskulinum** | | | | | |
| **1.** | तौ | एतौ | इमौ | यौ | कौ |
| **2.** | तौ | एतौ / एनौ | इमौ / एनौ | यौ | कौ |
| **3., 4., 5.** | ताभ्याम् | एताभ्याम् | आभ्याम् | याभ्याम् | काभ्याम् |
| **6., 7.** | तयोस् | एतयोस् / एनयोस् | अनयोस् / एनयोस् | ययोस् | कयोस् |
| **Neutrum** | | | | | |
| **1., 2.** | ते | एते / एने | इमे / एने | ये | के |
| | (Rest wie Maskulinum) | | | | |
| **Femininum** | | | | | |
| **1., 2.** | ते | एते / एने | इमे / एने | ये | के |
| | (Rest wie Maskulinum) | | | | |
:::"""

new_content = re.sub(pattern, replacement, content, flags=re.DOTALL)

# Handle the Komparative table too
pattern2 = r'\|\s* \s*\|\s*एकवचनम्\s*\|\s*द्विवचनम्\s*\|\s*बहुवचनम्\s*\|.*?गरीयांसी\s*\|'
replacement2 = """::: grammar-box
|   | एकवचनम् | | द्विवचनम् | | बहुवचनम् | |
| --- | --- | --- | --- | --- | --- | --- |
| | पुमान् | नपुंसकम् | पुमान् | नपुंसकम् | पुमान् | नपुंसकम् |
| **1.** | गरीयान् | गरीयस् | गरीयांसौ | गरीयसी | गरीयांसस् | गरीयांसि |
| **2.** | गरीयांसम् | गरीयस् | गरीयांसौ | गरीयसी | गरीयसस् | गरीयांसि |
| **3.** | गरीयसा | | गरीयोभ्याम् | | गरीयोभिस् | |
| **4.** | गरीयसे | | गरीयोभ्याम् | | गरीयोभ्यस् | |
| **5.** | गरीयसस् | | गरीयोभ्याम् | | गरीयोभ्यस् | |
| **6.** | गरीयसस् | | गरीयसोस् | | गरीयसाम् | |
| **7.** | गरीयसि | | गरीयसोस् | | गरीयःसु / गरीयस्su | |
| **Vok.** | गरीयान् | गरीयस् | गरीयांसौ | गरीयसी | गरीयांसस् | गरीयांसि |
:::"""

new_content = re.sub(pattern2, replacement2, new_content, flags=re.DOTALL)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(new_content)
print("Success")
