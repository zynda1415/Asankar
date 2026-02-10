import streamlit as st
from product.whatsapp import build_whatsapp_link
from product.badges import render_badge

def show_product_grid(df, phone):
    cols = st.columns(3)

    for i, row in df.iterrows():
        with cols[i % 3]:
            st.markdown('<div class="card">', unsafe_allow_html=True)

            # Badge
            if "Badge" in df.columns and row.get("Badge"):
                render_badge(row["Badge"])

            url = row["URL"]

            # Media
            if any(url.lower().endswith(ext) for ext in ["jpg", "jpeg", "png", "webp"]):
                st.image(url, use_container_width=True)
            else:
                st.video(url)

            name = row.get("Name", "Product")
            st.subheader(name)
            st.caption(row.get("Category", ""))

            if "Price" in df.columns and row.get("Price"):
                st.markdown(
                    f"<div class='price'>💰 {row['Price']}</div>",
                    unsafe_allow_html=True
                )

            # WhatsApp CTA
            wa_link = build_whatsapp_link(phone, name)
            st.markdown(
                f"<a class='whatsapp' href='{wa_link}' target='_blank'>📲 Request this product</a>",
                unsafe_allow_html=True
            )

            st.markdown('</div>', unsafe_allow_html=True)
