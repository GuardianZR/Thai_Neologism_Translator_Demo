"""
pipeline.py
-----------
Orchestrator หลักที่รวมทุก module เข้าด้วยกัน
ขั้นตอน: Input -> Normalize -> Dictionary Map -> NLP Analyze -> Output
"""

import json
import os
import sys
from typing import Dict, Any

# เพิ่ม src ใน path
sys.path.insert(0, os.path.dirname(__file__))

from normalizer        import normalize_text
from dictionary_mapper import load_dictionary, map_sentence
from nlp_analyzer      import analyze


DEFAULT_DICT_PATH = os.path.join(os.path.dirname(__file__), "../data/slang_dict.json")


class ThaiNeologismTranslator:
    """
    Thai Neologism Translator — แปลภาษาเด็กแว้นเป็นภาษาไทยมาตรฐาน

    การใช้งาน:
        translator = ThaiNeologismTranslator()
        result = translator.translate("แกร พรุ่งนี้ไปสยามมมมมกัลป๊ะ")
        print(result["output"])
    """

    def __init__(self, dict_path: str = DEFAULT_DICT_PATH, fuzzy_threshold: int = 80):
        self.dictionary      = load_dictionary(dict_path)
        self.fuzzy_threshold = fuzzy_threshold

    def translate(self, text: str) -> Dict[str, Any]:
        """
        แปลข้อความ slang -> ภาษามาตรฐาน พร้อม metadata

        Returns:
            {
                "input":     ข้อความต้นฉบับ,
                "normalized": หลัง normalize,
                "output":    หลังแปลแล้ว,
                "analysis":  NLP analysis dict
            }
        """
        # Step 1: Normalize (ตัดอักษรซ้ำ)
        normalized = normalize_text(text)

        # Step 2: Dictionary Mapping
        translated = map_sentence(normalized, self.dictionary, self.fuzzy_threshold)

        # Step 3: NLP Analysis
        analysis = analyze(translated)

        return {
            "input":      text,
            "normalized": normalized,
            "output":     translated,
            "analysis":   analysis,
        }

    def translate_simple(self, text: str) -> str:
        """แปลแบบง่าย คืนแค่ข้อความผลลัพธ์"""
        return self.translate(text)["output"]


def main():
    """Demo CLI"""
    translator = ThaiNeologismTranslator()

    test_cases = [
        "แกร๊รรร พรุ่งนี้ไปสยามมมมมกัลป๊ะ",
        "รักเทอจุงเบยยยย",
        "เทอมันจัยร้ายมั่กๆ",
        "ฝันดีนร้าาาา",
        "วันนี้เหนื่อยมั่กกกก อยากลาออกจุงเบยยย",
    ]

    print("=" * 60)
    print("  Thai Neologism Translator — Demo")
    print("=" * 60)

    for text in test_cases:
        result = translator.translate(text)
        print(f"\nInput    : {result['input']}")
        print(f"Normalize: {result['normalized']}")
        print(f"Output   : {result['output']}")
        print(f"Sentiment: {result['analysis']['sentiment']}")
        print(f"Intent   : {result['analysis']['intent']}")

    print("\n" + "=" * 60)

    # Interactive mode
    print("\nโหมดทดสอบ (พิมพ์ 'exit' เพื่อออก):")
    while True:
        try:
            user_input = input(">>> ")
            if user_input.lower() in ("exit", "quit", "ออก"):
                break
            if user_input.strip():
                result = translator.translate(user_input)
                print(f"    -> {result['output']}")
                print(f"       [{result['analysis']['sentiment']} | {result['analysis']['intent']}]")
        except (KeyboardInterrupt, EOFError):
            break

    print("ลาก่อน!")


if __name__ == "__main__":
    main()
