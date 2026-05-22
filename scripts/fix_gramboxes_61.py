#!/usr/bin/env python3
"""Fix grammar-box issues in lektion61.md (sections 61.2-61.9)."""

path = '/Volumes/SanDisk1TB/proj/Payer/docs/lektionen/lektion61.md'
with open(path, encoding='utf-8') as f:
    content = f.read()


def replace_exact(content, old, new, label):
    if old not in content:
        print(f'  [!] MATCH FAILED: {label}')
        return content
    result = content.replace(old, new, 1)
    print(f'  [ok] {label}')
    return result


# Fix 1: Wrap 61.2 endings table in grammar-box
content = replace_exact(content,
    'Die Endungen des periphrastischen Futur lauten also:\n'
    '\n'
    '|   | परस्मैपदम् | आत्मनेपदम् | | | | |\n'
    '| --- | --- | --- | --- | --- | --- | --- |\n'
    '|   | एकवचनम् | द्विवचनम् | बहुवचनम् | एकवचनम् | द्विवचनम् | बहुवचनम् |\n'
    '| 1\\. तृतीयः | \\-tāsmi   | | | | | |\n'
    '(-tā + asmi) | \\-tāsvas | \\-tāsmas   | | | | | |\n'
    '(-tā smas) | ***\\-tāhe*** | \\-tāsvahe | \\-tāsmahe | | | | |\n'
    '| 2\\. मध्यमः | \\-tāsi | \\-tāsthas | \\-tāstha | \\-tāse | \\-tāsāthe | \\-tādhve |\n'
    '| 3\\. प्रथमः | \\-tā | \\-tārau | \\-tāras | \\-tā | \\-tārau | \\-tāras |',

    'Die Endungen des periphrastischen Futur lauten also:\n'
    '\n'
    '::: grammar-box\n'
    '|   | परस्मैपदम् | आत्मनेपदम् | | | | |\n'
    '| --- | --- | --- | --- | --- | --- | --- |\n'
    '|   | एकवचनम् | द्विवचनम् | बहुवचनम् | एकवचनम् | द्विवचनम् | बहुवचनम् |\n'
    '| 1\\. तृतीयः | \\-tāsmi   | | | | | |\n'
    '(-tā + asmi) | \\-tāsvas | \\-tāsmas   | | | | | |\n'
    '(-tā smas) | ***\\-tāhe*** | \\-tāsvahe | \\-tāsmahe | | | | |\n'
    '| 2\\. मध्यमः | \\-tāsi | \\-tāsthas | \\-tāstha | \\-tāse | \\-tāsāthe | \\-tādhve |\n'
    '| 3\\. प्रथमः | \\-tā | \\-tārau | \\-tāras | \\-tā | \\-tārau | \\-tāras |\n'
    ':::',
    '61.2 endings table wrapped in grammar-box'
)

# Fix 2: Extend 61.3 Bildung des Intensivums grammar-box
content = replace_exact(content,
    '::: grammar-box\n'
    '**Bildung des Intensivums:**\n'
    '\n'
    '**Es gibt zwei Bildungstypen des Intensivums:**\n'
    ':::\n'
    '\n'
    '*   Ātmanepada-Intensivum\n'
    '*   Parasmaipada-Intensivum\n'
    '\n'
    'Beide werden von der mit starker Reduplikation reduplizierten Wurzel gebildet.'
    ' Beide unterscheiden sich in der Bedeutung nicht.'
    ' Beide können zu denselben Wurzeln gebildet werden.',

    '::: grammar-box\n'
    '**Bildung des Intensivums:**\n'
    '\n'
    '**Es gibt zwei Bildungstypen des Intensivums:**\n'
    '\n'
    '*   **Ātmanepada-Intensivum**\n'
    '*   **Parasmaipada-Intensivum**\n'
    '\n'
    '**Beide werden von der mit starker Reduplikation reduplizierten Wurzel gebildet.'
    ' Beide unterscheiden sich in der Bedeutung nicht.'
    ' Beide können zu denselben Wurzeln gebildet werden.**\n'
    ':::',
    '61.3 Bildung des Intensivums grammar-box extended'
)

