import streamlit as st

def show_product_grid(df, whatsapp_phone, columns_mode=3):
    cols = st.columns(columns_mode)
    
    for i, row in df.iterrows():
        col = cols[i % columns_mode]
        with col:
            # Modern card design
            st.markdown("""
            <style>
            .product-card {
                background: white;
                border-radius: 15px;
                padding: 0;
                box-shadow: 0 4px 15px rgba(0,0,0,0.1);
                transition: all 0.3s ease;
                overflow: hidden;
                margin-bottom: 25px;
            }
            .product-card:hover {
                transform: translateY(-10px);
                box-shadow: 0 8px 25px rgba(0,0,0,0.15);
            }
            .product-image-container {
                position: relative;
                overflow: hidden;
                border-radius: 15px 15px 0 0;
            }
            .product-image-container img {
                transition: transform 0.3s ease;
            }
            .product-image-container:hover img {
                transform: scale(1.05);
            }
            .product-info {
                padding: 20px;
            }
            .product-name {
                font-size: 18px;
                font-weight: 600;
                color: #1e3c72;
                margin-bottom: 15px;
                text-align: center;
            }
            .whatsapp-btn {
                display: block;
                background: linear-gradient(135deg, #25D366 0%, #128C7E 100%);
                color: white;
                padding: 12px 20px;
                text-align: center;
                text-decoration: none;
                border-radius: 10px;
                font-weight: 600;
                font-size: 16px;
                transition: all 0.3s ease;
                box-shadow: 0 4px 10px rgba(37,211,102,0.3);
            }
            .whatsapp-btn:hover {
                transform: translateY(-2px);
                box-shadow: 0 6px 15px rgba(37,211,102,0.4);
                text-decoration: none;
                color: white;
            }
            </style>
            """, unsafe_allow_html=True)
            
            # Product card HTML
            product_name = row.get('Name', 'Product')
            image_url = row.get("URL", "")
            
            st.markdown('<div class="product-card">', unsafe_allow_html=True)
            
            # Image with hover effect
            st.markdown('<div class="product-image-container">', unsafe_allow_html=True)
            if image_url:
                st.image(image_url, use_container_width=True)
            else:
                st.markdown("""
                <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                            height: 200px; display: flex; align-items: center; 
                            justify-content: center; color: white; font-size: 48px;'>
                    🛋️
                </div>
                """, unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Product info
            st.markdown(f'<div class="product-info">', unsafe_allow_html=True)
            st.markdown(f'<div class="product-name">{product_name}</div>', unsafe_allow_html=True)
            
            # WhatsApp button
            message = f"Hello! I'm interested in: {product_name}"
            whatsapp_link = f"https://wa.me/{whatsapp_phone}?text={message}"
            
            st.markdown(f"""
            <a href="{whatsapp_link}" target="_blank" class="whatsapp-btn">
                📱 Order on WhatsApp
            </a>
            """, unsafe_allow_html=True)
            
            st.markdown('</div></div>', unsafe_allow_html=True)
