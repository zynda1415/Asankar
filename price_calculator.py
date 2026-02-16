import streamlit as st
from kitchen_wardrobe import show_kitchen_wardrobe
from bed import show_bed
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

# ---------------- Initialize session_state ----------------
for key, default in [("cart", []), ("step", 0), ("selected_product", None),
                     ("selected_material", None), ("bed_size", None), ("bed_type", None)]:
    if key not in st.session_state:
        st.session_state[key] = default

# ---------------- Price Calculator ----------------
def show_price_calculator():
    st.title("Price Calculator")

    # 1️⃣ Select Product Type
    product_type = st.radio(
        "Select Product Type",
        ["Kitchen", "Wardrobe", "Bed"],
        horizontal=True
    )
    st.image("images/products.png", use_container_width=True)

    # Delegate to specific script
    if product_type in ["Kitchen", "Wardrobe"]:
        show_kitchen_wardrobe(materials=MATERIAL_PRICES)
    else:
        show_bed(bed_prices=BED_PRICES)

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
