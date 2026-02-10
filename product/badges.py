
import streamlit as st

def render_badge(badge):
    if badge == "New":
        st.markdown(
            "<span style='background:#198754;color:white;padding:4px 10px;"
            "border-radius:8px;font-size:12px;'>🆕 NEW</span>",
            unsafe_allow_html=True
        )
    elif badge == "Best":
        st.markdown(
            "<span style='background:#fd7e14;color:white;padding:4px 10px;"
            "border-radius:8px;font-size:12px;'>⭐ BEST SELLER</span>",
            unsafe_allow_html=True
        )
