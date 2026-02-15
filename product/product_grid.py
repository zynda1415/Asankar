import streamlit as st

def show_product_grid(df, whatsapp_phone, columns_mode=3):
    cols = st.columns(columns_mode)

    for i, row in df.iterrows():
        with cols[i % columns_mode]:

            url = str(row.get("URL", "")).strip()

            if url:
                # YouTube
                if "youtube" in url or "youtu.be" in url:
                    st.video(url)

                # Image
                elif url.lower().endswith((".jpg", ".jpeg", ".png", ".webp")):
                    st.image(url, use_container_width=True)

                # Fallback
                else:
                    st.write(url)

            st.markdown(f"**{row.get('Title','')}**")
            st.markdown(row.get("Description",""))

            if whatsapp_phone:
                msg = row.get("Title","Product")
                wa_url = f"https://wa.me/{whatsapp_phone}?text=I%20am%20interested%20in%20{msg}"
                st.markdown(f"[Order via WhatsApp]({wa_url})")
