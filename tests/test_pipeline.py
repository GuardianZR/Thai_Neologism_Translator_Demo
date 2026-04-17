"""
test_pipeline.py
----------------
Unit tests สำหรับ Thai Neologism Translator
รัน: python -m pytest tests/ -v
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../src"))

from normalizer import remove_repeated_chars, normalize_text
from spell_corrector import correct_word


# ---- Normalizer tests ----

def test_remove_single_repeated():
    assert remove_repeated_chars("มั่กกกกก") == "มั่ก"

def test_remove_vowel_repeated():
    assert remove_repeated_chars("นร้าาาา") == "นร้า"

def test_no_change_normal():
    result = remove_repeated_chars("สวัสดี")
    assert result == "สวัสดี"

def test_normalize_full():
    result = normalize_text("แกร๊รรร พรุ่งนี้ไปสยามมมมมกัลป๊ะ")
    # หลัง normalize ต้องไม่มีอักษรซ้ำเกิน 1 ตัว
    import re
    assert not re.search(r'(.)\1{1,}', result)


# ---- Spell Corrector tests ----

SAMPLE_DICT = {
    "เทอ": "เธอ",
    "จัย": "ใจ",
    "มั่ก": "มาก",
    "กัล": "กัน",
    "นร้า": "นะ",
}

def test_exact_match():
    assert correct_word("เทอ", SAMPLE_DICT) == "เธอ"

def test_exact_match_2():
    assert correct_word("จัย", SAMPLE_DICT) == "ใจ"

def test_unknown_word_passthrough():
    # คำที่ไม่อยู่ใน dict ควรคืนคำเดิม (score ต่ำกว่า threshold)
    result = correct_word("สวัสดี", SAMPLE_DICT, threshold=95)
    assert result == "สวัสดี"


# ---- Pipeline tests ----

def test_pipeline_import():
    from pipeline import ThaiNeologismTranslator
    t = ThaiNeologismTranslator()
    assert t is not None

def test_pipeline_translate_simple():
    from pipeline import ThaiNeologismTranslator
    t = ThaiNeologismTranslator()
    result = t.translate("ฝันดีนร้า")
    assert "input"  in result
    assert "output" in result
    assert "analysis" in result
    assert result["input"] == "ฝันดีนร้า"

def test_pipeline_sentiment():
    from pipeline import ThaiNeologismTranslator
    t = ThaiNeologismTranslator()
    result = t.translate("รักเธอมาก")
    assert result["analysis"]["sentiment"] in ("positive", "negative", "neutral")

def test_pipeline_intent_question():
    from pipeline import ThaiNeologismTranslator
    t = ThaiNeologismTranslator()
    result = t.translate("พรุ่งนี้ไปสยามกันไหม")
    assert result["analysis"]["intent"] == "question"
