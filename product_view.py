import streamlit as st
from product.load_data import load_data
from product.product_grid import show_product_grid

def show_products_page(whatsapp_phone):
    st.markdown("<h2>بەرهەمەکانمان</h2>", unsafe_allow_html=True)

    df = load_data()

    if df.empty:
        st.warning("No products available.")
    else:
        show_product_grid(df, whatsapp_phone, columns_mode=3)
