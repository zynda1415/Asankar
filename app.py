import streamlit as st
from product.load_data import load_data
from product.filters import apply_filters
from product.product_grid import show_product_grid

# ------------------ CONFIG ------------------
st.set_page_config(page_title="Product Catalog", layout="wide")

WHATSAPP_PHONE = "964XXXXXXXXX"  # ← your real number

# ------------------ STYLE ------------------
st.markdown("""
<style>
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

# ------------------ HERO ------------------
st.markdown("""
## 📦 Premium Product Catalog  
**Real photos & videos • Transparent prices • Updated live**
""")

st.divider()

# ------------------ DATA ------------------
df = load_data()

if df.empty or "URL" not in df.columns:
    st.error("No data found or 'URL' column missing.")
    st.stop()

df = apply_filters(df)

# ------------------ VIEW MODE ------------------
view_mode = st.radio(
    "🔳 Select view mode",
    ("4 products square", "2 columns", "3 columns", "5 columns")
)

if view_mode == "4 products square":
    columns_mode = 1
elif view_mode == "2 columns":
    columns_mode = 2
elif view_mode == "3 columns":
    columns_mode = 3
else:
    columns_mode = 4

# ------------------ PRODUCT GRID ------------------
show_product_grid(df, WHATSAPP_PHONE, columns_mode)

# ------------------ FOOTER ------------------
st.divider()
st.caption("🟢 Auto-updated • Google Sheets backend")
