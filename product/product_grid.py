import streamlit as st
import urllib.parse

def show_product_grid(df, whatsapp_phone, columns_mode=3):

    st.markdown("""
    <style>
    .product-container {
        position: relative;
        display: inline-block;
        width: 100%;
    }
    
    .product-image {
        width: 100%;
        display: block;
    }
    
    .overlay-btn {
        position: absolute;
        bottom: 10px;           /* distance from bottom of image */
        left: 50%;
        transform: translateX(-50%);
        background-color: rgba(46,46,46,0.7); /* semi-transparent dark grey 20% */
        color: white !important;
        padding: 8px 16px;
        border-radius: 10px;
        font-weight: 700;
        text-align: center;
        text-decoration: none;    /* remove underline */
        opacity: 1;               /* opacity handled by background-color */
    }
    
    .overlay-btn:hover {
        background-color: rgba(46,46,46,0.8);
    }
    
    .product-name {
        font-weight: 600;
        text-align: center;
        margin-top: 5px;
        margin-bottom: 5px;
    }
    
    div[data-testid="stVerticalBlock"] > div {
        gap: 0.5rem;
    }
    </style>
    """, unsafe_allow_html=True)


    cols = st.columns(columns_mode)

    for i, row in df.iterrows():
        col = cols[i % columns_mode]

        with col:
            url = row["URL"]

            # Container for overlay
            st.markdown('<div class="product-container">', unsafe_allow_html=True)

            # Show product
            if "youtube.com" in url or "youtu.be" in url:
                st.video(url)
            elif any(url.lower().endswith(ext) for ext in [".mp4", ".mov", ".avi", ".webm", ".m4v"]):
                st.video(url)
            else:
                st.image(url, use_container_width=True, output_format="auto")

            # WhatsApp button overlay
            message = f"I am interested in this product: {row.get('Name','')}"
            encoded_message = urllib.parse.quote(message)
            link = f"https://wa.me/{whatsapp_phone}?text={encoded_message}"

            st.markdown(
                f'<a href="{link}" target="_blank" class="overlay-btn">لەسەر بەرهەمەکە بپرسە</a>',
                unsafe_allow_html=True
            )

            st.markdown('</div>', unsafe_allow_html=True)

            # Product name below image
            st.markdown(
                f'<div class="product-name">{row.get("Name","")}</div>',
                unsafe_allow_html=True
            )
