import streamlit as st
from product.load_data import load_data
from product.filters import apply_filters
from product.product_grid import show_product_grid
from product.whatsapp import build_whatsapp_link

# ------------------ CONFIG ------------------
st.set_page_config(
    page_title="Company Catalog",
    layout="wide"
)

WHATSAPP_PHONE = "964XXXXXXXXX"  # ← your WhatsApp number

# ------------------ SIDEBAR ------------------
st.sidebar.image("logo.png", use_column_width=True)  # ← replace with your logo path

page = st.sidebar.radio(
    "📌 Navigation",
    ("Products", "Price Calculating", "Contact Us", "About Us")
)

# ------------------ PAGE: PRODUCTS ------------------
if page == "Products":
    st.title("📦 Products")

    # Load and filter data
    df = load_data()
    if df.empty or "URL" not in df.columns:
        st.error("No data found or 'URL' column missing in Google Sheet.")
        st.stop()

    df = apply_filters(df)

    # View mode selector
    view_mode = st.radio(
        "🔳 Select view mode",
        ("2 columns", "3 columns", "5 columns")
    )
    columns_mode = {"2 columns":2, "3 columns":3, "5 columns":4}[view_mode]

    # Show products
    show_product_grid(df, WHATSAPP_PHONE, columns_mode)

# ------------------ PAGE: PRICE CALCULATING ------------------
elif page == "Price Calculating":
    st.title("💰 Price Calculator")
    st.markdown("""
    Enter your product details and quantity to calculate total price.
    """)
    # Example: you can add inputs and calculation here
    product_name = st.text_input("Product Name")
    quantity = st.number_input("Quantity", min_value=1, value=1)
    price_per_unit = st.number_input("Price per unit", min_value=0.0, value=0.0)

    if st.button("Calculate Total"):
        total = quantity * price_per_unit
        st.success(f"Total Price: 💰 {total}")

# ------------------ PAGE: CONTACT US ------------------
elif page == "Contact Us":
    st.title("📞 Contact Us")
    st.markdown("You can reach us via WhatsApp or Email:")

    st.markdown(f"- WhatsApp: [Send Message](https://wa.me/{WHATSAPP_PHONE})")
    st.markdown("- Email: info@yourcompany.com")  # replace with your email

# ------------------ PAGE: ABOUT US ------------------
elif page == "About Us":
    st.title("ℹ️ About Us")
    st.image("logo.png", width=200)  # your logo
    st.markdown("""
    **Company Name**: Your Company  
    **Location**: Erbil, Kurdistan  
    **Services**: Solar panel cleaning, products showcase, and more.  

    We provide high-quality products and real-time product info via Google Sheets.
    """)
