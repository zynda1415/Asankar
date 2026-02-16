import streamlit as st
import datetime
import os
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import fonts
from reportlab.lib.pagesizes import A4
from reportlab.platypus import Table
from reportlab.lib.styles import getSampleStyleSheet

MATERIAL_PRICES = {
    "MDF": 120,
    "Balloon Press": 160,
    "Glass": 170
}

BED_PRICES = {
    "Simple": {"90": 310, "120": 350, "180": 420},
    "Rabbet": {"90": 500, "120": 590, "180": 750},
    "MDF": {"90": 200, "120": 230, "180": 300}
}

if "cart" not in st.session_state:
    st.session_state.cart = []

def show_price_calculator():
    st.title("Price Calculator")

    product_type = st.selectbox("Select Product", ["Kitchen", "Wardrobe", "Bed"])

    if product_type in ["Kitchen", "Wardrobe"]:

        material = st.selectbox("Select Material", list(MATERIAL_PRICES.keys()))

        height = st.number_input("Height (m)", 0.0)
        length = st.number_input("Length (m)", 0.0)

        fridge = st.number_input("Fridge Width (m)", 0.0)
        dishwasher = st.number_input("Dishwasher Width (m)", 0.0)
        cabinet = st.number_input("Cabinet Width (m)", 0.0)
        stove = st.number_input("Stove Width (m)", 0.0)

        if st.button("Calculate"):

            base_area = height * length
            deductions = (fridge + dishwasher + cabinet + stove) * height
            total_area = base_area - deductions
            total_price = total_area * MATERIAL_PRICES[material]

            item = {
                "Product": product_type,
                "Material": material,
                "Price": round(total_price, 2)
            }

            st.session_state.cart.append(item)
            st.success(f"Added to cart: ${round(total_price,2)}")

    if product_type == "Bed":

        size = st.selectbox("Select Size (cm)", ["90", "120", "180"])
        bed_type = st.selectbox("Select Type", list(BED_PRICES.keys()))

        if st.button("Get Price"):
            price = BED_PRICES[bed_type][size]

            item = {
                "Product": "Bed",
                "Type": bed_type,
                "Size": size,
                "Price": price
            }

            st.session_state.cart.append(item)
            st.success(f"Added to cart: ${price}")

    st.divider()
    st.subheader("Cart")

    total = 0
    for item in st.session_state.cart:
        st.write(item)
        total += item["Price"]

    st.write(f"### Total: ${round(total,2)}")

    col1, col2 = st.columns(2)

    if col1.button("Clear Cart"):
        st.session_state.cart = []

    if col2.button("Generate PDF"):
        generate_pdf(total)

def generate_pdf(total):
    file_path = "quotation.pdf"
    doc = SimpleDocTemplate(file_path, pagesize=A4)
    elements = []

    styles = getSampleStyleSheet()
    elements.append(Paragraph("Asankar Factory - Quotation", styles["Heading1"]))
    elements.append(Spacer(1, 0.5 * inch))

    data = [["Product", "Details", "Price"]]

    for item in st.session_state.cart:
        details = " - ".join([str(v) for k,v in item.items() if k not in ["Product","Price"]])
        data.append([item["Product"], details, f"${item['Price']}"])

    data.append(["", "Total", f"${total}"])

    table = Table(data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.grey),
        ('GRID', (0,0), (-1,-1), 1, colors.black)
    ]))

    elements.append(table)
    doc.build(elements)

    with open(file_path, "rb") as f:
        st.download_button("Download PDF", f, file_name="quotation.pdf")
