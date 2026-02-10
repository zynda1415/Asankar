view_mode = st.radio(
    "🔳 Select view mode",
    ("4 products square", "2 columns", "3 columns", "5 columns")
)

if view_mode == "4 products square":
    columns_mode = 1
elif view_mode == "2 columns":
    columns_mode = 2
elif view_mode == "3 columns":
    columns_mode = 3
else:
    columns_mode = 4

show_product_grid(df, WHATSAPP_PHONE, columns_mode)
