import streamlit as st

def show_product_grid(df, whatsapp_phone, columns_mode=3):
    cols = st.columns(columns_mode)
    for i, row in df.iterrows():
        with cols[i % columns_mode]:
            if row.get("Image"):
                st.image(row["Image"], use_container_width=True)
            st.markdown(f"**{row.get('Title','')}**")
            st.markdown(row.get("Description",""))
            if whatsapp_phone:
                msg = row.get("Title","Product")
                url = f"https://wa.me/{whatsapp_phone}?text=I%20am%20interested%20in%20{msg}"
                st.markdown(f"[Order via WhatsApp]({url})")
