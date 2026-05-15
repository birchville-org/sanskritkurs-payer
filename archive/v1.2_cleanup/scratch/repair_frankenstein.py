import os
import re

# Exact replacements for the most common mangled terms
EXACT_MAP = {
    'प्रथma': 'प्रथमा',
    'क्षtriया': 'क्षत्रिया',
    'क्षtriयान्': 'क्षत्रियान्',
    'क्षत्रियाञ्जयti': 'क्षत्रियाञ्जयति',
    'रिpuः': 'रिपुः',
    'धेnu': 'धेनु',
    'श्रुti': 'श्रुति',
    'अтиस्तुti': 'अतिस्तुति',
    'अत्युkti': 'अत्युक्ति',
    'यजन्ti': 'यजन्ति',
    'तुदाdi': 'तुदादि',
    'करोti': 'करोति',
    'जयti': 'जयति',
    'आप्नोti': 'आप्नोति',
    'शृणोti': 'शृणोति',
    'तनोti': 'तनोति',
    'वसti': 'वसति',
    'विшti': 'विशति',
    'विशti': 'विशति',
    'शाक्यमुniः': 'शाक्यमुनिः',
    'वागर्थप्रतिपत्तye': 'वागर्थप्रतिपत्तये',
    'संन्याsiन्': 'संन्यासिन्',
    'पшupatiनाथ': 'पशुपतिनाथ',
    'neपाल': 'नेपाल',
    'चन्द्रकीrti': 'चन्द्रकीर्ति',
    'brāhमṇї': 'ब्राह्मणी',
    'गुrvi': 'गुर्वी',
    'इतra': 'इतरा',
    'निdarśakasarvanāmāni': 'निदर्शकसर्वनमनि',
    'काni': 'कानि',
    'तद्धित-суфикс': 'суфикс тадхита',
    'कृत्-суфикс': 'суфикс крит',
    'А-склонеniя': 'А-склонения',
    'U-склонеniя': 'U-склонения',
    'каузативum': 'каузатив',
    'абсолютивum': 'абсолютив',
    'инфинитивum': 'инфинитив',
    'наречиеial': 'наречие',
    'лицеalendungen': 'лични окончания',
    'време)s': 'време)',
    'основаs': 'основа',
    'пасивs': 'пасив',
    'футурs': 'футур',
    'падежs': 'падеж',
    'даṇḍanīти': 'daṇḍanīti',
    'daṇḍanīти': 'daṇḍanīti',
    'catvāро': 'catvāro',
    'А-склонения': 'А-склонения', # already correct
}

def repair_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    orig_content = content
    
    # 1. Apply Exact Replacements (longest first to avoid partial matches)
    for err, fix in sorted(EXACT_MAP.items(), key=lambda x: len(x[0]), reverse=True):
        content = content.replace(err, fix)
        
    # 2. Apply regex for common suffixes in BG files
    if '/bg/' in path:
        # Remove trailing 's' from Cyrillic words (German Genitive remnant)
        content = re.sub(r'([\u0400-\u04FF]+)s\b', r'\1', content)
        # Remove trailing 'um' from Cyrillic words (Latin remnant)
        content = re.sub(r'([\u0400-\u04FF]+)um\b', r'\1', content)
        
    # 3. Fix IAST mangled with Cyrillic (specific suffixes)
    content = content.replace('nīти', 'nīti')
    content = content.replace('vāро', 'vāro')
    content = content.replace('tiः', 'tiḥ')
    content = content.replace('ktiः', 'ktiḥ')
    
    if content != orig_content:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

def main():
    docs_dir = "/Volumes/SanDisk1TB/proj/Payer/docs"
    count = 0
    for root, dirs, files in os.walk(docs_dir):
        if 'node_modules' in root: continue
        for file in files:
            if file.endswith('.md'):
                if repair_file(os.path.join(root, file)):
                    count += 1
    print(f"Repaired {count} files.")

if __name__ == "__main__":
    main()
