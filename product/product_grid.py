import streamlit as st
import urllib.parse

def is_video(url):
    video_extensions = [".mp4", ".mov", ".avi", ".webm", ".m4v"]
    return any(url.lower().endswith(ext) for ext in video_extensions)

def show_product_grid(df, whatsapp_phone, columns_mode=3):

    st.markdown("""
        <style>
        .whatsapp-btn {
            display: inline-block;
            background-color: #2e2e2e;
            color: white !important;
            padding: 10px 18px;
            border-radius: 8px;
            text-decoration: none;
            font-weight: 600;
            text-align: center;
            width: 100%;
        }
        .whatsapp-btn:hover {
            background-color: #1f1f1f;
        }
        </style>
    """, unsafe_allow_html=True)

    cols = st.columns(columns_mode)

    for i, row in df.iterrows():
        col = cols[i % columns_mode]

        with col:
            url = row["URL"]

            # Detect video or image
            if is_video(url):
                st.video(url)
            else:
                st.image(url, use_container_width=True)

            st.markdown(f"**{row.get('Name','')}**")

            message = f"I am interested in this product: {row.get('Name','')}"
            encoded_message = urllib.parse.quote(message)
            link = f"https://wa.me/{whatsapp_phone}?text={encoded_message}"

            st.markdown(
                f'<a href="{link}" target="_blank" class="whatsapp-btn">لەسەر بەرهەمەکە بپرسە</a>',
                unsafe_allow_html=True
            )
