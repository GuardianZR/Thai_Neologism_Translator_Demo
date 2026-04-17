"""
api_server.py
-------------
Flask API server สำหรับให้ Chrome Extension เรียกใช้งาน
Endpoint: POST /translate  body: {"text": "..."}
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from flask import Flask, request, jsonify
from flask_cors import CORS
from pipeline import ThaiNeologismTranslator

app = Flask(__name__)
CORS(app)  # อนุญาต Chrome Extension เรียกข้ามโดเมน

translator = ThaiNeologismTranslator()


@app.route("/", methods=["GET"])
def health():
    return jsonify({"status": "ok", "message": "Thai Neologism Translator API"})


@app.route("/translate", methods=["POST"])
def translate():
    """
    แปลข้อความ slang -> ภาษามาตรฐาน

    Request body (JSON):
        { "text": "แกร พรุ่งนี้ไปสยามมมมมกัลป๊ะ" }

    Response:
        {
            "input": "...",
            "output": "...",
            "sentiment": "...",
            "intent": "..."
        }
    """
    data = request.get_json()
    if not data or "text" not in data:
        return jsonify({"error": "กรุณาส่ง JSON ที่มี key 'text'"}), 400

    text = data["text"].strip()
    if not text:
        return jsonify({"error": "ข้อความว่างเปล่า"}), 400

    result = translator.translate(text)

    return jsonify({
        "input":     result["input"],
        "output":    result["output"],
        "sentiment": result["analysis"]["sentiment"],
        "intent":    result["analysis"]["intent"],
        "keywords":  result["analysis"]["keywords"],
    })


@app.route("/batch", methods=["POST"])
def batch_translate():
    """
    แปลหลายประโยคพร้อมกัน

    Request body: { "texts": ["...", "...", ...] }
    """
    data = request.get_json()
    if not data or "texts" not in data:
        return jsonify({"error": "กรุณาส่ง JSON ที่มี key 'texts'"}), 400

    results = []
    for text in data["texts"]:
        r = translator.translate(text)
        results.append({
            "input":  r["input"],
            "output": r["output"],
        })

    return jsonify({"results": results})


if __name__ == "__main__":
    print("Starting Thai Neologism Translator API...")
    print("Endpoint: http://localhost:5000/translate")
    app.run(host="0.0.0.0", port=5000, debug=False)