# Fix 3: Wrap 61.3.1 Wurzeln -a-Nasal section in grammar-box
content = replace_exact(content,
    'Wurzeln der Form -a-Nasal verlängern in der Reduplikationssilbe den Vokal nicht,'
    ' sondern wiederholen den Nasal.\n'
    '\n'
    '::: indent\n'
    'z.B. यम् 1P: यंयम्य-\n'
    ':::\n'
    '\n'
    'Bei einigen Wurzeln tritt zwischen den Vokal der Reduplikationssilbe und den'
    ' anlautenden Konsonanten der Wurzel -nī- bzw. -rī- (-rī- bei Wurzeln, die im'
    ' Intensiv ein ṛ enthalten).\n'
    '\n'
    '::: indent\n'
    'z.B.\n'
    'पत् 1P: प***नी***पत्य-\n'
    'वृत् 1Ā: व***री***वृत्य-\n'
    ':::',

    ':::: grammar-box\n'
    '**Wurzeln der Form -a-Nasal verlängern in der Reduplikationssilbe den Vokal nicht,'
    ' sondern wiederholen den Nasal.**\n'
    '\n'
    '::: indent\n'
    'z.B. यम् 1P: यंयम्य-\n'
    ':::\n'
    '\n'
    '**Bei einigen Wurzeln tritt zwischen den Vokal der Reduplikationssilbe und den'
    ' anlautenden Konsonanten der Wurzel -nī- bzw. -rī- (-rī- bei Wurzeln, die im'
    ' Intensiv ein ṛ enthalten).**\n'
    '\n'
    '::: indent\n'
    'z.B.\n'
    'पत् 1P: प***नी***पत्य-\n'
    'वृत् 1Ā: व***री***वृत्य-\n'
    ':::\n'
    '\n'
    '::::',
    '61.3.1 Wurzeln -a-Nasal wrapped in grammar-box'
)

# Fix 4: Extend 61.4.2 grammar-box to include Stammbildung;
#         remove grammar-box from examples table
content = replace_exact(content,
    '::: grammar-box\n'
    '**Bedeutung:**\n'
    '\n'
    '*   **jemand wünscht sich das, was durch den Nominalstamm bezeichnet wird**\n'
    '*   **jemand behandelt oder betrachtet eine Person oder Sache wie das, was vom Nominalstamm bezeichnet wird**\n'
    ':::\n'
    '\n'
    'Stammbildung:\n'
    '\n'
    '::: indent\n'
    'vor dem -ya unterliegt der Auslauts des Nominalstamms folgenden Veränderungen:\n'
    '\n'
    '*   a, ā » ī : पुत्र » पुत्रीय-\n'
    '*   i, u\xa0 » ī, ū : कवि » कवीय-\n'
    '*   ṛ » rī : कर्तृ » कर्त्रीय-\n'
    '*   o » av : गो » गव्य-\n'
    '*   au » āv : नौ » नाव्य-\n'
    '*   auslautender Nasal fällt ab, davor stehender Vokal wird nach den eben genannten Regeln behandelt: राजन् » राजीय-\n'
    '*   andere auslautende Konsonanten bleiben unverändert\n'
    ':::\n'
    '\n'
    'Beispiele:\n'
    '\n'
    '::: grammar-box\n'
    '| पुत्र m. "Sohn" | पुत्रीयति "er wünscht sich einen Sohn" |\n'
    '| --- | --- |\n'
    '| कवि m. "Dichter" | कवीयति "er wünscht sich einen Dichter" |\n'
    '| गो f. "Kuh" | गव्यति "er wünscht sich eine Kuh" |\n'
    '| राजन् m. "König" | राजीयति "er wünscht sich einen König" |\n'
    '| विष्णु m. Viṣṇu | विष्णूयति "er behandelt jemanden wie Viṣṇu" |\n'
    '| प्रासाद m. "Palast" | प्रासादीयति "er sieht (z.B. seine Hütte) für einen Palast an" |\n'
    ':::',

    ':::: grammar-box\n'
    '**Bedeutung:**\n'
    '\n'
    '*   **jemand wünscht sich das, was durch den Nominalstamm bezeichnet wird**\n'
    '*   **jemand behandelt oder betrachtet eine Person oder Sache wie das, was vom Nominalstamm bezeichnet wird**\n'
    '\n'
    '**Stammbildung:**\n'
    '\n'
    '::: indent\n'
    '**vor dem -ya unterliegt der Auslauts des Nominalstamms folgenden Veränderungen:**\n'
    '\n'
    '*   **a, ā » ī :** पुत्र » पुत्रीय-\n'
    '*   **i, u » ī, ū :** कवि » कवीय-\n'
    '*   **ṛ » rī :** कर्तृ » कर्त्रीय-\n'
    '*   **o » av :** गो » गव्य-\n'
    '*   **au » āv :** नौ » नाव्य-\n'
    '*   **auslautender Nasal fällt ab, davor stehender Vokal wird nach den eben genannten Regeln behandelt:** राजन् » राजीय-\n'
    '*   **andere auslautende Konsonanten bleiben unverändert**\n'
    ':::\n'
    '\n'
    '::::\n'
    '\n'
    'Beispiele:\n'
    '\n'
    '| पुत्र m. "Sohn" | पुत्रीयति "er wünscht sich einen Sohn" |\n'
    '| --- | --- |\n'
    '| कवि m. "Dichter" | कवीयति "er wünscht sich einen Dichter" |\n'
    '| गो f. "Kuh" | गव्यति "er wünscht sich eine Kuh" |\n'
    '| राजन् m. "König" | राजीयति "er wünscht sich einen König" |\n'
    '| विष्णु m. Viṣṇu | विष्णूयति "er behandelt jemanden wie Viṣṇu" |\n'
    '| प्रासाद m. "Palast" | प्रासादीयति "er sieht (z.B. seine Hütte) für einen Palast an" |',
    '61.4.2 grammar-box extended to include Stammbildung; examples grammar-box removed'
)

