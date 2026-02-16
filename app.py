import streamlit as st
from product_view import show_products_page
from price_calculator import show_price_calculator
from contactus import show_contact

st.set_page_config(
    page_title="Asankar Factory",
    page_icon="🏭",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Auto refresh every 1 hour
st.markdown('<meta http-equiv="refresh" content="3600">', unsafe_allow_html=True)

WHATSAPP_PHONE = "9647501003839"

with st.sidebar:
    st.image("logo.png", width=170)
    page = st.radio(
        "",
        ["Products", "Price Calculator", "Contact Us"],
        label_visibility="collapsed"
    )

if page == "Products":
    show_products_page(WHATSAPP_PHONE)

elif page == "Price Calculator":
    show_price_calculator()

elif page == "Contact Us":
    show_contact(phone=WHATSAPP_PHONE)
