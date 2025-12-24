from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline
import torch
import spacy
import nltk

# Load once
nlp_ner = spacy.load("en_core_web_sm")

# Make sure these are installed ONCE (not per request)
# Run manually once if needed:
# python -m nltk.downloader punkt averaged_perceptron_tagger
#
# Comment them out in production
# nltk.download("punkt")
# nltk.download("averaged_perceptron_tagger")

MODEL_NAME = "t5-base"
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME)

emotion_analyzer = pipeline(
    "text-classification",
    model="j-hartmann/emotion-english-distilroberta-base"
)

# ---------------- SUMMARY ----------------
def summarize_text(text: str, max_tokens: int = 80) -> str:
    if not text.strip():
        return ""

    input_text = "summarize: " + text.strip()
    inputs = tokenizer(
        input_text,
        return_tensors="pt",
        max_length=512,
        truncation=True
    )

    with torch.no_grad():
        output_ids = model.generate(
            **inputs,
            max_length=max_tokens,
            min_length=20,
            num_beams=4,
            no_repeat_ngram_size=3
        )

    return tokenizer.decode(output_ids[0], skip_special_tokens=True).strip()

# ---------------- VISUAL KEYWORDS ----------------
def extract_visual_keywords(text: str, max_keywords=10):
    tokens = nltk.word_tokenize(text)
    tagged = nltk.pos_tag(tokens)

    keywords = [
        word.lower()
        for word, pos in tagged
        if pos in ("NN", "NNS", "JJ") and len(word) > 3
    ]

    return list(dict.fromkeys(keywords))[:max_keywords]

# ---------------- ENTITIES ----------------
def extract_entities(text: str):
    doc = nlp_ner(text)
    characters = []
    locations = []

    for ent in doc.ents:
        if ent.label_ == "PERSON":
            characters.append(ent.text)
        elif ent.label_ in ("GPE", "LOC", "FAC"):
            locations.append(ent.text)

    return list(set(characters)), list(set(locations))

# ---------------- MOOD ----------------
def detect_mood(text: str) -> str:
    try:
        result = emotion_analyzer(text[:400])[0]
        return result["label"].lower()
    except Exception:
        return "neutral"

# ---------------- LOCATION ENHANCEMENT ----------------
LOCATION_WORDS = [
    "island", "dock", "port", "beach", "ocean", "sea", "shore",
    "patio", "house", "room", "cottage", "resort", "boat"
]

def enhance_location(text: str, ner_locations):
    if ner_locations:
        return ner_locations[0]

    found = [w for w in LOCATION_WORDS if w in text.lower()]
    return ", ".join(found) if found else None

# ---------------- PAGE ANALYSIS ----------------
def analyze_page(text: str) -> dict:
    summary = summarize_text(text)
    characters, locations = extract_entities(text)
    visuals = extract_visual_keywords(text)
    mood = detect_mood(text)
    location = enhance_location(text, locations)

    return {
        "summary": summary,
        "characters": characters,
        "location": location,
        "mood": mood,
        "visual_keywords": visuals
    }
