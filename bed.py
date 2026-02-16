# bed.py
import streamlit as st

def show_bed(bed_prices):
    st.markdown("<h3>Bed Configuration</h3>", unsafe_allow_html=True)
    
    st.image("images/bed_size.png", use_container_width=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        size = st.selectbox("حجم السرير (cm)", ["90", "120", "180"])
    
    st.image("images/bed_types.png", use_container_width=True)
    
    with col2:
        bed_type = st.selectbox("نوع السرير", list(bed_prices.keys()))

    price = bed_prices[bed_type][size]
    
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("الحجم", f"{size} cm")
    with col2:
        st.metric("النوع", bed_type)
    with col3:
        st.metric("السعر", f"${price}")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col3:
        if st.button("➕ إضافة إلى السلة", use_container_width=True, type="primary"):
            st.session_state.cart.append({
                "Product": "Bed",
                "Type": bed_type,
                "Size": f"{size}cm",
                "Price": price
            })
            st.success(f"✅ تمت الإضافة: ${price}")
            st.rerun()
