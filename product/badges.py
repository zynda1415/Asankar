import streamlit as st

def render_badge(badge: str):
    """
    Render product badge. Supports 'New' and 'Best Seller'
    """
    color = "#ff5a5f" if badge.lower() == "new" else "#f0ad4e"
    st.markdown(f"<span style='background-color:{color}; color:white; padding:3px 8px; border-radius:8px; font-size:12px;'>{badge}</span>", unsafe_allow_html=True)
