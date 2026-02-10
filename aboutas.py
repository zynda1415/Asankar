import streamlit as st

def show_about():
    st.title("ℹ️ About Us")
    st.image("logo.png", width=200)  # replace with your logo

    st.markdown("""
    **Company Name**: Your Company  
    **Location**: Erbil, Kurdistan  
    **Services**: Solar panel cleaning, products showcase, and more.  

    We provide high-quality products and real-time product info via Google Sheets.
    """)
