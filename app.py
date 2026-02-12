import streamlit as st
from product.load_data import load_data
from product.product_grid import show_product_grid

# Pages
from price_calculator import show_price_calculator
from contactus import show_contact
from aboutas import show_about


# ----------------- PAGE CONFIG -----------------
st.set_page_config(
    page_title="Asankar Factory",
    page_icon="🏭",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ----------------- AUTO REFRESH (1 hour) -----------------
st.markdown(
    """
    <meta http-equiv="refresh" content="3600">
    """,
    unsafe_allow_html=True
)

# ----------------- WHATSAPP CONFIG -----------------
WHATSAPP_PHONE = "9647501003839"  # without +

# ----------------- SIDEBAR -----------------
with st.sidebar:
    st.image("logo.png", width=170)
    st.markdown("### Navigation")

    page = st.radio(
        "",
        [
            "Products",
            "Price Calculator",
            "Contact Us",
            "About Us"
        ],
        label_visibility="collapsed"
    )

# ----------------- PAGE ROUTING -----------------

# ================= PRODUCTS =================
if page == "Products":

    st.markdown("<h2 style='margin-top:0;'>بەرهەمەکانمان</h2>", unsafe_allow_html=True)

    df = load_data()

    if df.empty:
        st.warning("No products available.")
    else:
        show_product_grid(df, WHATSAPP_PHONE, columns_mode=3)


# ================= PRICE CALCULATOR =================
elif page == "Price Calculator":

    show_price_calculator()


# ================= CONTACT =================
elif page == "Contact Us":

    show_contact(phone=WHATSAPP_PHONE)


# ================= ABOUT =================
elif page == "About Us":

    show_about()
