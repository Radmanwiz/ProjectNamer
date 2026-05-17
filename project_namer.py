#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import datetime
import re
from typing import Tuple
import streamlit as object  # standard import is usually 'import streamlit as st'
import streamlit as st

# Set page config for a clean look
st.set_page_config(page_title="PROJECT NAMER (ALL CAPS)", layout="centered")

# --------- Jalali (Persian) date conversion (no external libs) ---------
def gregorian_to_jalali(gy: int, gm: int, gd: int) -> Tuple[int, int, int]:
    g_d_m = [0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334]
    if gy > 1600:
        jy = 979
        gy -= 1600
    else:
        jy = 0
        gy -= 621
    gy2 = gy + 1 if gm > 2 else gy
    days = 365 * gy + (gy2 + 3) // 4 - (gy2 + 99) // 100 + (gy2 + 399) // 400 - 80 + gd + g_d_m[gm - 1]
    jy += 33 * (days // 12053)
    days %= 12053
    jy += 4 * (days // 1461)
    days %= 1461
    if days > 365:
        jy += (days - 1) // 365
        days = (days - 1) % 365
    if days < 186:
        jm = 1 + days // 31
        jd = 1 + days % 31
    else:
        jm = 7 + (days - 186) // 30
        jd = 1 + (days - 186) % 30
    return jy, jm, jd

def today_jalali_str() -> str:
    t = datetime.date.today()
    jy, jm, jd = gregorian_to_jalali(t.year, t.month, t.day)
    return f"{jy:04d}-{jm:02d}-{jd:02d}"

def today_gregorian_str() -> str:
    t = datetime.date.today()
    return f"{t.year:04d}-{t.month:02d}-{t.day:02d}"

# --------- Formatting helpers ---------
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
    sep = (data.get("sep") or "_").upper()
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

    version = format_version(data.get("version", ""))

    parts = [project, subproject, date_str, datatype, version]
    name = sep.join(parts)

    ext = (data.get("ext") or "").strip().lstrip(".").upper()
    if ext:
        name = f"{name}.{ext}"
    return name

# --------- Streamlit UI ---------
st.title("PROJECT NAMER — ALL CAPS")
st.caption("Format: PROJECT_SUBPROJECT_DATE_#DATATYPE_VERSION[.EXT]")

# Grid layout using columns
col1, col2 = st.columns(2)

with col1:
    project = st.text_input("PROJECT", placeholder="TWOOD")
    datatype = st.text_input("DATATYPE (no # needed)", placeholder="IMAGE / VIDEO / LOGO")
    date = st.text_input("DATE (YYYY-MM-DD) — leave empty for today", placeholder="e.g. 1404-06-23")
    sep = st.text_input("SEPARATOR", value="_")

with col2:
    subproject = st.text_input("SUBPROJECT", placeholder="CHESSBOARD")
    version = st.text_input("VERSION", placeholder="V01 / 1 / 12")
    calendar = st.radio("CALENDAR", options=["JALALI", "GREGORIAN"], horizontal=True)
    ext = st.text_input("EXTENSION (optional)", placeholder="PSD / PNG / MP4")

# Compile data payload
payload = {
    "project": project,
    "subproject": subproject,
    "datatype": datatype,
    "version": version,
    "date": date,
    "calendar": calendar.lower(),
    "sep": sep,
    "ext": ext
}

# Generate final output
generated_name = build_name(payload)

st.write("---")
st.subheader("Preview")

# Streamlit code widget provides an instant, native "Copy" button out of the box
st.code(generated_name, language="text")
