import streamlit as st
from product.whatsapp import build_whatsapp_link
from product.badges import render_badge

product_url = row["URL"]
message = f"السلام علیکم، دەمەوێت زیاتر بزانم لەسەر ئەم بەرهەمە: {product_url}"
wa_link = f"https://wa.me/{phone}?text={st.experimental_singleton(lambda: message)()}"

    """
    Modern responsive product grid with badges and WhatsApp CTA.
    columns_mode: 2 → 2 cols, 3 → 3 cols, 4 → 5 cols
    """
    # Determine number of columns
    if columns_mode == 2:
        cols_count = 2
    elif columns_mode == 3:
        cols_count = 3
    elif columns_mode == 4:
        cols_count = 5
    else:
        cols_count = 3

    # Custom CSS for cards
    st.markdown("""
    <style>
    .card {
        background: white;
        border-radius: 16px;
        padding: 15px;
        margin-bottom: 20px;
        box-shadow: 0 6px 20px rgba(0,0,0,0.08);
    }
    .price {
        font-size: 16px;
        font-weight: 700;
        color: #0d6efd;
    }
    .whatsapp {
        background-color: #25D366;
        color: white;
        padding: 10px;
        border-radius: 10px;
        text-align: center;
        text-decoration: none;
        display: block;
        margin-top: 10px;
        font-weight: 600;
    }
    @media (max-width: 768px) {
        .stColumns {flex-wrap: wrap;}
        .stColumn {width: 100% !important;}
    }
    </style>
    """, unsafe_allow_html=True)

    cols = st.columns(cols_count)

    for i, row in df.iterrows():
        with cols[i % cols_count]:
            st.markdown('<div class="card">', unsafe_allow_html=True)

            # Badge
            if "Badge" in df.columns and row.get("Badge"):
                render_badge(row["Badge"])

            url = row["URL"]
            if any(url.lower().endswith(ext) for ext in ["jpg", "jpeg", "png", "webp"]):
                st.image(url, use_container_width=True)
            else:
                st.video(url)

            name = row.get("Name", "Product")
            st.subheader(name)
            st.caption(row.get("Category", ""))

            if "Price" in df.columns and row.get("Price"):
                st.markdown(f"<div class='price'>💰 {row['Price']}</div>", unsafe_allow_html=True)

            wa_link = build_whatsapp_link(phone, name)
            st.markdown(f"<a class='whatsapp' href='{wa_link}' target='_blank'>📲 Request this product</a>", unsafe_allow_html=True)

            st.markdown('</div>', unsafe_allow_html=True)
