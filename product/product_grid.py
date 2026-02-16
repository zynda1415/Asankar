import streamlit as st

def show_product_grid(df, whatsapp_phone, columns_mode=3):
    cols = st.columns(columns_mode)

    for i, row in df.iterrows():
        col = cols[i % columns_mode]

        with col:
            st.image(row["URL"], use_container_width=True)
            st.markdown(f"**{row.get('Name','')}**")

            message = f"I am interested in this product: {row.get('Name','')}"
            link = f"https://wa.me/{whatsapp_phone}?text={message}"

            st.markdown(
                f"[Order via WhatsApp]({link})",
                unsafe_allow_html=True
            )
