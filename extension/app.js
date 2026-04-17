 const API = "http://localhost:5000/translate";

    document.getElementById("btn-translate").addEventListener("click", async () => {
      const text = document.getElementById("input").value.trim();
      if (!text) return;

      const resultEl     = document.getElementById("result");
      const outputEl     = document.getElementById("output-text");
      const metaEl       = document.getElementById("meta");

      resultEl.style.display = "block";
      outputEl.className  = "output-text loading";
      outputEl.textContent = "กำลังแปล...";
      metaEl.textContent  = "";

      try {
        const res = await fetch(API, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ text }),
        });

        if (!res.ok) throw new Error();
        const data = await res.json();

        outputEl.className  = "output-text";
        outputEl.textContent = data.output;

        const icons = { positive: "😊", negative: "😞", neutral: "😐" };
        const intents = { question: "คำถาม", greeting: "ทักทาย", command: "คำสั่ง", statement: "บอกเล่า" };

        metaEl.textContent =
          `${icons[data.sentiment] || "🔤"} ${data.sentiment} · ${intents[data.intent] || data.intent}`;

      } catch {
        outputEl.className  = "output-text error";
        outputEl.textContent = "⚠ ไม่สามารถเชื่อมต่อ API ได้ กรุณาตรวจสอบว่า api_server.py กำลังทำงานอยู่";
        metaEl.textContent  = "";
      }
    });

    // กด Enter แปลได้เลย
    document.getElementById("input").addEventListener("keydown", (e) => {
      if (e.key === "Enter" && e.ctrlKey) {
        document.getElementById("btn-translate").click();
      }
    });