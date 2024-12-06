# texhelper/bibtex.py
import re

def capitalize_title(title):
    """Capitalize title field correctly for BibTeX"""
    exclude = {'and', 'or', 'nor', 'but', 'a', 'an', 'the', 'as', 'at', 'by', 'for', 'in', 'of', 'on', 'per', 'to', 'via'}
    words = title.split()
    capitalized_words = [
        word.capitalize() if (word.lower() not in exclude or i == 0 or i == len(words) - 1) else word.lower()
        for i, word in enumerate(words)
    ]
    return ' '.join(capitalized_words)

def process_bibtex(bib_content):
    """Process the content of a BibTeX file and capitalize titles"""
    processed_bib = []
    for line in bib_content:
        if line.strip().startswith("title={") and line.strip().endswith("},"):
            title_content = re.search(r"title={(.*)}", line).group(1)
            capitalized_title = capitalize_title(title_content)
            processed_bib.append(f"title={{{capitalized_title}}},\n")
        else:
            processed_bib.append(line)
    return processed_bib

