"""
spell_corrector.py
------------------
ใช้ FuzzyWuzzy วัดความคล้ายคลึงระหว่างคำที่รับเข้ามา
กับคำในพจนานุกรม slang เพื่อหาคู่ที่ใกล้เคียงที่สุด
"""

from fuzzywuzzy import fuzz
from typing import Optional


def find_best_match(word: str, dictionary: dict, threshold: int = 80) -> Optional[str]:
    """
    หาคำในพจนานุกรมที่คล้ายกับ word มากที่สุด
    คืนค่าคำมาตรฐาน ถ้า score >= threshold ไม่งั้นคืน None

    Args:
        word: คำที่ต้องการแก้ไข
        dictionary: dict ของ {slang: standard}
        threshold: ค่าขั้นต่ำ similarity (0-100)

    Returns:
        คำมาตรฐาน หรือ None ถ้าไม่พบคู่ที่ดีพอ
    """
    best_score = 0
    best_match = None

    for slang, standard in dictionary.items():
        score = fuzz.ratio(word, slang)
        if score > best_score:
            best_score = score
            best_match = standard

    if best_score >= threshold:
        return best_match
    return None


def correct_word(word: str, dictionary: dict, threshold: int = 80) -> str:
    """
    แก้ไขคำเดียว: ตรวจ exact match ก่อน จากนั้น fuzzy match
    """
    # Exact match ก่อนเสมอ
    if word in dictionary:
        return dictionary[word]

    # Fuzzy match
    result = find_best_match(word, dictionary, threshold)
    return result if result else word


if __name__ == "__main__":
    import json, os
    dict_path = os.path.join(os.path.dirname(__file__), "../data/slang_dict.json")
    with open(dict_path, encoding="utf-8") as f:
        slang_dict = json.load(f)

    test_words = ["มั่ก", "เทอ", "จัย", "กัล", "นร้า", "ชิป๊ะ"]
    for w in test_words:
        print(f"{w} -> {correct_word(w, slang_dict)}")
