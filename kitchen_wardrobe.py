import streamlit as st

def show_kitchen_wardrobe(materials):
    st.image("images/materials.png", use_container_width=True)

    material = st.selectbox("Select Material", list(materials.keys()))
    height = st.number_input("Height (m)", min_value=0.0, step=0.1)
    length = st.number_input("Length (m)", min_value=0.0, step=0.1)

    st.markdown("#### Appliances / Components (optional)")

    # Compact appliance rows with icon + input
    def appliance_input(icon, label, default=0.0):
        col_icon, col_input = st.columns([1,4])
        with col_icon:
            st.image(f"images/{icon}.png", width=32)
        with col_input:
            value = st.number_input(label, min_value=0.0, step=1.0, value=default)
        return value

    fridge = appliance_input("fridge", "Fridge width (cm)")
    dishwasher = appliance_input("dishwasher", "Dishwasher width (cm)")
    stove = appliance_input("stove", "Stove width (cm)")
    oven = st.checkbox("Oven included")
    cabinet = appliance_input("cabinet", "Cabinet width (cm)")

    if st.button("Add to Cart"):
        total_area = height * length
        deductions = (fridge + dishwasher + stove + cabinet)/100  # cm -> m
        total_area -= deductions
        price = round(total_area * materials[material], 2)

        st.session_state.cart.append({
            "Product": st.session_state.selected_product or "Kitchen/Wardrobe",
            "Material": material,
            "Height": height,
            "Length": length,
            "Price": price
        })
        st.success(f"Added to cart: ${price}")
