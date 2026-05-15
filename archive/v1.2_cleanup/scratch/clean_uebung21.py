import sys
import re

path = "/Volumes/SanDisk1TB/proj/Payer/docs/bg/lektionen/uebung21.md"
with open(path, "r", encoding="utf-8") as f:
    content = f.read()

# Pattern for the German/Bulgarian mix:
# Line 1: Sanskrit (Devanagari)
# Line 2: German translation
# Line 3: Bulgarian translation prefix '*превод:*'
# Goal: Remove German line and the '*превод:*' prefix.

# Also remove the 'A)' section German/Bulgarian mix which I partially fixed but let's be thorough.

# Fix the specific lines:
# 1. मृतं...
content = content.replace(
    "> Das Feuer, das den Toten verbrennt, verbrennt auch die treue Gattin (सती).  \n> *превод:* ",
    "> "
)
# 2. सद्गुरु...
content = content.replace(
    "> Der gute Meister preist den großen Gott mit Lobliedern der großen Dichters.  \n> *превод:* ",
    "> "
)
# 3. महान्ति...
content = content.replace(
    "> Die Knaben, die große Früchte essen, trinken auch Wasser.  \n> *превод:* ",
    "> "
)
# 4. पुरजां...
content = content.replace(
    "> Während der Verehrung opfert und preist der Mann die Gottheit.  \n> *превод:* ",
    "> "
)
# 5. गुरूपनी... (Partially fixed but let's ensure it's clean)
content = content.replace(
    "> Ein Zweimalgeborener ist ein Mann, der vom Meister in den Veda initiiert wurde.  \n> *превод:* ",
    "> "
)
# 6. जितक्रोधो...
content = content.replace(
    "> Wer den Zorn besiegt hat, der hasst einen Feind nicht, auch wenn dieser ihn tötet. Wer aber vom Zorn besiegt ist, hasst.  \n> *превод:* ",
    "> "
)

# Clean up any trailing space before newlines in Sanskrit lines if they were part of the problem
content = re.sub(r'  \n', '\n', content)

with open(path, "w", encoding="utf-8") as f:
    f.write(content)
