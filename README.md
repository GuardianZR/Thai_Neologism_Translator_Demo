# 🔤 Thai Neologism Translator

แปลภาษาเด็กแว้น/ภาษาวิบัติบนโซเชียลมีเดียให้เป็นภาษาไทยมาตรฐาน
รองรับ Facebook, TikTok, Twitter/X ผ่าน Chrome Extension

---

## 📁 โครงสร้างโปรเจกต์

```
thai-neologism-translator/
├── data/
│   └── slang_dict.json       # คลัง slang -> คำมาตรฐาน (ขยายได้)
├── src/
│   ├── normalizer.py         # ตัดอักษรซ้ำ + normalize
│   ├── spell_corrector.py    # FuzzyWuzzy matching
│   ├── dictionary_mapper.py  # Search & Replace จาก dict
│   ├── nlp_analyzer.py       # POS, NER, Sentiment, Intent
│   ├── pipeline.py           # Orchestrator หลัก + CLI demo
│   └── api_server.py         # Flask API server
├── extension/
│   ├── manifest.json
│   ├── content.js            # Tooltip เมื่อ select ข้อความ
│   └── popup.html            # หน้า popup ของ Extension
├── tests/
│   └── test_pipeline.py
├── requirements.txt
└── README.md
```

---

## ⚙️ การติดตั้ง

### ข้อกำหนดเบื้องต้น
- Python 3.9 ขึ้นไป
- Google Chrome

### ขั้นตอน

**1. Clone หรือแตกไฟล์ ZIP**
```bash
cd thai-neologism-translator
```

**2. สร้าง Virtual Environment (แนะนำ)**
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

**3. ติดตั้ง Dependencies**
```bash
pip install -r requirements.txt
```

> หมายเหตุ: `pythainlp` จะดาวน์โหลด corpus อัตโนมัติเมื่อใช้ครั้งแรก
> ต้องการอินเทอร์เน็ตในครั้งแรก

---

## 🚀 การใช้งาน

### วิธีที่ 1 — Python CLI (ทดสอบด่วน)

```bash
cd src
python pipeline.py
```

จะแสดง demo และเปิดโหมด interactive ให้พิมพ์ทดสอบได้เลย

**ตัวอย่างผลลัพธ์:**
```
Input    : แกร๊รรร พรุ่งนี้ไปสยามมมมมกัลป๊ะ
Normalize: แกร พรุ่งนี้ไปสยามกัลป๊ะ
Output   : แก พรุ่งนี้ไปสยามกันไหม
Sentiment: neutral
Intent   : question
```

---

### วิธีที่ 2 — API Server + Chrome Extension

**ขั้นตอนที่ 1: เปิด API Server**
```bash
cd src
python api_server.py
```
เซิร์ฟเวอร์จะรันที่ `http://localhost:5000`

**ขั้นตอนที่ 2: ทดสอบ API**
```bash
curl -X POST http://localhost:5000/translate \
  -H "Content-Type: application/json" \
  -d '{"text": "รักเทอจุงเบยยยย"}'
```

**ขั้นตอนที่ 3: ติดตั้ง Chrome Extension**
1. เปิด Chrome → `chrome://extensions/`
2. เปิด **Developer mode** (มุมขวาบน)
3. คลิก **Load unpacked**
4. เลือกโฟลเดอร์ `extension/`
5. Extension จะปรากฏใน toolbar

**ขั้นตอนที่ 4: ใช้งาน**
- เข้า Facebook / TikTok / Twitter
- **เลือก (highlight) ข้อความ** ที่ต้องการแปล → tooltip จะแสดงผลอัตโนมัติ
- หรือคลิกไอคอน Extension เพื่อพิมพ์ข้อความเอง

---

### วิธีที่ 3 — ใช้ใน Python Code

```python
from src.pipeline import ThaiNeologismTranslator

translator = ThaiNeologismTranslator()

# แปลง่าย
result = translator.translate_simple("มั่กกกกเรยยยอ้ะเทอ")
print(result)  # -> มากเลยอะเธอ

# แปลพร้อม metadata
result = translator.translate("แกร พรุ่งนี้ไปสยามมมมมกัลป๊ะ")
print(result["output"])            # -> แก พรุ่งนี้ไปสยามกันไหม
print(result["analysis"]["intent"])  # -> question
```

---

## 🧪 การรัน Tests

```bash
pip install pytest
python -m pytest tests/ -v
```

---

## 📖 เพิ่มคำ Slang ใหม่

แก้ไขไฟล์ `data/slang_dict.json`:

```json
{
  "คำสแลง": "คำมาตรฐาน",
  "ชิมิ": "ใช่ไหม",
  "อิหยัง": "อะไร"
}
```

บันทึกและรีสตาร์ท API Server — ระบบจะโหลด dict ใหม่อัตโนมัติ

---

## 🔧 แก้ปัญหาเบื้องต้น

| ปัญหา | วิธีแก้ |
|-------|---------|
| `ModuleNotFoundError: pythainlp` | รัน `pip install pythainlp` |
| `ModuleNotFoundError: fuzzywuzzy` | รัน `pip install fuzzywuzzy python-Levenshtein` |
| Extension ไม่แสดง tooltip | ตรวจสอบว่า `api_server.py` กำลังรันอยู่ |
| Chrome บล็อก `localhost` | ใน `chrome://flags` ค้นหา "Insecure origins treated as secure" แล้วเพิ่ม `http://localhost:5000` |

---

## 📚 Libraries ที่ใช้

| Library | ใช้ทำอะไร |
|---------|-----------|
| [PyThaiNLP](https://github.com/PyThaiNLP/pythainlp) | ตัดคำ, POS tagging, normalize |
| [FuzzyWuzzy](https://github.com/seatgeek/fuzzywuzzy) | วัด string similarity |
| [Wisesight Sentiment](https://github.com/PyThaiNLP/wisesight-sentiment) | Dataset ภาษาไทยโซเชียลมีเดีย |
| Flask + Flask-CORS | API server |
