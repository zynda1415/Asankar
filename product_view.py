import streamlit as st
from product.load_data import load_data
from product.product_grid import show_product_grid

def show_products_page(whatsapp_phone):

    st.markdown("<h2>بەرهەمەکانمان</h2>", unsafe_allow_html=True)

    df = load_data()

    if df.empty:
        st.warning("No products available.")
        return

    # ----------- DYNAMIC FILTERS (Column B → G) -----------
    # Skip first column (A = URL)
    filter_columns = df.columns[1:7]   # B to G

    active_filters = {}

    st.markdown("### Filter")

    cols = st.columns(len(filter_columns))

    for i, col_name in enumerate(filter_columns):

        # Only create filter if column has data
        unique_values = df[col_name].dropna().unique()

        if len(unique_values) > 0:
            selected = cols[i].selectbox(
                col_name,
                ["All"] + sorted(unique_values.tolist())
            )

            if selected != "All":
                active_filters[col_name] = selected

    # ----------- APPLY FILTERS -----------
    filtered_df = df.copy()

    for col_name, value in active_filters.items():
        filtered_df = filtered_df[filtered_df[col_name] == value]

    # ----------- SHOW PRODUCTS -----------
    if filtered_df.empty:
        st.info("No products match your filter.")
    else:
        show_product_grid(filtered_df, whatsapp_phone, columns_mode=3)
