# kitchen_wardrobe.py
import streamlit as st

def show_kitchen_wardrobe(materials, product_type):
    st.markdown(f"<h3>{product_type} Configuration</h3>", unsafe_allow_html=True)
    
    st.image("images/materials.png", use_container_width=True)

    col1, col2 = st.columns(2)
    
    with col1:
        material = st.selectbox("اختر المادة", list(materials.keys()))
    
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        st.info(f"السعر: ${materials[material]}/m²")
    
    st.markdown("#### القياسات")
    col1, col2 = st.columns(2)
    
    with col1:
        height = st.number_input("الارتفاع (m)", min_value=0.0, step=0.1, value=2.0)
    with col2:
        length = st.number_input("الطول (m)", min_value=0.0, step=0.1, value=3.0)

    st.markdown("#### الأجهزة / المكونات (اختياري)")

    def appliance_input(icon, label, default=0.0):
        col_icon, col_input = st.columns([1, 4])
        with col_icon:
            st.image(f"images/{icon}.png", width=32)
        with col_input:
            value = st.number_input(label, min_value=0.0, step=10.0, value=default, key=f"{icon}_{product_type}")
        return value

    fridge = appliance_input("fridge", "عرض الثلاجة (cm)")
    dishwasher = appliance_input("dishwasher", "عرض غسالة الصحون (cm)")
    stove = appliance_input("stove", "عرض الموقد (cm)")
    cabinet = appliance_input("cabinet", "عرض الخزانة (cm)")

    # Live calculation preview
    total_area = height * length
    deductions = (fridge + dishwasher + stove + cabinet) / 100
    net_area = max(0, total_area - deductions)
    price = round(net_area * materials[material], 2)
    
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("المساحة الإجمالية", f"{round(total_area, 2)} m²")
    with col2:
        st.metric("الخصومات", f"{round(deductions, 2)} m²")
    with col3:
        st.metric("السعر المقدر", f"${price}")

    st.markdown("<br>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col3:
        if st.button("➕ إضافة إلى السلة", use_container_width=True, type="primary"):
            if height > 0 and length > 0:
                st.session_state.cart.append({
                    "Product": product_type,
                    "Material": material,
                    "Height": f"{height}m",
                    "Length": f"{length}m",
                    "Area": f"{round(net_area, 2)}m²",
                    "Price": price
                })
                st.success(f"✅ تمت الإضافة: ${price}")
                st.rerun()
            else:
                st.error("يرجى إدخال قياسات صحيحة")
