import streamlit as st
from product.whatsapp import build_whatsapp_link
from product.badges import render_badge

def show_product_grid(df, phone, columns_mode=3):
    cols_count = {2:2, 3:3, 4:5}.get(columns_mode, 3)
    cols = st.columns(cols_count)

    # ------------------ CSS ------------------
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
        background-color: #333333 !important;
        color: white !important;
        padding: 10px;
        border-radius: 10px;
        text-align: center;
        text-decoration: none !important;
        display: block;
        margin-top: 10px;
        font-weight: 600;
    }
    .whatsapp:hover {
        background-color: #555555 !important;
        color: white !important;
    }
    @media (max-width: 768px) {
        .stColumns {flex-wrap: wrap;}
        .stColumn {width: 100% !important;}
    }
    </style>
    """, unsafe_allow_html=True)

    # ------------------ Render Products ------------------
    for i, row in df.iterrows():
        with cols[i % cols_count]:
            st.markdown('<div class="card">', unsafe_allow_html=True)

            if "Badge" in df.columns and row.get("Badge"):
                render_badge(row["Badge"])

            url = row["URL"]
            if any(url.lower().endswith(ext) for ext in ["jpg","jpeg","png","webp"]):
                st.image(url, use_container_width=True)
            else:
                st.video(url)

            st.subheader(row.get("Name","Product"))
            st.caption(row.get("Category",""))

            if "Price" in df.columns and row.get("Price"):
                st.markdown(f"<div class='price'>💰 {row['Price']}</div>", unsafe_allow_html=True)

            wa_link = build_whatsapp_link(phone, url)
            st.markdown(
                f"<a class='whatsapp' href='{wa_link}' target='_blank'>پرسیار بکە لەسەر بەرهەمەکە</a>",
                unsafe_allow_html=True
            )

            st.markdown('</div>', unsafe_allow_html=True)
