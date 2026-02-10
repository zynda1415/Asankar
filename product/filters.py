
import streamlit as st

def apply_filters(df):
    c1, c2 = st.columns(2)

    with c1:
        search = st.text_input("🔍 Search product")

    with c2:
        if "Category" in df.columns:
            categories = ["All"] + sorted(df["Category"].dropna().unique())
            selected_category = st.selectbox("📂 Category", categories)
        else:
            selected_category = "All"

    if search and "Name" in df.columns:
        df = df[df["Name"].str.contains(search, case=False, na=False)]

    if selected_category != "All" and "Category" in df.columns:
        df = df[df["Category"] == selected_category]

    return df
