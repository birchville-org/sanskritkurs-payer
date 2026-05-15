import os
import re

directory = "/Volumes/SanDisk1TB/proj/Payer/docs/en/lektionen"

# Pattern to match "## Quiz: ..." followed by an optional blank line and the PayerQuiz tag
# This will match:
# ## Quiz: Something
#
# <PayerQuiz :questions="quizQuestions" />
pattern = re.compile(r'## Quiz:.*?\n\n<PayerQuiz :questions="quizQuestions" />\n?', re.DOTALL)

for filename in os.listdir(directory):
    if filename.endswith(".md"):
        path = os.path.join(directory, filename)
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        new_content = pattern.sub('', content)
        
        if new_content != content:
            print(f"Removing quiz from {filename}")
            with open(path, 'w', encoding='utf-8') as f:
                f.write(new_content)
        else:
            # Also check for the tag without the heading just in case
            tag_only_pattern = re.compile(r'<PayerQuiz :questions="quizQuestions" />\n?', re.DOTALL)
            new_content = tag_only_pattern.sub('', content)
            if new_content != content:
                print(f"Removing standalone quiz tag from {filename}")
                with open(path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
