import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials

# ------------------ CONFIG ------------------
st.set_page_config(
    page_title="Product Showcase",
    layout="wide"
)

# ------------------ AUTH ------------------
scope = [
    "https://www.googleapis.com/auth/spreadsheets.readonly",
    "https://www.googleapis.com/auth/drive.readonly",
]

credentials = Credentials.from_service_account_info(
    st.secrets["service_account"],
    scopes=scope
)

client = gspread.authorize(credentials)

# ------------------ LOAD DATA ------------------
@st.cache_data
def load_data():
    sheet_id = st.secrets["sheet"]["sheet_id"]
    sheet = client.open_by_key(sheet_id).sheet1
    data = sheet.get_all_records()
    return pd.DataFrame(data)

df = load_data()

# ------------------ UI ------------------
st.title("📦 Product Media Showcase")

if df.empty or "URL" not in df.columns:
    st.warning("No data found or 'URL' column is missing.")
    st.stop()

# ------------------ DISPLAY MEDIA ------------------
cols = st.columns(3)

for i, url in enumerate(df["URL"]):
    if not url:
        continue

    with cols[i % 3]:
        if any(url.lower().endswith(ext) for ext in [".jpg", ".jpeg", ".png", ".webp"]):
            st.image(url, use_container_width=True)

        elif any(ext in url.lower() for ext in ["youtube.com", "youtu.be", ".mp4"]):
            st.video(url)

        else:
            st.link_button("Open Media", url)