# Fix 5: Wrap 61.4.3 Bedeutung in grammar-box
content = replace_exact(content,
    'Bedeutung:\n'
    '\n'
    '::: indent\n'
    'jemand wünsch sich das, was durch den Nominalstamm bezeichnet wird\n'
    ':::\n'
    '\n'
    'Beispiele:\n'
    '\n'
    '| पुत्र m. "Sohn" | पुत्रकाय्म्यति "er wünscht sich einen Sohn" |',

    '::: grammar-box\n'
    '**Bedeutung:**\n'
    '\n'
    '**jemand wünsch sich das, was durch den Nominalstamm bezeichnet wird**\n'
    ':::\n'
    '\n'
    'Beispiele:\n'
    '\n'
    '| पुत्र m. "Sohn" | पुत्रकाय्म्यति "er wünscht sich einen Sohn" |',
    '61.4.3 Bedeutung wrapped in grammar-box'
)

# Fix 6: Extend 61.4.5 grammar-box to include Bildung bullets
content = replace_exact(content,
    ':::: grammar-box\n'
    '**Bedeutung:**\n'
    '\n'
    '::: indent\n'
    '**jemand verhält sich als das, oder gleicht dem, was durch den Nominalstamm bezeichnet wird.**\n'
    ':::\n'
    '::::\n'
    '\n'
    'Bildung:\n'
    '\n'
    '*   auslautendes -a » -ā\n'
    '*   auslautendes -ā bleibt unverändert\n'
    '*   sonst wie vor -ya, Parasmaipada (siehe oben 4.2.)\n'
    '*   auslautendes -as wahlweise » -ā\n'
    '*   Femininstamm meist » Maskulinstamm',

    ':::: grammar-box\n'
    '**Bedeutung:**\n'
    '\n'
    '::: indent\n'
    '**jemand verhält sich als das, oder gleicht dem, was durch den Nominalstamm bezeichnet wird.**\n'
    ':::\n'
    '\n'
    '**Bildung:**\n'
    '\n'
    '*   **auslautendes -a » -ā**\n'
    '*   **auslautendes -ā bleibt unverändert**\n'
    '*   **sonst wie vor -ya, Parasmaipada (siehe oben 4.2.)**\n'
    '*   **auslautendes -as wahlweise » -ā**\n'
    '*   **Femininstamm meist » Maskulinstamm**\n'
    '\n'
    '::::',
    '61.4.5 Bedeutung+Bildung grammar-box extended'
)

# Fix 7: Extend 61.4.5 second grammar-box to include z.B. and "In einigen Fällen"
content = replace_exact(content,
    '::: grammar-box\n'
    '**Bei einigen Nominalstämmen bedeutet dieses Suffix: etwas wird wie das,'
    ' oder wird zu dem, was durch den Nominalstamm bezeichnet wird:**\n'
    ':::\n'
    '\n'
    '::: indent\n'
    'z.B. उन्मनस् 3 "erregt": उन्मनायते "er wird erregt"\n'
    ':::\n'
    '\n'
    'In einigen Fällen werden mit diesem Suffix Verben in anderen Bedeutungen gebildet:\n'
    '\n'
    'Beispiele:\n'
    '\n'
    '::: indent\n'
    'दुःख n. "Leid" : दुःखायते "er empfindet Leid"\n'
    'शब्द m. "Laut" : शब्दायते "er gibt einen Ton von sich"\n'
    ':::',

    ':::: grammar-box\n'
    '**Bei einigen Nominalstämmen bedeutet dieses Suffix: etwas wird wie das,'
    ' oder wird zu dem, was durch den Nominalstamm bezeichnet wird:**\n'
    '\n'
    '::: indent\n'
    'z.B. उन्मनस् 3 "erregt": उन्मनायते "er wird erregt"\n'
    ':::\n'
    '\n'
    '**In einigen Fällen werden mit diesem Suffix Verben in anderen Bedeutungen gebildet:**\n'
    '\n'
    'Beispiele:\n'
    '\n'
    '::: indent\n'
    'दुःख n. "Leid" : दुःखायते "er empfindet Leid"\n'
    'शब्द m. "Laut" : शब्दायते "er gibt einen Ton von sich"\n'
    ':::\n'
    '\n'
    '::::',
    '61.4.5 second grammar-box extended to include z.B. and In einigen Fällen'
)

