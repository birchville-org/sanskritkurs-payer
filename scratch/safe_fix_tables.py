import os

def fix_file_tables(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    in_table = False
    table_lines = []
    fixed_lines = []
    modified = False
    
    for line in lines:
        if '|' in line:
            if not in_table:
                in_table = True
                table_lines = []
            table_lines.append(line)
        else:
            if in_table:
                # End of table, process and fix it
                if len(table_lines) > 1:
                    counts = [l.count('|') for l in table_lines]
                    if len(set(counts)) > 1:
                        max_pipes = max(counts)
                        fixed_table = []
                        for tl in table_lines:
                            pipes = tl.count('|')
                            if pipes < max_pipes:
                                diff = max_pipes - pipes
                                stripped = tl.strip()
                                is_separator = len(stripped) > 0 and all(c in ' |:-' for c in stripped)
                                
                                newline = '\n' if tl.endswith('\n') else ''
                                content = tl.rstrip('\r\n')
                                
                                if is_separator:
                                    padding = ' --- |' * diff
                                else:
                                    padding = ' |' * diff
                                    
                                fixed_table.append(content + padding + newline)
                                modified = True
                            else:
                                fixed_table.append(tl)
                        fixed_lines.extend(fixed_table)
                    else:
                        fixed_lines.extend(table_lines)
                else:
                    fixed_lines.extend(table_lines)
                in_table = False
            fixed_lines.append(line)
            
    if in_table:
        if len(table_lines) > 1:
            counts = [l.count('|') for l in table_lines]
            if len(set(counts)) > 1:
                max_pipes = max(counts)
                fixed_table = []
                for tl in table_lines:
                    pipes = tl.count('|')
                    if pipes < max_pipes:
                        diff = max_pipes - pipes
                        stripped = tl.strip()
                        is_separator = len(stripped) > 0 and all(c in ' |:-' for c in stripped)
                        
                        newline = '\n' if tl.endswith('\n') else ''
                        content = tl.rstrip('\r\n')
                        
                        if is_separator:
                            padding = ' --- |' * diff
                        else:
                            padding = ' |' * diff
                            
                        fixed_table.append(content + padding + newline)
                        modified = True
                    else:
                        fixed_table.append(tl)
                fixed_lines.extend(fixed_table)
            else:
                fixed_lines.extend(table_lines)
        else:
            fixed_lines.extend(table_lines)
            
    if modified:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.writelines(fixed_lines)
        print(f"Fixed table mismatches in {file_path}")
    return modified

if __name__ == "__main__":
    lektionen_dir = 'docs/lektionen'
    fixed_count = 0
    for filename in os.listdir(lektionen_dir):
        if filename.endswith('.md'):
            path = os.path.join(lektionen_dir, filename)
            if fix_file_tables(path):
                fixed_count += 1
    print(f"Total files fixed: {fixed_count}")
