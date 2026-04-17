"""
nlp_analyzer.py
---------------
วิเคราะห์ข้อความใน 3 ด้าน:
  1. POS Tagging + NER (ใช้ pythainlp)
  2. Sentiment Classification (rule-based + Wisesight patterns)
  3. Intent Classification (rule-based)
"""

import re
from typing import Dict, Any, List, Tuple

try:
    from pythainlp.tag import pos_tag
    from pythainlp.tokenize import word_tokenize
    PYTHAINLP_AVAILABLE = True
except ImportError:
    PYTHAINLP_AVAILABLE = False


# ---- Sentiment keywords (ขยายได้จาก Wisesight corpus) ----
POSITIVE_WORDS = {
    "รัก", "ชอบ", "ดี", "สุข", "สนุก", "เยี่ยม", "เจ๋ง", "ปัง",
    "น่ารัก", "หล่อ", "สวย", "อร่อย", "แนะนำ", "ประทับใจ", "ขอบคุณ"
}
NEGATIVE_WORDS = {
    "เกลียด", "แย่", "ห่วย", "โกรธ", "เบื่อ", "เหนื่อย", "เศร้า",
    "ร้าย", "ผิดหวัง", "ลาออก", "หมด", "ไม่ดี", "ไม่ชอบ", "เครียด"
}

# ---- Intent patterns ----
QUESTION_MARKERS = {"ไหม", "มั้ย", "ป๊ะ", "เปล่า", "ป่าว", "หรือ", "เหรอ", "ใช่ไหม", "ชิป๊ะ"}
GREETING_MARKERS = {"สวัสดี", "ฝันดี", "บาย", "หวัดดี", "ราตรีสวัสดิ์"}
COMMAND_MARKERS  = {"ไป", "มา", "ทำ", "เอา", "บอก", "ช่วย", "กรุณา"}


def get_pos_tags(tokens: List[str]) -> List[Tuple[str, str]]:
    """POS tagging ด้วย pythainlp (ถ้ามี)"""
    if PYTHAINLP_AVAILABLE:
        return pos_tag(tokens, corpus="orchid_ud")
    return [(t, "UNKNOWN") for t in tokens]


def extract_entities(tokens: List[str], pos_tags: List[Tuple[str, str]]) -> Dict[str, List[str]]:
    """
    NER แบบ rule-based เบื้องต้น:
    - PROPN (proper noun) จาก POS tagger -> ชื่อคน/สถานที่
    รองรับการขยายด้วย model จาก pythainlp ในอนาคต
    """
    entities = {"PERSON": [], "PLACE": [], "ORG": [], "OTHER": []}
    known_places = {"สยาม", "พารากอน", "เซ็นทรัล", "ทองหล่อ", "อโศก", "บางนา"}
    for token, tag in pos_tags:
        if token in known_places:
            entities["PLACE"].append(token)
        elif tag in ("PROPN", "NNP"):
            entities["PERSON"].append(token)
    return entities


def classify_sentiment(tokens: List[str]) -> str:
    """
    จำแนก sentiment: positive / negative / neutral
    ใช้ keyword matching เบื้องต้น (ขยายด้วย ML model ได้)
    """
    pos_count = sum(1 for t in tokens if t in POSITIVE_WORDS)
    neg_count = sum(1 for t in tokens if t in NEGATIVE_WORDS)

    if pos_count > neg_count:
        return "positive"
    elif neg_count > pos_count:
        return "negative"
    return "neutral"


def classify_intent(tokens: List[str]) -> str:
    """
    จำแนก intent: question / greeting / command / statement
    """
    token_set = set(tokens)
    if token_set & QUESTION_MARKERS:
        return "question"
    if token_set & GREETING_MARKERS:
        return "greeting"
    if token_set & COMMAND_MARKERS:
        return "command"
    return "statement"


def extract_keywords(tokens: List[str], pos_tags: List[Tuple[str, str]]) -> List[str]:
    """
    ดึงคำสำคัญ: คำนาม (NOUN/PROPN) และคำกริยา (VERB)
    """
    important_pos = {"NOUN", "PROPN", "VERB", "NN", "NNP", "VV"}
    return [token for token, tag in pos_tags if tag in important_pos]


def analyze(text: str) -> Dict[str, Any]:
    """
    วิเคราะห์ข้อความแบบครบวงจร

    Returns:
        dict ที่มี tokens, pos_tags, entities, sentiment, intent, keywords
    """
    if PYTHAINLP_AVAILABLE:
        tokens = word_tokenize(text, engine="newmm")
    else:
        tokens = text.split()

    pos_tags  = get_pos_tags(tokens)
    entities  = extract_entities(tokens, pos_tags)
    sentiment = classify_sentiment(tokens)
    intent    = classify_intent(tokens)
    keywords  = extract_keywords(tokens, pos_tags)

    return {
        "tokens":    tokens,
        "pos_tags":  pos_tags,
        "entities":  entities,
        "sentiment": sentiment,
        "intent":    intent,
        "keywords":  keywords,
    }


if __name__ == "__main__":
    import json
    samples = [
        "รักเธอจังเลย",
        "เธอนิสัยไม่ดีจริงๆ",
        "พรุ่งนี้ไปสยามกันไหม",
        "ฝันดีนะ",
    ]
    for s in samples:
        result = analyze(s)
        print(f"Text     : {s}")
        print(f"Sentiment: {result['sentiment']}")
        print(f"Intent   : {result['intent']}")
        print(f"Keywords : {result['keywords']}")
        print(f"Entities : {result['entities']}")
        print()
