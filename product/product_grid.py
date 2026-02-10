import streamlit as st

def show_product_grid(df):
    cols = st.columns(3)

    for i, row in df.iterrows():
        with cols[i % 3]:
            st.markdown('<div class="card">', unsafe_allow_html=True)

            url = row["URL"]

            # Media detection
            if any(url.lower().endswith(ext) for ext in ["jpg", "jpeg", "png", "webp"]):
                st.image(url, use_container_width=True)
            else:
                st.video(url)

            st.subheader(row.get("Name", "Product"))
            st.caption(row.get("Category", ""))

            if "Price" in df.columns and row.get("Price"):
                st.markdown(
                    f'<div class="price">💰 {row["Price"]}</div>',
                    unsafe_allow_html=True
                )

            message = f"Hello, I am interested in {row.get('Name', 'this product')}"
            wa_link = f"https://wa.me/964XXXXXXXXX?text={message.replace(' ', '%20')}"

            st.markdown(
                f'<a class="whatsapp" href="{wa_link}" target="_blank">📲 Request this product</a>',
                unsafe_allow_html=True
            )

            st.markdown('</div>', unsafe_allow_html=True)
