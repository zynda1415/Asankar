import streamlit as st

# ----------------- Modular Imports -----------------
from product.load_data import load_data
from product.product_grid import show_product_grid

from price import show_price_calculator
from contactus import show_contact
from aboutas import show_about

# ----------------- Page Config -----------------
st.set_page_config(
    page_title="Asankar Products",
    layout="wide"
)

# ----------------- Auto Refresh Every 30s -----------------
st.autorefresh(interval=30000, key="sheet_refresh")

# ----------------- WhatsApp Config -----------------
WHATSAPP_PHONE = "9647501003839"  # no + sign

# ----------------- Sidebar -----------------
with st.sidebar:
    st.image("logo.png", width=180)
    st.markdown("## Menu")
    page = st.radio(
        "",
        [
            "Products",
            "Price Calculating",
            "Contact Us",
            "About Us"
        ]
    )

# ----------------- Page Routing -----------------
if page == "Products":
    st.markdown("<h2 style='margin-top:0;'>بەرهەمەکانمان</h2>", unsafe_allow_html=True)

    df = load_data()

    if df.empty:
        st.warning("No products found.")
    else:
        show_product_grid(df, WHATSAPP_PHONE, 3)  # Always 3 columns

elif page == "Price Calculating":
    show_price_calculator()

elif page == "Contact Us":
    show_contact(phone=WHATSAPP_PHONE)

elif page == "About Us":
    show_about()
