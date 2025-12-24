from fastapi import APIRouter
from services.pdf_extractor import clean_text_dynamic, extract_pages
from services.image_generator import generate_image
from services.chunker import chunk_paragraphs, split_into_paragraphs
from services.nlp_engine import analyze_page
from services.prompt_builder import build_prompt

router = APIRouter(prefix="/image")

pages = []

def pages_loading():
    global pages
    if len(pages) == 0:
        print("Loading & processing PDF...")
        raw = extract_pages("data/short_story.pdf") 
        cleaned = clean_text_dynamic(raw)
        paragraphs = split_into_paragraphs(cleaned)
        pages.extend(chunk_paragraphs(paragraphs))
        print(f" Pages ready: {len(pages)}")


@router.post("/generate/{page}")
def generate(page: int):

    pages_loading() 

    if page < 1 or page > len(pages):
        return {"error": "Invalid page number"}

    page_text = pages[page - 1]["text"]
    analysis = analyze_page(page_text)
    prompt_data = build_prompt(analysis)
    image_b64 = generate_image(prompt_data)

    return {
        "page": page,
        "analysis": analysis,
        "prompt": prompt_data,
        "image": image_b64
    }