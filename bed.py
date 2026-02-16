import streamlit as st

def show_bed(bed_prices):
    st.image("images/bed_size.png", use_container_width=True)
    size = st.selectbox("Bed Size (cm)", ["90", "120", "180"])
    st.image("images/bed_types.png", use_container_width=True)
    bed_type = st.selectbox("Bed Type", list(bed_prices.keys()))

    if st.button("Add Bed to Cart"):
        price = bed_prices[bed_type][size]
        st.session_state.cart.append({
            "Product": "Bed",
            "Type": bed_type,
            "Size": size,
            "Price": price
        })
        st.success(f"Added to cart: ${price}")
