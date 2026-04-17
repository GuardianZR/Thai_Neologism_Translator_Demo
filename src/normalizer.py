"""
normalizer.py
-------------
ทำความสะอาดข้อความเบื้องต้น:
  1. ตัดอักษรซ้ำ (มั่กกกกก -> มั่ก)
  2. Normalize Unicode ด้วย pythainlp
"""

import re

try:
    from pythainlp.util import normalize as thai_normalize
    PYTHAINLP_AVAILABLE = True
except ImportError:
    PYTHAINLP_AVAILABLE = False


def remove_repeated_chars(text: str, max_repeat: int = 1) -> str:
    """
    ตัดอักษรซ้ำติดกันให้เหลือ max_repeat ตัว
    ตัวอย่าง: 'มั่กกกกก' -> 'มั่ก', 'นร้าาาา' -> 'นร้า'

    หมายเหตุ: วรรณยุกต์และสระที่ซ้อนกับพยัญชนะจะถูกจัดการโดย regex (\w)
    """
    # จับกลุ่มอักขระซ้ำ (ทั้ง Unicode Thai และ ASCII)
    pattern = r'(.)\1{' + str(max_repeat) + r',}'
    return re.sub(pattern, r'\1' * max_repeat, text)


def normalize_text(text: str) -> str:
    """
    Normalize ข้อความภาษาไทย:
      - ตัดอักษรซ้ำ
      - ใช้ pythainlp.normalize ถ้ามี (แก้ spacing สระ ฯลฯ)
    """
    text = remove_repeated_chars(text, max_repeat=1)

    if PYTHAINLP_AVAILABLE:
        text = thai_normalize(text)

    # ลบ whitespace ซ้ำ
    text = re.sub(r'\s+', ' ', text).strip()
    return text


if __name__ == "__main__":
    samples = [
        "มั่กกกกกเรยยยอ้ะเทอ",
        "แกร๊รรร พรุ่งนี้ไปสยามมมมมกัลป๊ะ",
        "รักเทอจุงเบยยยย",
        "ฝันดีนร้าาาา",
    ]
    for s in samples:
        print(f"Input : {s}")
        print(f"Output: {normalize_text(s)}")
        print()
