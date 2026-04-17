"""
dictionary_mapper.py
--------------------
โหลดและจัดการ slang dictionary
แปลงคำในประโยคโดยใช้ exact match + fuzzy fallback
"""

import json
import os
from typing import Dict

try:
    from pythainlp.tokenize import word_tokenize
    PYTHAINLP_AVAILABLE = True
except ImportError:
    PYTHAINLP_AVAILABLE = False

from spell_corrector import correct_word


DEFAULT_DICT_PATH = os.path.join(os.path.dirname(__file__), "../data/slang_dict.json")


def load_dictionary(path: str = DEFAULT_DICT_PATH) -> Dict[str, str]:
    """โหลด slang dictionary จาก JSON"""
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def tokenize(text: str):
    """ตัดคำภาษาไทย"""
    if PYTHAINLP_AVAILABLE:
        return word_tokenize(text, engine="newmm")
    # fallback: แยกด้วย whitespace
    return text.split()


def map_sentence(text: str, dictionary: Dict[str, str], fuzzy_threshold: int = 80) -> str:
    """
    แปลงคำ slang ในประโยคให้เป็นภาษามาตรฐาน

    Args:
        text: ประโยคที่รับเข้า (ผ่าน normalize แล้ว)
        dictionary: slang dict
        fuzzy_threshold: ความแม่นยำขั้นต่ำสำหรับ fuzzy match

    Returns:
        ประโยคที่แปลงแล้ว
    """
    tokens = tokenize(text)
    corrected = []
    for token in tokens:
        corrected.append(correct_word(token, dictionary, fuzzy_threshold))
    return "".join(corrected) if PYTHAINLP_AVAILABLE else " ".join(corrected)


if __name__ == "__main__":
    d = load_dictionary()
    sentences = [
        "รักเทอจุงเบย",
        "แกร พรุ่งนี้ไปสยามกัลป๊ะ",
        "เทอมันจัยร้าย",
        "ฝันดีนร้า",
    ]
    for s in sentences:
        print(f"Input : {s}")
        print(f"Output: {map_sentence(s, d)}")
        print()
