def build_prompt(analysis: dict) -> dict:
    # SUBJECT
    subject = analysis["characters"][0] if analysis["characters"] else "a lone person"

    # SCENE (must be singular & physical)
    scene = analysis.get("scene") or "a quiet train platform at night"

    # MOOD → lighting only
    mood = analysis.get("mood", "neutral")

    # VISUAL OBJECTS (physical only)
    visuals = [
        w for w in analysis.get("visual_keywords", [])
        if w.isalpha() and w.lower() not in {"last", "journey", "fear"}
    ][:5]

    visual_str = ", ".join(visuals)

    prompt = (
        f"Realistic cinematic photograph of {subject} standing in {scene}. "
        f"It is nighttime. The mood is {mood}. "
        f"Visible elements include {visual_str}. "
        "Natural human proportions, realistic body anatomy, "
        "35mm camera, shallow depth of field, natural lighting, "
        "documentary realism."
    )

    negative_prompt = (
        "fantasy, surreal, abstract, dreamlike, anime, cartoon, "
        "painterly, distorted anatomy, extra limbs, blurry, text, watermark"
    )

    return {
        "prompt": prompt,
        "negative_prompt": negative_prompt
    }
