from services.pdf_extractor import extract_pages, clean_text_dynamic

PDF_PATH = "data/short_story.pdf"

def split_into_paragraphs(text: str):
    return [p.strip() for p in text.split("\n\n") if p.strip()]

def chunk_paragraphs(paragraphs, min_words=300, max_words=700):
    pages = []
    current = []
    word_count = 0
    page_num = 1

    for para in paragraphs:
        wc = len(para.split())

        if word_count + wc > max_words:
            pages.append({
                "page": page_num,
                "text": " ".join(current)
            })
            page_num += 1
            current = []
            word_count = 0

        current.append(para)
        word_count += wc

    if current:
        pages.append({
            "page": page_num,
            "text": " ".join(current)
        })

    return pages

# ---------- LOAD ONCE ----------
print("Loading PDF...")
raw_pages = extract_pages(PDF_PATH)
cleaned_story = clean_text_dynamic(raw_pages)
paragraphs = split_into_paragraphs(cleaned_story)
pages = chunk_paragraphs(paragraphs)

print(f"Pages Successfully Loaded: {len(pages)}")
