import streamlit as st

def show_contact(phone="964XXXXXXXXX", email="info@yourcompany.com"):
    st.title("📞 Contact Us")
    st.markdown("You can reach us via WhatsApp or Email:")

    # WhatsApp link
    st.markdown(f"- WhatsApp: [Send Message](https://wa.me/{phone})")
    st.markdown(f"- Email: {email}")
    
    st.markdown("---")
    st.markdown("We respond as fast as possible!")
