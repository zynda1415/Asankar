import streamlit as st
from product_view import show_products_page
from price_calculator import show_price_calculator
from contactus import show_contact

st.set_page_config(page_title="Asankar Factory", page_icon="🏭", layout="wide")

st.markdown("""
<style>
    /* Dark grey theme */
    .stApp {
        background-color: #2b2b2b;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Buttons */
    .stButton>button {
        width: 100%;
        background-color: #4a4a4a;
        color: white;
        border: none;
        padding: 15px;
        font-size: 16px;
        font-weight: 600;
        border-radius: 8px;
        transition: all 0.3s;
    }
    
    .stButton>button:hover {
        background-color: #5a5a5a;
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: #1e1e1e;
    }
    
    [data-testid="stSidebar"] * {
        color: white !important;
    }
    
    /* Input fields */
    .stNumberInput input, .stSelectbox select, .stTextArea textarea {
        background-color: #3a3a3a;
        color: white;
        border: 1px solid #4a4a4a;
        border-radius: 5px;
    }
    
    /* Text */
    h1, h2, h3, h4, h5, h6, p, label, div {
        color: white !important;
    }
    
    /* Cards */
    .card {
        background-color: #3a3a3a;
        padding: 20px;
        border-radius: 8px;
        margin-bottom: 15px;
    }
    
    /* Success/Info messages */
    .stSuccess, .stInfo {
        background-color: #4a4a4a;
        color: white;
    }
</style>
""", unsafe_allow_html=True)

WHATSAPP_PHONE = "9647501003839"

with st.sidebar:
    try:
        st.image("logo.png", width=170)
    except:
        st.markdown("### 🏭 Asankar")
    
    st.markdown("---")
    page = st.radio("", ["Products", "Price Calculator", "Contact Us"], label_visibility="collapsed")

if page == "Products":
    show_products_page(WHATSAPP_PHONE)
elif page == "Price Calculator":
    show_price_calculator()
elif page == "Contact Us":
    show_contact(phone=WHATSAPP_PHONE)
