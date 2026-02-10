import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials

# ------------------ PAGE CONFIG ------------------
st.set_page_config(
    page_title="Product Catalog",
    layout="wide"
)

# ------------------ STYLING ------------------
st.markdown("""
<style>
body { background-color: #f8f9fa; }
.card {
    background: white;
    border-radius: 16px;
    padding: 15px;
    box-shadow: 0 6px 20px rgba(0,0,0,0.08);
    margin-bottom: 20px;
}
.price {
    font-size: 18px;
    font-weight: 700;
    color: #0d6efd;
}
.whatsapp {
    background-color: #25D366;
    color: white;
    padding: 10px;
    border-radius: 10px;
    text-align: center;
    text-decoration: none;
    display: block;
    margin-top: 10px;
    font-weight: 600;
}
</style>
""", unsafe_allow_html=True)

# ------------------ HERO SECTION ------------------
st.markdown("""
## 📦 Premium Product Catalog  
**Real photos & videos. Transparent prices. Updated live.**

🟢 Shared privately with our clients  
📍 Serving Erbil & Kurdistan
""")

st.divider()

# ------------------ GOOGLE SHEET AUTH ------------------
scope = [
    "https://www.googleapis.com/auth/spreadsheets.readonly",
    "https://www.googleapis.com/auth/drive.readonly",
]

credentials = Credentials.from_service_account_info(
    st.secrets["service_account"],
    scopes=scope
)

client = gspread.authorize(credentials)

@st.cache_data
def load_data():
    sheet_id = st.secrets["sheet"]["sheet_id"]
    sheet = client.open_by_key(sheet_id).sheet1
    return pd.DataFrame(sheet.get_all_records())

df = load_data()

if df.empty:
    st.warning("No products available.")
    st.stop()

# ------------------ FILTERS ------------------
col1, col2 = st.columns(2)

with col1:
    search = st.text_input("🔍 Search product")

with col2:
    categories = ["All"] + sorted(df["Category"].dropna().unique().tolist())
    selected_category = st.selectbox("📂 Category", categories)

if search:
    df = df[df["Name"].str.contains(search, case=False, na=False)]

if selected_category != "All":
    df = df[df["Category"] == selected_category]

# ------------------ PRODUCT GRID ------------------
cols = st.columns(3)

for i, row in df.iterrows():
    with cols[i % 3]:
        st.markdown('<div class="card">', unsafe_allow_html=True)

        url = row["URL"]

        # Media
        if any(url.lower().endswith(ext) for ext in ["jpg", "jpeg", "png", "webp"]):
            st.image(url, use_container_width=True)
        else:
            st.video(url)

        # Info
        st.subheader(row.get("Name", "Product"))
        st.caption(row.get("Category", ""))

        if row.get("Price"):
            st.markdown(f'<div class="price">💰 {row["Price"]}</div>', unsafe_allow_html=True)

        # WhatsApp button
        message = f"Hello, I am interested in {row.get('Name','this product')}"
        wa_link = f"https://wa.me/964XXXXXXXXX?text={message.replace(' ', '%20')}"

        st.markdown(
            f'<a class="whatsapp" href="{wa_link}" target="_blank">📲 Request this product</a>',
            unsafe_allow_html=True
        )

        st.markdown('</div>', unsafe_allow_html=True)

# ------------------ FOOTER ------------------
st.divider()
st.caption("🟢 Catalog updated automatically • Powered by Google Sheets")
