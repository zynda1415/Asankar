import streamlit as st
from product_view import show_products_page
from price_calculator import show_price_calculator
from contactus import show_contact

# Page config with better branding
st.set_page_config(
    page_title="Asankar Factory | Premium Furniture",
    page_icon="🏭",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for modern, attractive design
st.markdown("""
<style>
    /* Main theme colors */
    :root {
        --primary-color: #2E7D32;
        --secondary-color: #FFA726;
        --accent-color: #5E35B1;
        --bg-gradient: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Modern card design */
    .stButton>button {
        width: 100%;
        border-radius: 12px;
        height: 3em;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        font-weight: 600;
        font-size: 16px;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0,0,0,0.3);
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1e3c72 0%, #2a5298 100%);
    }
    
    [data-testid="stSidebar"] .stRadio label {
        color: white !important;
        font-size: 18px !important;
        font-weight: 500 !important;
        padding: 12px 20px;
        border-radius: 10px;
        transition: all 0.3s ease;
    }
    
    [data-testid="stSidebar"] .stRadio label:hover {
        background-color: rgba(255,255,255,0.1);
    }
    
    /* Input fields */
    .stNumberInput input, .stSelectbox select {
        border-radius: 8px;
        border: 2px solid #e0e0e0;
        padding: 10px;
        font-size: 16px;
    }
    
    /* Success messages */
    .stSuccess {
        background-color: #4caf50;
        color: white;
        border-radius: 10px;
        padding: 15px;
        font-weight: 500;
    }
    
    /* Headers */
    h1, h2, h3 {
        color: #1e3c72;
        font-weight: 700;
    }
    
    /* Divider */
    hr {
        margin: 2rem 0;
        border: none;
        height: 2px;
        background: linear-gradient(90deg, transparent, #667eea, transparent);
    }
    
    /* Custom cards */
    .custom-card {
        background: white;
        border-radius: 15px;
        padding: 25px;
        box-shadow: 0 8px 25px rgba(0,0,0,0.1);
        margin-bottom: 20px;
        transition: all 0.3s ease;
    }
    
    .custom-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 35px rgba(0,0,0,0.15);
    }
    
    /* Price display */
    .price-tag {
        background: linear-gradient(135deg, #FFA726 0%, #FF6F00 100%);
        color: white;
        padding: 15px 30px;
        border-radius: 50px;
        font-size: 24px;
        font-weight: 700;
        display: inline-block;
        box-shadow: 0 4px 15px rgba(255,167,38,0.4);
    }
    
    /* Icon styling */
    .icon-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        width: 60px;
        height: 60px;
        border-radius: 15px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 30px;
        margin-bottom: 15px;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<meta http-equiv="refresh" content="3600">', unsafe_allow_html=True)

WHATSAPP_PHONE = "9647501003839"

# Sidebar with improved design
with st.sidebar:
    # Logo section
    col1, col2, col3 = st.columns([1,3,1])
    with col2:
        try:
            st.image("logo.png", width=170)
        except:
            st.markdown("### 🏭 Asankar Factory")
    
    st.markdown("---")
    st.markdown("### 📱 Navigation")
    
    page = st.radio(
        "",
        ["🏠 Products", "💰 Price Calculator", "📞 Contact Us"],
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    st.markdown("#### ✨ Premium Quality")
    st.markdown("#### 🚚 Fast Delivery")
    st.markdown("#### 💯 Best Prices")

# Main content routing
if "Products" in page:
    show_products_page(WHATSAPP_PHONE)
elif "Calculator" in page:
    show_price_calculator()
elif "Contact" in page:
    show_contact(phone=WHATSAPP_PHONE)
