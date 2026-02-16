import streamlit as st
from product.load_data import load_data
from product.product_grid import show_product_grid

def show_products_page(whatsapp_phone):
    # Hero section
    st.markdown("""
    <div style='text-align: center; padding: 40px 20px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 20px; margin-bottom: 30px;'>
        <h1 style='color: white; font-size: 48px; margin-bottom: 15px;'>🏭 Asankar Factory</h1>
        <h2 style='color: white; font-size: 28px; font-weight: 400; margin-bottom: 10px;'>بەرهەمەکانمان</h2>
        <p style='color: rgba(255,255,255,0.9); font-size: 20px;'>Premium Quality Furniture - Crafted with Excellence</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Features section
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div style='text-align: center; padding: 20px; background: white; border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.1);'>
            <div style='font-size: 40px; margin-bottom: 10px;'>✨</div>
            <h4 style='color: #1e3c72; margin-bottom: 5px;'>Premium Quality</h4>
            <p style='color: #666; font-size: 14px;'>Top materials</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style='text-align: center; padding: 20px; background: white; border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.1);'>
            <div style='font-size: 40px; margin-bottom: 10px;'>🚚</div>
            <h4 style='color: #1e3c72; margin-bottom: 5px;'>Fast Delivery</h4>
            <p style='color: #666; font-size: 14px;'>On-time service</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style='text-align: center; padding: 20px; background: white; border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.1);'>
            <div style='font-size: 40px; margin-bottom: 10px;'>💯</div>
            <h4 style='color: #1e3c72; margin-bottom: 5px;'>Best Prices</h4>
            <p style='color: #666; font-size: 14px;'>Great value</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div style='text-align: center; padding: 20px; background: white; border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.1);'>
            <div style='font-size: 40px; margin-bottom: 10px;'>🎨</div>
            <h4 style='color: #1e3c72; margin-bottom: 5px;'>Custom Design</h4>
            <p style='color: #666; font-size: 14px;'>Your style</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Products section
    st.markdown("### 🛋️ Our Products Collection")
    st.markdown("Browse our extensive collection of premium furniture")
    st.markdown("---")
    
    df = load_data()
    if df.empty:
        st.warning("⚠️ No products available at the moment. Please check back later!")
    else:
        show_product_grid(df, whatsapp_phone, columns_mode=3)
    
    # Call to action
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("""
    <div style='text-align: center; padding: 40px; background: linear-gradient(135deg, #FFA726 0%, #FF6F00 100%); border-radius: 20px;'>
        <h2 style='color: white; margin-bottom: 15px;'>💬 Ready to Order?</h2>
        <p style='color: white; font-size: 18px; margin-bottom: 20px;'>Contact us on WhatsApp for instant support and custom quotes!</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Direct WhatsApp button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        whatsapp_link = f"https://wa.me/{whatsapp_phone}?text=Hello! I'm interested in your furniture products."
        st.markdown(f"""
        <a href="{whatsapp_link}" target="_blank" style="text-decoration: none;">
            <div style='background: #25D366; color: white; padding: 20px; border-radius: 15px; text-align: center; font-size: 20px; font-weight: 600; box-shadow: 0 4px 15px rgba(37,211,102,0.4);'>
                📱 Chat on WhatsApp Now
            </div>
        </a>
        """, unsafe_allow_html=True)
