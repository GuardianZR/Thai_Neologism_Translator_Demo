// content.js — inject "แปล" button เมื่อ user เลือกข้อความบนหน้าเว็บ

const API_URL = "https://thai-neologism-translator-demo.onrender.com/translate";

let tooltip = null;

// สร้าง tooltip element
function createTooltip() {
  const el = document.createElement("div");
  el.id = "tnt-tooltip";
  el.style.cssText = `
    position: fixed;
    z-index: 999999;
    background: #1a1a2e;
    color: #eee;
    padding: 8px 14px;
    border-radius: 8px;
    font-size: 14px;
    font-family: 'Sarabun', sans-serif;
    max-width: 320px;
    box-shadow: 0 4px 16px rgba(0,0,0,0.35);
    display: none;
    line-height: 1.6;
  `;
  document.body.appendChild(el);
  return el;
}

// แสดง tooltip ใกล้ cursor
function showTooltip(x, y, content) {
  if (!tooltip) tooltip = createTooltip();
  tooltip.innerHTML = content;
  tooltip.style.display = "block";

  // วางตำแหน่งให้ไม่เกินขอบจอ
  const rect = tooltip.getBoundingClientRect();
  const left = Math.min(x, window.innerWidth  - rect.width  - 16);
  const top  = Math.max(y - rect.height - 10, 10);

  tooltip.style.left = left + "px";
  tooltip.style.top  = top  + "px";
}

function hideTooltip() {
  if (tooltip) tooltip.style.display = "none";
}

// เรียก API แปลข้อความ
async function translateText(text) {
  try {
    const res = await fetch(API_URL, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ text }),
    });
    if (!res.ok) throw new Error("API error");
    return await res.json();
  } catch (e) {
    return null;
  }
}

// ฟังก์ชัน debounce
function debounce(fn, delay) {
  let timer;
  return (...args) => {
    clearTimeout(timer);
    timer = setTimeout(() => fn(...args), delay);
  };
}

// เมื่อ user เลือกข้อความ
const handleSelection = debounce(async (e) => {
  const selection = window.getSelection();
  const text = selection?.toString().trim();

  if (!text || text.length < 2) {
    hideTooltip();
    return;
  }

  // แสดง loading ก่อน
  showTooltip(e.clientX, e.clientY, `
    <div style="opacity:0.6;font-size:12px;">กำลังแปล...</div>
  `);

  const result = await translateText(text);

  if (!result) {
    showTooltip(e.clientX, e.clientY, `
      <div style="color:#f88;font-size:12px;">⚠ ไม่สามารถเชื่อมต่อ API ได้</div>
    `);
    return;
  }

  const sentimentIcon = {
    positive: "😊",
    negative: "😞",
    neutral:  "😐",
  }[result.sentiment] || "🔤";

  const intentLabel = {
    question:  "คำถาม",
    greeting:  "ทักทาย",
    command:   "คำสั่ง",
    statement: "บอกเล่า",
  }[result.intent] || result.intent;

  showTooltip(e.clientX, e.clientY, `
    <div style="margin-bottom:4px;font-size:11px;opacity:0.6;">ต้นฉบับ: ${result.input}</div>
    <div style="font-size:15px;font-weight:600;margin-bottom:6px;">📖 ${result.output}</div>
    <div style="font-size:11px;opacity:0.7;">${sentimentIcon} ${result.sentiment} · ${intentLabel}</div>
  `);
}, 400);

document.addEventListener("mouseup", handleSelection);

// ปิด tooltip เมื่อคลิกที่อื่น
document.addEventListener("mousedown", (e) => {
  if (tooltip && !tooltip.contains(e.target)) {
    hideTooltip();
  }
});
