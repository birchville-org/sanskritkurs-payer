#!/usr/bin/env python3
"""Fix grammar-boxes in lektion59.md (59.2.1-59.2.5) and lektion60.md (60.3 and 60.6)."""
import re

BASE = '/Volumes/SanDisk1TB/proj/Payer/docs/lektionen'

# ── lektion59.md: wrap plain tables in sections 59.2.1–59.2.5 ─────────────────

def fix_59():
    path = f'{BASE}/lektion59.md'
    with open(path, encoding='utf-8') as f:
        lines = f.read().split('\n')

    result = []
    i = 0
    in_target = False
    depth = 0

    while i < len(lines):
        line = lines[i]

        # Enter target when ## 59.2. heading found
        if re.match(r'^## 59\.2\.', line):
            in_target = True
        # Exit target at next ## heading that is not 59.2
        elif re.match(r'^## ', line) and not re.match(r'^## 59\.2\.', line):
            in_target = False

        # Track container nesting depth
        stripped = line.strip()
        if re.match(r'^:{3,}', stripped):
            if depth == 0:
                depth += 1
            else:
                depth -= 1

        # Wrap table block if in target section and not inside a container
        if in_target and depth == 0 and line.startswith('|'):
            result.append('::: grammar-box')
            while i < len(lines) and lines[i].startswith('|'):
                result.append(lines[i])
                i += 1
            result.append(':::')
            continue

        result.append(line)
        i += 1

    with open(path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(result))
    print('lektion59.md: tables in 59.2.1–59.2.5 wrapped.')


# ── lektion60.md: fix 60.3 tables and 60.6 grammar-boxes ─────────────────────

def replace_exact(content, old, new, label):
    if old not in content:
        print(f'  [!] MATCH FAILED: {label}')
        return content
    result = content.replace(old, new, 1)
    print(f'  [ok] {label}')
    return result


