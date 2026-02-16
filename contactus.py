import streamlit as st

def show_contact(phone):
    # Hero section
    st.markdown("""
    <div style='text-align: center; padding: 50px 20px;'>
        <div style='font-size: 80px; margin-bottom: 20px;'>📞</div>
        <h1 style='color: #1e3c72; font-size: 42px; margin-bottom: 15px;'>Get in Touch</h1>
        <p style='font-size: 20px; color: #666;'>We're here to help with your furniture needs</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Contact methods
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class='custom-card' style='text-align: center; padding: 40px;'>
            <div style='font-size: 60px; margin-bottom: 20px;'>📱</div>
            <h3 style='color: #1e3c72; margin-bottom: 15px;'>Phone / WhatsApp</h3>
            <p style='font-size: 24px; font-weight: 600; color: #25D366; margin-bottom: 20px;'>+""" + phone + """</p>
            <p style='color: #666;'>Available 24/7 for your inquiries</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class='custom-card' style='text-align: center; padding: 40px;'>
            <div style='font-size: 60px; margin-bottom: 20px;'>⏰</div>
            <h3 style='color: #1e3c72; margin-bottom: 15px;'>Business Hours</h3>
            <p style='font-size: 18px; margin-bottom: 10px;'><strong>Saturday - Thursday</strong></p>
            <p style='color: #666; font-size: 16px;'>9:00 AM - 9:00 PM</p>
            <p style='font-size: 18px; margin-top: 15px; margin-bottom: 10px;'><strong>Friday</strong></p>
            <p style='color: #666; font-size: 16px;'>Closed</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # WhatsApp CTA
    st.markdown("""
    <div style='background: linear-gradient(135deg, #25D366 0%, #128C7E 100%); 
                padding: 40px; border-radius: 20px; text-align: center; margin: 30px 0;'>
        <h2 style='color: white; margin-bottom: 15px;'>💬 Start a Conversation</h2>
        <p style='color: white; font-size: 18px; margin-bottom: 25px;'>
            Get instant responses to your questions and receive personalized quotes
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        whatsapp_link = f"https://wa.me/{phone}?text=Hello! I would like to know more about your products and services."
        if st.button("📱 Open WhatsApp Chat", use_container_width=True, key="whatsapp_main"):
            st.markdown(f'<meta http-equiv="refresh" content="0;url={whatsapp_link}">', unsafe_allow_html=True)
            st.markdown(f"[Click here if not redirected]({whatsapp_link})")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Why contact us section
    st.markdown("### ✨ Why Choose Asankar Factory?")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div style='padding: 20px; background: #f8f9fa; border-radius: 12px; margin-bottom: 15px;'>
            <h4 style='color: #1e3c72;'>🎨 Custom Designs</h4>
            <p style='color: #666;'>Tailored furniture solutions to match your exact specifications and style preferences</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div style='padding: 20px; background: #f8f9fa; border-radius: 12px; margin-bottom: 15px;'>
            <h4 style='color: #1e3c72;'>💰 Competitive Pricing</h4>
            <p style='color: #666;'>Direct factory prices with no middleman markup - best value for your investment</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style='padding: 20px; background: #f8f9fa; border-radius: 12px; margin-bottom: 15px;'>
            <h4 style='color: #1e3c72;'>✅ Quality Guarantee</h4>
            <p style='color: #666;'>Premium materials and expert craftsmanship ensuring long-lasting furniture</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div style='padding: 20px; background: #f8f9fa; border-radius: 12px; margin-bottom: 15px;'>
            <h4 style='color: #1e3c72;'>🚚 Reliable Delivery</h4>
            <p style='color: #666;'>On-time delivery and professional installation services across the region</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Location info (if you have one)
    st.markdown("### 📍 Visit Our Showroom")
    st.markdown("""
    <div class='custom-card' style='padding: 30px;'>
        <h4 style='color: #1e3c72; margin-bottom: 15px;'>Asankar Factory</h4>
        <p style='color: #666; font-size: 16px; line-height: 1.8;'>
            📍 Sulaymaniyah, Iraq<br>
            📞 +""" + phone + """<br>
            💬 WhatsApp: +""" + phone + """<br>
            🕐 Sat-Thu: 9:00 AM - 9:00 PM
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Quick message section
    st.markdown("### 💭 Send Us a Quick Message")
    
    with st.form("contact_form"):
        message_type = st.selectbox(
            "What are you interested in?",
            ["General Inquiry", "Kitchen Furniture", "Wardrobe", "Bed Frames", "Custom Design", "Price Quote"]
        )
        
        user_message = st.text_area(
            "Your Message",
            placeholder="Tell us about your furniture needs...",
            height=120
        )
        
        col1, col2 = st.columns([3, 1])
        with col2:
            submitted = st.form_submit_button("Send via WhatsApp 📱", use_container_width=True)
        
        if submitted:
            if user_message.strip():
                full_message = f"*{message_type}*\n\n{user_message}"
                whatsapp_link = f"https://wa.me/{phone}?text={full_message}"
                st.success("✅ Redirecting to WhatsApp...")
                st.markdown(f'<meta http-equiv="refresh" content="1;url={whatsapp_link}">', unsafe_allow_html=True)
                st.markdown(f"[Click here if not redirected]({whatsapp_link})")
            else:
                st.warning("Please enter a message first!")
