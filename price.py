import streamlit as st

def show_price_calculator():
    st.title("💰 Price Calculator")
    st.markdown("Enter your product details and quantity to calculate total price.")

    product_name = st.text_input("Product Name")
    quantity = st.number_input("Quantity", min_value=1, value=1)
    price_per_unit = st.number_input("Price per unit", min_value=0.0, value=0.0)

    if st.button("Calculate Total"):
        total = quantity * price_per_unit
        st.success(f"Total Price: 💰 {total}")
