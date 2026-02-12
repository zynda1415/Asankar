import streamlit as st

# ------------------ CONFIG ------------------
MATERIAL_PRICES = {
    "MDF": 120,
    "Balloon Press": 160,
    "Glass": 170
}

# ------------------ PAGE ------------------
def show_price_calculator():

    st.title("🧮 Price Calculator")

    # ------------------ STEP 1: MATERIAL ------------------
    st.subheader("Select Material")

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("MDF"):
            st.session_state.material = "MDF"
        st.image("main/images/materials/mdf.png", use_column_width=True)

    with col2:
        if st.button("Balloon Press"):
            st.session_state.material = "Balloon Press"
        st.image("main/images/materials/balloon_press.png", use_column_width=True)

    with col3:
        if st.button("Glass"):
            st.session_state.material = "Glass"
        st.image("main/images/materials/glass.png", use_column_width=True)

    if "material" not in st.session_state:
        return

    st.success(f"Selected Material: {st.session_state.material} "
               f"({MATERIAL_PRICES[st.session_state.material]}$/m²)")

    # ------------------ STEP 2: PRODUCT ------------------
    st.subheader("Select Product")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Kitchen"):
            st.session_state.product = "Kitchen"
        st.image("main/images/products/kitchen.png", use_column_width=True)

    with col2:
        if st.button("Wardrobe"):
            st.session_state.product = "Wardrobe"
        st.image("main/images/products/wardrobe.png", use_column_width=True)

    if "product" not in st.session_state:
        return

    st.success(f"Selected Product: {st.session_state.product}")

    # ------------------ STEP 3: KITCHEN LAYOUT ------------------
    if st.session_state.product == "Kitchen":

        st.subheader("Select Kitchen Layout")

        col1, col2 = st.columns(2)
        col3, col4 = st.columns(2)

        with col1:
            if st.button("One-Wall"):
                st.session_state.layout = "One-Wall"
            st.image("main/images/layouts/one_wall.png", use_column_width=True)

        with col2:
            if st.button("L-Shaped"):
                st.session_state.layout = "L-Shaped"
            st.image("main/images/layouts/l_shaped.png", use_column_width=True)

        with col3:
            if st.button("U-Shaped"):
                st.session_state.layout = "U-Shaped"
            st.image("main/images/layouts/u_shaped.png", use_column_width=True)

        with col4:
            if st.button("Galley"):
                st.session_state.layout = "Galley"
            st.image("main/images/layouts/galley.png", use_column_width=True)

        if "layout" in st.session_state:
            st.success(f"Selected Layout: {st.session_state.layout}")

    # ------------------ STEP 3: WARDROBE ------------------
    if st.session_state.product == "Wardrobe":

        st.subheader("Wardrobe Dimensions")

        height = st.number_input("Height (m)", min_value=0.0, step=0.1)
        width = st.number_input("Width (m)", min_value=0.0, step=0.1)

        if height > 0 and width > 0:
            area = height * width
            price = area * MATERIAL_PRICES[st.session_state.material]

            st.markdown("---")
            st.write(f"Area: {area:.2f} m²")
            st.write(f"Estimated Price: ${price:.2f}")
