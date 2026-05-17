#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import datetime
from typing import Tuple
from flask import Flask, request, jsonify, Response

app = Flask(__name__)

# --------- Jalali (Persian) date conversion (no external libs) ---------
def gregorian_to_jalali(gy: int, gm: int, gd: int) -> Tuple[int, int, int]:
    g_d_m = [0,31,59,90,120,151,181,212,243,273,304,334]
    if gy > 1600:
        jy = 979
        gy -= 1600
    else:
        jy = 0
        gy -= 621
    gy2 = gy + 1 if gm > 2 else gy
    days = 365*gy + (gy2+3)//4 - (gy2+99)//100 + (gy2+399)//400 - 80 + gd + g_d_m[gm-1]
    jy += 33*(days//12053)
    days %= 12053
    jy += 4*(days//1461)
    days %= 1461
    if days > 365:
        jy += (days-1)//365
        days = (days-1)%365
    if days < 186:
        jm = 1 + days//31
        jd = 1 + days%31
    else:
        jm = 7 + (days-186)//30
        jd = 1 + (days-186)%30
    return jy, jm, jd

def today_jalali_str() -> str:
    t = datetime.date.today()
    jy, jm, jd = gregorian_to_jalali(t.year, t.month, t.day)
    return f"{jy:04d}-{jm:02d}-{jd:02d}"

def today_gregorian_str() -> str:
    t = datetime.date.today()
    return f"{t.year:04d}-{t.month:02d}-{t.day:02d}"

# --------- Formatting helpers ---------
import re
SAFE_CHARS_RE = re.compile(r"[^A-Z0-9#\-]+")

def to_token(s: str) -> str:
    s = (s or "").strip().upper().replace(" ", "-")
    s = SAFE_CHARS_RE.sub("", s)
    return s if s else "UNTITLED"

def format_version(v: str) -> str:
    v = (v or "").strip().upper()
    if not v:
        return "V01"
    if not v.startswith("V"):
        v = "V" + v
    m = re.match(r"V(\d+)$", v)
    if m:
        return f"V{int(m.group(1)):02d}"
    return v

def build_name(data: dict) -> str:
    project = to_token(data.get("project", ""))
    subproject = to_token(data.get("subproject", ""))
    sep = (data.get("sep") or "_").upper()  # keep ALL CAPS style even for separator (underscore unaffected)
    cal = (data.get("calendar") or "jalali").lower()
    date_override = (data.get("date") or "").strip().upper()

    if date_override:
        date_str = date_override
    else:
        date_str = today_jalali_str() if cal == "jalali" else today_gregorian_str()
    date_str = date_str.upper()

    datatype = to_token(data.get("datatype", ""))
    if not datatype.startswith("#"):
        datatype = "#" + datatype
    if not datatype.startswith("#"):  # in case sanitization removed '#'
        datatype = "#" + datatype

    version = format_version(data.get("version", ""))

    parts = [project, subproject, date_str, datatype, version]
    name = sep.join(parts)

    ext = (data.get("ext") or "").strip().lstrip(".").upper()
    if ext:
        name = f"{name}.{ext}"
    return name

# --------- Routes ---------
@app.route("/", methods=["GET"])
def index():
    html = f"""
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width,initial-scale=1" />
<title>PROJECT NAMER (ALL CAPS)</title>
<style>
  :root {{
    --bg:#0b0f14; --card:#121821; --ink:#e7f0ff; --muted:#a9b6c8; --accent:#7ea6ff; --ok:#8cffb7;
    --border:#1e2632;
  }}
  * {{ box-sizing: border-box; }}
  body {{
    margin:0; font-family: ui-sans-serif, system-ui, -apple-system, Segoe UI, Roboto, Helvetica, Arial;
    background:linear-gradient(180deg,#0b0f14 0%,#0e1420 100%); color:var(--ink);
    min-height:100vh; display:flex; align-items:center; justify-content:center; padding:24px;
  }}
  .wrap {{ width: min(980px, 100%); }}
  .card {{
    background:var(--card); border:1px solid var(--border); border-radius:18px;
    padding:22px; box-shadow: 0 10px 30px rgba(0,0,0,.35);
  }}
  h1 {{ margin:0 0 8px; font-size: clamp(20px, 3.5vw, 28px); letter-spacing: .6px; }}
  p.sub {{ margin:0 0 18px; color:var(--muted); }}
  .grid {{ display:grid; grid-template-columns: repeat(2, minmax(0,1fr)); gap:14px; }}
  .row {{ display:flex; gap:10px; align-items:center; }}
  label {{ font-size:12px; letter-spacing:.4px; color:var(--muted); display:block; margin-bottom:6px; }}
  input[type="text"], select {{
    width:100%; padding:10px 12px; border-radius:10px; border:1px solid var(--border);
    background:#0f1520; color:var(--ink); outline:none;
  }}
  input[type="text"]:focus, select:focus {{ border-color: var(--accent); }}
  .radio-group {{ display:flex; gap:10px; }}
  .pill {{
    display:inline-flex; align-items:center; gap:8px; background:#0f1520; border:1px solid var(--border);
    border-radius:999px; padding:8px 12px; cursor:pointer; user-select:none;
  }}
  .pill input {{ accent-color: var(--accent); }}
  .preview {{
    margin-top:18px; padding:14px; background:#0f1520; border:1px dashed var(--border);
    border-radius:12px; font-family: ui-monospace, SFMono-Regular, Menlo, monospace;
    word-break: break-all;
  }}
  .btns {{ display:flex; gap:10px; margin-top:12px; flex-wrap:wrap; }}
  button {{
    background:linear-gradient(180deg, #1a2333, #131a27); color:var(--ink);
    border:1px solid var(--border); padding:10px 14px; border-radius:12px;
    cursor:pointer; letter-spacing:.4px;
  }}
  button.primary {{ border-color:#36518f; }}
  .note {{ color:var(--muted); font-size:12px; margin-top:8px; }}
  .ok {{ color: var(--ok); font-size:12px; display:none; }}
  @media (max-width: 720px) {{
    .grid {{ grid-template-columns: 1fr; }}
  }}
</style>
</head>
<body>
<div class="wrap">
  <div class="card">
    <h1>PROJECT NAMER — ALL CAPS</h1>
    <p class="sub">Format: <b>PROJECT_SUBPROJECT_DATE_#DATATYPE_VERSION[.EXT]</b></p>

    <div class="grid">
      <div>
        <label>PROJECT</label>
        <input type="text" id="project" placeholder="TWOOD" />
      </div>
      <div>
        <label>SUBPROJECT</label>
        <input type="text" id="subproject" placeholder="CHESSBOARD" />
      </div>
      <div>
        <label>DATATYPE (no # needed, we add it)</label>
        <input type="text" id="datatype" placeholder="IMAGE / VIDEO / LOGO" />
      </div>
      <div>
        <label>VERSION</label>
        <input type="text" id="version" placeholder="V01 / 1 / 12" />
      </div>
      <div>
        <label>DATE (YYYY-MM-DD) — leave empty for today</label>
        <input type="text" id="date" placeholder="e.g. 1404-06-23 or 2025-09-14" />
      </div>
      <div>
        <label>CALENDAR</label>
        <div class="radio-group">
          <label class="pill"><input type="radio" name="calendar" value="jalali" checked/> JALALI</label>
          <label class="pill"><input type="radio" name="calendar" value="gregorian"/> GREGORIAN</label>
        </div>
      </div>
      <div>
        <label>SEPARATOR</label>
        <input type="text" id="sep" value="_" />
      </div>
      <div>
        <label>EXTENSION (optional)</label>
        <input type="text" id="ext" placeholder="PSD / PNG / MP4" />
      </div>
    </div>

    <div class="preview" id="preview">—</div>
    <div class="btns">
      <button class="primary" id="copyBtn">Copy</button>
      <button id="resetBtn">Reset</button>
      <span class="ok" id="copied">Copied!</span>
    </div>
</div>

<script>
function collect() {{
  const cal = document.querySelector('input[name="calendar"]:checked')?.value || "jalali";
  return {{
    project: document.getElementById("project").value,
    subproject: document.getElementById("subproject").value,
    datatype: document.getElementById("datatype").value,
    version: document.getElementById("version").value,
    date: document.getElementById("date").value,
    calendar: cal,
    sep: document.getElementById("sep").value,
    ext: document.getElementById("ext").value
  }};
}}

async function refresh() {{
  const data = collect();
  const res = await fetch("/generate", {{
    method: "POST",
    headers: {{ "Content-Type": "application/json" }},
    body: JSON.stringify(data)
  }});
  const j = await res.json();
  document.getElementById("preview").textContent = j.name || "—";
}}

["project","subproject","datatype","version","date","sep","ext"].forEach(id => {{
  document.getElementById(id).addEventListener("input", refresh);
}});
document.querySelectorAll('input[name="calendar"]').forEach(r => r.addEventListener("change", refresh));

document.getElementById("copyBtn").addEventListener("click", async () => {{
  const text = document.getElementById("preview").textContent;
  try {{
    await navigator.clipboard.writeText(text);
    const ok = document.getElementById("copied");
    ok.style.display = "inline";
    setTimeout(() => ok.style.display = "none", 1200);
  }} catch (e) {{
    alert("Copy failed. Select and use ⌘C/CTRL+C.");
  }}
}});

document.getElementById("resetBtn").addEventListener("click", () => {{
  ["project","subproject","datatype","version","date","sep","ext"].forEach(id => document.getElementById(id).value = id==="sep" ? "_" : "");
  document.querySelector('input[value="jalali"]').checked = true;
  refresh();
}});

window.addEventListener("load", refresh);
</script>
</body>
</html>
    """
    return Response(html, mimetype="text/html")

@app.route("/generate", methods=["POST"])
def generate():
    data = request.get_json(force=True, silent=True) or {}
    name = build_name(data)
    return jsonify({"name": name})

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5003))  # Render sets PORT
    app.run(host="0.0.0.0", port=port, debug=False)
