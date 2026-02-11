import streamlit as st
from product.whatsapp import build_whatsapp_link
from product.badges import render_badge

def show_product_grid(df, phone, columns_mode=3):
    """
    Display products in a responsive grid with WhatsApp inquiry button.
    :param df: DataFrame containing product data (columns: URL, Name, Price, Badge, Category)
    :param phone: WhatsApp phone number (without +)
    :param columns_mode: 2,3,5 columns layout (default 3)
    """
    cols_count = {2:2, 3:3, 4:5}.get(columns_mode, 3)
    cols = st.columns(cols_count)

    # ------------------ CSS ------------------
    st.markdown("""
    <style>
    
    .price {
        font-size: 16px;
        font-weight: 700;
        color: #0d6efd;
        margin-top: 5px;
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
    .stImage {
        display: block;
        margin: 0 auto;
        width: 100% !important; /* fill full width */
        height: auto !important;
        border-top-left-radius: 16px;
        border-top-right-radius: 16px;
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

            # Show badge if exists
            if "Badge" in df.columns and row.get("Badge"):
                render_badge(row["Badge"])

            # Image or Video
            url = row["URL"]
            if any(url.lower().endswith(ext) for ext in ["jpg","jpeg","png","webp"]):
                st.image(url, use_column_width=True)  # fills card width
            else:
                st.video(url)

            # Product Name
            st.subheader(row.get("Name", "Product"))

            # Category (optional)
            if "Category" in df.columns and row.get("Category"):
                st.caption(row["Category"])

            # Price (optional)
            if "Price" in df.columns and row.get("Price"):
                st.markdown(f"<div class='price'>💰 {row['Price']}</div>", unsafe_allow_html=True)

            # WhatsApp button
            wa_link = build_whatsapp_link(phone, url)
            st.markdown(
                f"<a class='whatsapp' href='{wa_link}' target='_blank'>پرسیار بکە لەسەر بەرهەمەکە</a>",
                unsafe_allow_html=True
            )

            st.markdown('</div>', unsafe_allow_html=True)
