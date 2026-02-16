import streamlit as st

def show_contact(phone):
    st.title("Contact Us")

    st.write("📞 Phone / WhatsApp:")
    st.write(phone)

    st.markdown(f"[Chat on WhatsApp](https://wa.me/{phone})")
