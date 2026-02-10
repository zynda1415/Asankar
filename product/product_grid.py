import streamlit as st
from product.whatsapp import build_whatsapp_link
from product.badges import render_badge

def show_product_grid(df, phone, columns_mode=3):
    """
    Displays products in a flexible grid with 4 modes:
    1 → 4 products square (2x2)
    2 → 2 columns
    3 → 3 columns
    4 → 5 columns

    Parameters:
        df (DataFrame): Product data with 'URL', 'Name', 'Price', 'Badge'
        phone (str): WhatsApp phone number
        columns_mode (int): 1,2,3,4 → layout mode
    """
    # Determine number of columns
    if columns_mode == 1:
        cols_count = 2  # 2x2 grid
    elif columns_mode == 2:
        cols_count = 2
    elif columns_mode == 3:
        cols_count = 3
    elif columns_mode == 4:
        cols_count = 5
    else:
        cols_count = 3  # fallback default

    cols = st.columns(cols_count)

    for i, row in df.iterrows():
        with cols[i % cols_count]:
            st.markdown('<div class="card">', unsafe_allow_html=True)

            # Show badge if available
            if "Badge" in df.columns and row.get("Badge"):
                render_badge(row["Badge"])

            url = row["URL"]

            # Detect media type
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
