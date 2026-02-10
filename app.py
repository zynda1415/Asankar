import streamlit as st
from product.load_data import load_data
from product.filters import apply_filters
from product.product_grid import show_product_grid

# Modular pages
from contactus import show_contact
from aboutas import show_about
from price import show_price_calculator

WHATSAPP_PHONE = "+9647501003839"  # your WhatsApp number

st.set_page_config(page_title="Company Catalog", layout="wide")
st.sidebar.image("logo.png", use_column_width=True)

page = st.sidebar.radio(
    "📌 Navigation",
    ("Products", "Price Calculating", "Contact Us", "About Us")
)

# ------------------ PAGES ------------------
if page == "Products":
    st.title("📦 Our Products")
    df = load_data()
    if df.empty or "URL" not in df.columns:
        st.error("No data found or 'URL' column missing in Google Sheet.")
        st.stop()

    df = apply_filters(df)

    view_mode = st.radio(
        "🔳 Select view mode",
        ("2 columns", "3 columns", "5 columns"),
        horizontal=True
    )
    columns_mode = {"2 columns":2, "3 columns":3, "5 columns":4}[view_mode]

    show_product_grid(df, WHATSAPP_PHONE, columns_mode)

elif page == "Price Calculating":
    show_price_calculator()

elif page == "Contact Us":
    show_contact(phone=WHATSAPP_PHONE, email="info@yourcompany.com")

elif page == "About Us":
    show_about()
