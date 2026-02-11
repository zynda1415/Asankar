import streamlit as st
import time

from product.load_data import load_data
from product.product_grid import show_product_grid

# If pages are outside product folder
from price import show_price_calculator
from contactus import show_contact
from aboutas import show_about


# ------------------ CONFIG ------------------
st.set_page_config(
    page_title="Asankar Products",
    layout="wide"
)

WHATSAPP_PHONE = "9647501003839"  # بدون +


# ------------------ AUTO REFRESH (5 min) ------------------
REFRESH_INTERVAL = 300  # seconds

if "last_refresh" not in st.session_state:
    st.session_state.last_refresh = time.time()
else:
    if time.time() - st.session_state.last_refresh > REFRESH_INTERVAL:
        st.session_state.last_refresh = time.time()
        st.rerun()


# ------------------ SIDEBAR ------------------
with st.sidebar:
    st.image("logo.png", width=180)  # make sure logo.png exists

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


# ------------------ PAGE ROUTING ------------------

if page == "Products":

    st.markdown("<h2 style='margin-top:0;'>بەرهەمەکانمان</h2>", unsafe_allow_html=True)

    # Load Google Sheet data
    df = load_data()

    if df.empty:
        st.warning("No products found.")
    else:
        show_product_grid(df, WHATSAPP_PHONE, 3)


elif page == "Price Calculating":
    show_price_calculator()


elif page == "Contact Us":
    show_contact(phone=WHATSAPP_PHONE)


elif page == "About Us":
    show_about()
