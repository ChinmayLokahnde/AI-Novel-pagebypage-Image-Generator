import fitz
import re
from collections import Counter

def extract_pages(file_path: str) -> list:
    doc = fitz.open(file_path)
    pages = [page.get_text("text") for page in doc]
    doc.close()
    return pages


def clean_text_dynamic(pages: list) -> str:

    
    split_pages = [page.splitlines() for page in pages]

    
    all_lines = [line.strip() for page in split_pages for line in page if line.strip()]
    freq = Counter(all_lines)
    page_count = len(pages)

    cleaned_pages = []

    for page in split_pages:
        new_lines = []
        for line in page:
            line = line.strip()

          
            if freq[line] > max(3, page_count * 0.4):
                continue

         
            if re.match(r"^[\*\-\–—]+$", line):
                continue

           
            if re.search(r"(https?://|www\.|@)", line):
                continue

            if len(line) <= 1:
                continue

            new_lines.append(line)

        cleaned_pages.append(" ".join(new_lines))  

    return "\n\n".join(cleaned_pages).strip()  


        