def fix_60():
    path = f'{BASE}/lektion60.md'
    with open(path, encoding='utf-8') as f:
        content = f.read()

    # ── 60.3: wrap गण् table ─────────────────────────────────────────────────
    content = replace_exact(content,
        'गण् 10P "zählen"\n\n'
        '|   | **परस्मैपदम्** |\n'
        '| --- | --- |\n'
        '| 1\\. तृतीयः | गणयां चकृव[[br]]गणयामासिव[[br]]गणयां बभूविव |\n'
        '| 2\\. मध्यमः | गणयां चक्रथुर्[[br]]गणयामासथुर्[[br]]गणयां बभूवथुर् |\n'
        '| 3\\. प्रथमः | गणयां चक्रतुर्[[br]]गणयामासतुर्[[br]]गणयां बभूवतुर् |',

        'गण् 10P "zählen"\n\n'
        '::: grammar-box\n'
        '|   | **परस्मैपदम्** |\n'
        '| --- | --- |\n'
        '| 1\\. तृतीयः | गणयां चकृव[[br]]गणयामासिव[[br]]गणयां बभूविव |\n'
        '| 2\\. मध्यमः | गणयां चक्रथुर्[[br]]गणयामासथुर्[[br]]गणयां बभूवथुर् |\n'
        '| 3\\. प्रथमः | गणयां चक्रतुर्[[br]]गणयामासतुर्[[br]]गणयां बभूवतुर् |\n'
        ':::',
        '60.3 गण् table wrapped'
    )

    # ── 60.3: wrap आस् table ─────────────────────────────────────────────────
    content = replace_exact(content,
        'आस् 2Ā "sitzen"\n\n'
        '|   | **आत्मनेपदम्** |\n'
        '| --- | --- |\n'
        '| 1\\. तृतीयः | आसां चकृवहे[[br]]आसामासिव[[br]]आसां बभूविवव् |\n'
        '| 2\\. मध्यमः | आसांव् चक्राथे[[br]]आसामासथुर्[[br]]आसां बभूवथुर् |\n'
        '| 3\\. प्रथमः | आसां चक्राते[[br]]आसामासतुर्[[br]]आसां बभूवतुर्व् |',

        'आस् 2Ā "sitzen"\n\n'
        '::: grammar-box\n'
        '|   | **आत्मनेपदम्** |\n'
        '| --- | --- |\n'
        '| 1\\. तृतीयः | आसां चकृवहे[[br]]आसामासिव[[br]]आसां बभूविवव् |\n'
        '| 2\\. मध्यमः | आसांव् चक्राथे[[br]]आसामासथुर्[[br]]आसां बभूवथुर् |\n'
        '| 3\\. प्रथमः | आसां चक्राते[[br]]आसामासतुर्[[br]]आसां बभूवतुर्व् |\n'
        ':::',
        '60.3 आस् table wrapped'
    )

    # ── 60.6 intro + Bedeutung → grammar-box ─────────────────────────────────
    content = replace_exact(content,
        'Von jeder Wurzel sowie vom Kausativum kann ein Desiderativum (सन्) gebildet werden.'
        ' Das Desiderativum kann in allen Zeiten und Modi des P, Ā und Passiv konjugiert werde.'
        ' Desiderativformen außerhalb des Präsensstamms sind aber sehr selten.\n'
        '\n'
        'Bedeutung:\n'
        '\n'
        '*   eine Person oder Sache wünscht zu tun oder zu erleiden,'
        ' was durch die Wurzel oder das Kausativum ausgedrückt wird\n'
        '*   seltener: jemand oder etwas ist im Begriffe, zu tun,'
        ' was durch die Wurzel oder das Kausativum ausgedrückt wird',

        '::: grammar-box\n'
        '**Von jeder Wurzel sowie vom Kausativum kann ein Desiderativum (सन्) gebildet werden.'
        ' Das Desiderativum kann in allen Zeiten und Modi des P, Ā und Passiv konjugiert werde.'
        ' Desiderativformen außerhalb des Präsensstamms sind aber sehr selten.**\n'
        '\n'
        '**Bedeutung:**\n'
        '\n'
        '*   **eine Person oder Sache wünscht zu tun oder zu erleiden,'
        ' was durch die Wurzel oder das Kausativum ausgedrückt wird**\n'
        '*   **seltener: jemand oder etwas ist im Begriffe, zu tun,'
        ' was durch die Wurzel oder das Kausativum ausgedrückt wird**\n'
        ':::',
        '60.6 intro+Bedeutung grammar-box'
    )

    # ── 60.6 Beispiele: remove grammar-box wrapper ────────────────────────────
    content = replace_exact(content,
        '####  Beispiele:\n'
        '\n'
        '::: grammar-box\n'
        '| कृ 8U | चिकीर्षति "er wünscht zu tun" |\n'
        '| --- | --- |\n'
        '| पत् 1P | पिपतिषति "er ist im Begriffe, zu fallen" |\n'
        '| चुर् 10U | चुचोरयिषति "er wünscht zu stehlen" |\n'
        '| बुध् Kaus. | बुबोधयिषति "er wünscht zu belehren (zur Erkenntnis zu wecken)" |\n'
        ':::',

        '####  Beispiele:\n'
        '\n'
        '| कृ 8U | चिकीर्षति "er wünscht zu tun" |\n'
        '| --- | --- |\n'
        '| पत् 1P | पिपतिषति "er ist im Begriffe, zu fallen" |\n'
        '| चुर् 10U | चुचोरयिषति "er wünscht zu stehlen" |\n'
        '| बुध् Kaus. | बुबोधयिषति "er wünscht zu belehren (zur Erkenntnis zu wecken)" |',
        '60.6 Beispiele grammar-box removed'
    )

    # ── 60.6.1 Bildung → grammar-box ─────────────────────────────────────────
    content = replace_exact(content,
        '### 60.6.1. Bildung des Desiderativstammes\n'
        '\n'
        'Wurzeln der Präsensklassen 1 - 9:\n'
        '\n'
        'reduplizierte Wurzel + sa\n'
        '\n'
        'oder:\n'
        '\n'
        'reduplizierte Wurzel + i + ṣa\n'
        '\n'
        'Die Regeln zur Verwendung des Bindevokals -i- siehe bei Kielhorn, Grammatik § 443 - 445.\n'
        '\n'
        'Wurzeln der 10. Präsensklasse und Kausative:\n'
        '\n'
        'reduplizierter Präsensstamm + i + ṣa',

        '### 60.6.1. Bildung des Desiderativstammes\n'
        '\n'
        '::: grammar-box\n'
        '**Wurzeln der Präsensklassen 1 - 9:**\n'
        '\n'
        '**reduplizierte Wurzel + sa**\n'
        '\n'
        '**oder:**\n'
        '\n'
        '**reduplizierte Wurzel + i + ṣa**\n'
        '\n'
        'Die Regeln zur Verwendung des Bindevokals -i- siehe bei Kielhorn, Grammatik § 443 - 445.\n'
        '\n'
        '**Wurzeln der 10. Präsensklasse und Kausative:**\n'
        '\n'
        '**reduplizierter Präsensstamm + i + ṣa**\n'
        ':::',
        '60.6.1 Bildung grammar-box'
    )

    # ── 60.6.1 Gestalt der Wurzel → grammar-box (open) ───────────────────────
    content = replace_exact(content,
        ':::\n'
        '\n'
        'Gestalt der Wurzel:\n'
        '\n'
        '1.  Die Wurzel ist meist tiefstufig',

        ':::\n'
        '\n'
        '::: grammar-box\n'
        '**Gestalt der Wurzel:**\n'
        '\n'
        '1.  Die Wurzel ist meist tiefstufig',
        '60.6.1 Gestalt der Wurzel grammar-box open'
    )

    # ── 60.6.1 close Gestalt + open Zur Reduplikation ────────────────────────
    content = replace_exact(content,
        '            द्युत् » दिद्योतिष- / दिद्युतिष- "aufzublitzen wünschen"\n'
        '\n'
        'Zur Reduplikation:',

        '            द्युत् » दिद्योतिष- / दिद्युतिष- "aufzublitzen wünschen"\n'
        ':::\n'
        '\n'
        '::: grammar-box\n'
        '**Zur Reduplikation:**',
        '60.6.1 Gestalt close + Zur Reduplikation open'
    )

    # ── 60.6.1 close Zur Reduplikation + open Zu einigen Wurzeln ─────────────
    content = replace_exact(content,
        '3.  Die besondere Desiderativbildung bestimmter Wurzeln'
        ' siehe bei Kielhorn, Grammatik § 451.\n'
        '\n'
        ' Zu einigen Wurzeln werden Desiderative',

        '3.  Die besondere Desiderativbildung bestimmter Wurzeln'
        ' siehe bei Kielhorn, Grammatik § 451.\n'
        ':::\n'
        '\n'
        '::: grammar-box\n'
        '**Zu einigen Wurzeln werden Desiderative',
        '60.6.1 Zur Reduplikation close + Zu einigen Wurzeln open'
    )

    # ── 60.6.1 close Zu einigen Wurzeln box ──────────────────────────────────
    content = replace_exact(content,
        '**Zu einigen Wurzeln werden Desiderative ohne desiderative Bedeutung gebildet.'
        ' Zu diesen Desiderativen können Desiderative'
        ' mit desiderativer Bedeutung gebildet werden.\n'
        '\n'
        'Liste bei Kielhorn',

        '**Zu einigen Wurzeln werden Desiderative ohne desiderative Bedeutung gebildet.'
        ' Zu diesen Desiderativen können Desiderative'
        ' mit desiderativer Bedeutung gebildet werden.**\n'
        ':::\n'
        '\n'
        'Liste bei Kielhorn',
        '60.6.1 Zu einigen Wurzeln close'
    )

    # ── 60.6.2 Konjugation → :::: grammar-box (contains nested :::) ──────────
    content = replace_exact(content,
        '### 60.6.2. Konjugation des Desiderativs (सन्)\n'
        '\n'
        'Das Desiderativ ist - mit wenigen Ausnahmen - P, Ā bzw. U,'
        ' je nachdem, ob die zugrundeliegende Wurzel'
        ' (bzw. der zugrundeligende Verbalstamm) P, Ā oder U ist.\n'
        '\n'
        'Präsensstamm: Konjugation wie ein thematischer Stamm:\n'
        '\n'
        'यज् 1U:\n'
        '\n'
        '::: indent\n'
        'P: यियक्षति "er wünscht, für jemand anderen zu opfern"\n'
        'Ā: यियक्षते "er wünscht, für sich selbst (als Opferherr) zu opfern"\n'
        'Passiv: यियक्ष्यते "es wird zu opfern gewünscht"\n'
        ':::\n'
        '\n'
        'Perfekt: periphrastisch:\n'
        '\n'
        '::: indent\n'
        'आप् » ईप्स- » ईप्सां चकार "er wünschte zu erlangen"\n'
        ':::\n'
        '\n'
        'Aorist: iṣ-Aorist:\n'
        '\n'
        '::: indent\n'
        'आप् » ऐप्सिषम् (a + īps-i-ṣ-am)\n'
        ':::\n'
        '\n'
        'Futur: सेट्\n'
        '\n'
        '::: indent\n'
        'आप् » ईप्सिष्यामि\n'
        ':::\n'
        '\n'
        'Zur Bildung von Nomina agentis auf -u aus dem Desiderativstamm'
        ' siehe [Lektion 54](lektion54.md).',

        '### 60.6.2. Konjugation des Desiderativs (सन्)\n'
        '\n'
        ':::: grammar-box\n'
        '**Das Desiderativ ist - mit wenigen Ausnahmen - P, Ā bzw. U,'
        ' je nachdem, ob die zugrundeliegende Wurzel'
        ' (bzw. der zugrundeligende Verbalstamm) P, Ā oder U ist.**\n'
        '\n'
        '**Präsensstamm: Konjugation wie ein thematischer Stamm:**\n'
        '\n'
        'यज् 1U:\n'
        '\n'
        '::: indent\n'
        'P: यियक्षति "er wünscht, für jemand anderen zu opfern"\n'
        'Ā: यियक्षते "er wünscht, für sich selbst (als Opferherr) zu opfern"\n'
        'Passiv: यियक्ष्यते "es wird zu opfern gewünscht"\n'
        ':::\n'
        '\n'
        '**Perfekt: periphrastisch:**\n'
        '\n'
        '::: indent\n'
        'आप् » ईप्स- » ईप्सां चकार "er wünschte zu erlangen"\n'
        ':::\n'
        '\n'
        '**Aorist: iṣ-Aorist:**\n'
        '\n'
        '::: indent\n'
        'आप् » ऐप्सिषम् (a + īps-i-ṣ-am)\n'
        ':::\n'
        '\n'
        '**Futur: सेट्**\n'
        '\n'
        '::: indent\n'
        'आप् » ईप्सिष्यामि\n'
        ':::\n'
        '\n'
        '::::\n'
        '\n'
        'Zur Bildung von Nomina agentis auf -u aus dem Desiderativstamm'
        ' siehe [Lektion 54](lektion54.md).',
        '60.6.2 Konjugation grammar-box'
    )

    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print('lektion60.md: done.')


if __name__ == '__main__':
    fix_59()
    fix_60()
