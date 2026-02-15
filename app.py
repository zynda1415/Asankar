import streamlit as st
from price_calculator import show_price_calculator
from product_view import show_products_page

st.set_page_config(page_title="Asankar Factory", layout="wide")

WHATSAPP_PHONE = "9647501003839"

with st.sidebar:
    page = st.radio("", ["Products", "Price Calculator"])

if page == "Products":
    show_products_page(WHATSAPP_PHONE)

elif page == "Price Calculator":
    show_price_calculator()
