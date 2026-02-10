import streamlit as st
from product.load_data import load_data
from product.product_grid import show_product_grid

# ------------------ PAGE CONFIG ------------------
st.set_page_config(
    page_title="Product Catalog",
    layout="wide"
)

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

🟢 Shared privately with our clients  
📍 Serving Erbil & Kurdistan
""")

st.divider()

# ------------------ LOAD DATA ------------------
df = load_data()

if df.empty or "URL" not in df.columns:
    st.error("No data found or 'URL' column missing in Google Sheet.")
    st.stop()

# ------------------ FILTERS ------------------
c1, c2 = st.columns(2)

with c1:
    search = st.text_input("🔍 Search product")

with c2:
    if "Category" in df.columns:
        categories = ["All"] + sorted(df["Category"].dropna().unique())
        selected_category = st.selectbox("📂 Category", categories)
    else:
        selected_category = "All"

if search and "Name" in df.columns:
    df = df[df["Name"].str.contains(search, case=False, na=False)]

if selected_category != "All" and "Category" in df.columns:
    df = df[df["Category"] == selected_category]

# ------------------ PRODUCT GRID ------------------
show_product_grid(df)

# ------------------ FOOTER ------------------
st.divider()
st.caption("🟢 Catalog updates automatically • Powered by Google Sheets")