# Fix 8: Extend 61.5 Benediktiv grammar-box to include Ātmanepada and Kielhorn ref
content = replace_exact(content,
    ':::: grammar-box\n'
    '**Bedeutung:**\n'
    '\n'
    '::: indent\n'
    '**Segenswunsch**\n'
    ':::\n'
    '\n'
    '**Bildung:**\n'
    '\n'
    '**Parasmaipada:**\n'
    '\n'
    '**tiefstufige Wurzel + yās + Sekundärendung**\n'
    '::::\n'
    '\n'
    '::: indent\n'
    'z.B. बुध्यासम् "möge ich erkennen!"\n'
    ':::\n'
    '\n'
    'Ātmanepada:\n'
    '\n'
    '(meist) hochstufige Wurzel + sī(y) + Sekundärendung\n'
    '\n'
    'oder:\n'
    '\n'
    '(hochstufige) Wurzel + ै + sī(y) + Sekundäraendung\n'
    '\n'
    '::: indent\n'
    'z.B.\n'
    'जि : जेषीय "möge ich im eigenen Interesse siegen!"\n'
    'बुध् : बोधिषीय "möge ich erkennen"\n'
    ':::\n'
    '\n'
    'Die Regeln zur Form der Wurzel im Einzelnen bei Kielhorn, Grammatik § 380ff.',

    ':::: grammar-box\n'
    '**Bedeutung:**\n'
    '\n'
    '::: indent\n'
    '**Segenswunsch**\n'
    ':::\n'
    '\n'
    '**Bildung:**\n'
    '\n'
    '**Parasmaipada:**\n'
    '\n'
    '**tiefstufige Wurzel + yās + Sekundärendung**\n'
    '\n'
    '::: indent\n'
    'z.B. बुध्यासम् "möge ich erkennen!"\n'
    ':::\n'
    '\n'
    '**Ātmanepada:**\n'
    '\n'
    '**(meist) hochstufige Wurzel + sī(y) + Sekundärendung**\n'
    '\n'
    '**oder:**\n'
    '\n'
    '**(hochstufige) Wurzel + ै + sī(y) + Sekundäraendung**\n'
    '\n'
    '::: indent\n'
    'z.B.\n'
    'जि : जेषीय "möge ich im eigenen Interesse siegen!"\n'
    'बुध् : बोधिषीय "möge ich erkennen"\n'
    ':::\n'
    '\n'
    '**Die Regeln zur Form der Wurzel im Einzelnen bei Kielhorn, Grammatik § 380ff.**\n'
    '\n'
    '::::',
    '61.5 Benediktiv grammar-box extended to include Ātmanepada and Kielhorn ref'
)

# Fix 9: Extend 61.7 grammar-box to include गो sentence
content = replace_exact(content,
    '::: grammar-box\n'
    '**Vor Konsonant lauten diese Stämme auf -ai, -o, -au; vor Konsonant auf -āy, -av, -āv**\n'
    ':::\n'
    '\n'
    'गो m.f. "Ochse, Kuh" hat Stammabstufung.'
    ' Siehe die Erklärung im Einzelnen bei Thumb-Hauschild § 296/7.',

    '::: grammar-box\n'
    '**Vor Konsonant lauten diese Stämme auf -ai, -o, -au; vor Konsonant auf -āy, -av, -āv**\n'
    '\n'
    '**गो m.f. "Ochse, Kuh" hat Stammabstufung.**'
    ' Siehe die Erklärung im Einzelnen bei Thumb-Hauschild § 296/7.\n'
    ':::',
    '61.7 grammar-box extended to include गो sentence'
)

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print('lektion61.md patch done.')
