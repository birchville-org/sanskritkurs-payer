import os
import re

def audit_file(path):
    with open(path, 'r', encoding='utf-8', errors='replace') as f:
        content = f.read()
    
    issues = []
    
    # 1. Look for placeholders
    if "** **" in content:
        issues.append("Placeholders found")
        
    # 2. Look for common German terms
    german_terms = [
        "Numeri", "Zählformen", "Einzahl", "Zweizahl", "Mehrzahl",
        "Genera", "Geschlecht", "Maskulinum", "Femininum", "Neutrum",
        "Kasus", "Fälle", "Endungen", "Priesterstand", "Adelsstand", "Bauernstand"
    ]
    found_german = [term for term in german_terms if term.lower() in content.lower()]
    if found_german:
        issues.append(f"German terms: {', '.join(found_german)}")
        
    # 3. Look for mixed script words (Frankenstein)
    # [а-яА-Я] mixed with [a-zA-Z]
    frankenstein = re.findall(r'\b[а-яА-Я]+[a-zA-Z]+[а-яА-Я]*\b|\b[a-zA-Z]+[а-яА-Я]+[a-zA-Z]*\b', content)
    if frankenstein:
        issues.append(f"Frankenstein words: {', '.join(frankenstein)}")

    return issues

def main():
    docs_dir = "/Volumes/SanDisk1TB/proj/Payer/docs/bg/lektionen"
    report = []
    for root, dirs, files in os.walk(docs_dir):
        for file in files:
            if file.endswith('.md'):
                path = os.path.join(root, file)
                issues = audit_file(path)
                if issues:
                    report.append(f"File: {file}\nIssues:\n - " + "\n - ".join(issues))
                    
    with open("audit_results.txt", "w", encoding='utf-8') as f:
        f.write("\n\n".join(report))
    print(f"Audit complete. Found issues in {len(report)} files.")

if __name__ == "__main__":
    main()
