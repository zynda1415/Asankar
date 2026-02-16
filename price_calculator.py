import streamlit as st
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
import datetime

# ---------------- Default Prices ----------------
MATERIAL_PRICES = {"MDF": 120, "Balloon Press": 160, "Glass": 170}
BED_PRICES = {
    "Simple": {"90": 310, "120": 350, "180": 420},
    "Rabbet": {"90": 500, "120": 590, "180": 750},
    "MDF": {"90": 200, "120": 230, "180": 300}
}

if "cart" not in st.session_state:
    st.session_state.cart = []

# ---------------- Price Calculator ----------------
def show_price_calculator(materials=MATERIAL_PRICES, bed_prices=BED_PRICES):
    st.title("Price Calculator")

    # 1️⃣ Select Product Type
    product_type = st.radio(
        "Select Product Type",
        ["Kitchen", "Wardrobe", "Bed"],
        horizontal=True
    )
    st.image("images/products.png", use_container_width=True)

    # ---------------- 2️⃣ Kitchen / Wardrobe Flow ----------------
    if product_type in ["Kitchen", "Wardrobe"]:
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
        oven = st.checkbox("Oven included")  # checkbox separate
        cabinet = appliance_input("cabinet", "Cabinet width (cm)")

        if st.button("Add to Cart"):
            total_area = height * length
            deductions = (fridge + dishwasher + stove + cabinet)/100  # cm -> m
            total_area -= deductions
            price = round(total_area * materials[material], 2)

            st.session_state.cart.append({
                "Product": product_type,
                "Material": material,
                "Height": height,
                "Length": length,
                "Price": price
            })
            st.success(f"Added to cart: ${price}")

    # ---------------- 3️⃣ Bed Flow ----------------
    elif product_type == "Bed":
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

    # ---------------- 4️⃣ Cart System ----------------
    if st.session_state.cart:
        st.markdown("---")
        st.subheader("Cart Items")
        total = 0
        for item in st.session_state.cart:
            st.write(item)
            total += item["Price"]
        st.write(f"**Total: ${round(total,2)}**")

        col_clear, col_pdf = st.columns(2)
        with col_clear:
            if st.button("Clear Cart"):
                st.session_state.cart = []
        with col_pdf:
            if st.button("Generate PDF"):
                generate_pdf(st.session_state.cart, total)

# ---------------- 5️⃣ PDF Quotation ----------------
def generate_pdf(cart, total):
    filename = "quotation.pdf"
    doc = SimpleDocTemplate(filename, pagesize=A4)
    elements = []
    styles = getSampleStyleSheet()

    elements.append(Paragraph("Asankar Factory - Quotation", styles["Heading1"]))
    elements.append(Spacer(1,12))
    elements.append(Paragraph(f"Date: {datetime.date.today()}", styles["Normal"]))
    elements.append(Spacer(1,12))

    data = [["Product", "Details", "Price"]]
    for item in cart:
        details = " - ".join([f"{k}: {v}" for k,v in item.items() if k not in ["Product","Price"]])
        data.append([item["Product"], details, f"${item['Price']}"])
    data.append(["", "Total", f"${total}"])

    table = Table(data)
    table.setStyle([
        ('GRID',(0,0),(-1,-1),1,colors.black),
        ('BACKGROUND',(0,0),(-1,0),colors.lightgrey)
    ])
    elements.append(table)
    doc.build(elements)

    with open(filename,"rb") as f:
        st.download_button("Download PDF", f, file_name="quotation.pdf")
