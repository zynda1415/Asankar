import streamlit as st
import pandas as pd
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from datetime import datetime

MATERIAL_PRICES = {
    "MDF": 120,
    "Balloon Press": 160,
    "Glass": 170
}

BED_PRICES = {
    "Simple": {90: 310, 120: 350, 180: 420},
    "Rabbet": {90: 500, 120: 590, 180: 750},
    "MDF": {90: 200, 120: 230, 180: 300}
}

def calculate_kitchen_price(height, length, material, fridge, dishwasher, cabinet, stove, oven):
    base_area = height * length
    additions = cabinet
    deductions = fridge + dishwasher + stove
    if oven:
        additions += 0.6
    total_area = base_area + additions - deductions
    return total_area * MATERIAL_PRICES[material]

def generate_pdf(cart):
    file_path = "quotation.pdf"
    doc = SimpleDocTemplate(file_path, pagesize=A4)
    elements = []
    styles = getSampleStyleSheet()

    elements.append(Paragraph("Asankar Factory Quotation", styles["Title"]))
    elements.append(Spacer(1, 0.3 * inch))
    elements.append(Paragraph(f"Date: {datetime.now().strftime('%Y-%m-%d')}", styles["Normal"]))
    elements.append(Spacer(1, 0.3 * inch))

    data = [["Item", "Price ($)"]]
    total = 0
    for item in cart:
        data.append([item["name"], f'{item["price"]:.2f}'])
        total += item["price"]

    data.append(["Total", f"{total:.2f}"])

    table = Table(data, colWidths=[4 * inch, 2 * inch])
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("ALIGN", (1, 1), (-1, -1), "RIGHT"),
    ]))

    elements.append(table)
    doc.build(elements)

    return file_path

def show_price_calculator():
    if "cart" not in st.session_state:
        st.session_state.cart = []

    st.title("Factory Price Calculator")

    product = st.radio("Select Product", ["Kitchen", "Wardrobe", "Bed"])

    if product in ["Kitchen", "Wardrobe"]:
        material = st.radio("Material", list(MATERIAL_PRICES.keys()))
        height = st.number_input("Height (m)", min_value=1.0)
        length = st.number_input("Length (m)", min_value=1.0)
        fridge = st.number_input("Fridge Width (m)", min_value=0.0)
        dishwasher = st.number_input("Dishwasher Width (m)", min_value=0.0)
        cabinet = st.number_input("Extra Cabinet (m)", min_value=0.0)
        stove = st.number_input("Stove Width (m)", min_value=0.0)
        oven = st.checkbox("Include Oven")

        price = calculate_kitchen_price(height, length, material, fridge, dishwasher, cabinet, stove, oven)

        if st.button("Add to Cart"):
            st.session_state.cart.append({
                "name": f"{product} - {material}",
                "price": price
            })

        st.success(f"Price: ${price:.2f}")

    if product == "Bed":
        size = st.radio("Size (cm)", [90, 120, 180])
        bed_type = st.radio("Type", list(BED_PRICES.keys()))
        price = BED_PRICES[bed_type][size]

        if st.button("Add to Cart"):
            st.session_state.cart.append({
                "name": f"Bed {size}cm - {bed_type}",
                "price": price
            })

        st.success(f"Price: ${price:.2f}")

    if st.session_state.cart:
        st.subheader("Cart")
        df = pd.DataFrame(st.session_state.cart)
        st.table(df)

        total = sum(item["price"] for item in st.session_state.cart)
        st.markdown(f"### Total: ${total:.2f}")

        col1, col2 = st.columns(2)

        if col1.button("Clear Cart"):
            st.session_state.cart = []

        if col2.button("Generate PDF"):
            pdf_path = generate_pdf(st.session_state.cart)
            with open(pdf_path, "rb") as f:
                st.download_button("Download PDF", f, file_name="quotation.pdf")
