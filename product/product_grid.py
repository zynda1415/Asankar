import streamlit as st
import urllib.parse

def show_product_grid(df, whatsapp_phone, columns_mode=3):

    st.markdown("""
        <style>
        .product-name {
            margin-bottom: 5px;
            font-weight: 600;
        }

        .whatsapp-btn {
            display: inline-block;
            background-color: #2e2e2e;
            color: white !important;
            padding: 8px 16px;
            border-radius: 8px;
            text-decoration: none;
            font-weight: 600;
            text-align: center;
            width: 100%;
            margin-top: 1px;
        }

        .whatsapp-btn:hover {
            background-color: #1f1f1f;
        }

        div[data-testid="stVerticalBlock"] > div {
            gap: 0.3rem;
        }
        </style>
    """, unsafe_allow_html=True)

    cols = st.columns(columns_mode)

    for i, row in df.iterrows():
        col = cols[i % columns_mode]

        with col:
            url = row["URL"]

            # YouTube
            if "youtube.com" in url or "youtu.be" in url:
                st.video(url)

            # Direct video files
            elif any(url.lower().endswith(ext) for ext in [".mp4", ".mov", ".avi", ".webm", ".m4v"]):
                st.video(url)

            # Image
            else:
                st.image(url, use_container_width=True)

            st.markdown(
                f'<div class="product-name">{row.get("Name","")}</div>',
                unsafe_allow_html=True
            )

            message = f"I am interested in this product: {row.get('Name','')}"
            encoded_message = urllib.parse.quote(message)
            link = f"https://wa.me/{whatsapp_phone}?text={encoded_message}"

            st.markdown(
                f'<a href="{link}" target="_blank" class="whatsapp-btn">لەسەر بەرهەمەکە بپرسە</a>',
                unsafe_allow_html=True
            )
