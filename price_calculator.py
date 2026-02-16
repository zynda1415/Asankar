# price_calculator.py
import streamlit as st
from kitchen_wardrobe import show_kitchen_wardrobe
from bed import show_bed
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
import datetime

MATERIAL_PRICES = {"MDF": 120, "Balloon Press": 160, "Glass": 170}
BED_PRICES = {
    "Simple": {"90": 310, "120": 350, "180": 420},
    "Rabbet": {"90": 500, "120": 590, "180": 750},
    "MDF": {"90": 200, "120": 230, "180": 300}
}

if "cart" not in st.session_state:
    st.session_state.cart = []

def show_price_calculator():
    st.markdown("<h2 style='text-align: center;'>حاسبة الأسعار</h2>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    
    product_type = st.radio(
        "اختر نوع المنتج",
        ["Kitchen", "Wardrobe", "Bed"],
        horizontal=True
    )
    
    st.image("images/products.png", use_container_width=True)
    st.markdown("---")
    
    if product_type in ["Kitchen", "Wardrobe"]:
        show_kitchen_wardrobe(materials=MATERIAL_PRICES, product_type=product_type)
    else:
        show_bed(bed_prices=BED_PRICES)

    if st.session_state.cart:
        st.markdown("---")
        st.markdown("<h3>🛒 السلة</h3>", unsafe_allow_html=True)
        
        cart_data = []
        total = 0
        
        for idx, item in enumerate(st.session_state.cart):
            details_parts = []
            for k, v in item.items():
                if k not in ["Product", "Price"]:
                    details_parts.append(f"{k}: {v}")
            details = " | ".join(details_parts)
            
            cart_data.append([
                str(idx + 1),
                item["Product"],
                details,
                f"${item['Price']}"
            ])
            total += item["Price"]
        
        st.table(cart_data)
        st.markdown(f"<h4 style='text-align: right;'>المجموع: ${round(total, 2)}</h4>", unsafe_allow_html=True)

        col1, col2, col3 = st.columns([2, 1, 1])
        
        with col2:
            if st.button("🗑️ مسح السلة", use_container_width=True):
                st.session_state.cart = []
                st.rerun()
        
        with col3:
            if st.button("📄 إنشاء PDF", use_container_width=True):
                generate_pdf(st.session_state.cart, total)

def generate_pdf(cart, total):
    filename = "quotation.pdf"
    doc = SimpleDocTemplate(filename, pagesize=A4)
    elements = []
    styles = getSampleStyleSheet()

    elements.append(Paragraph("Asankar Factory - Quotation", styles["Heading1"]))
    elements.append(Spacer(1, 12))
    elements.append(Paragraph(f"Date: {datetime.date.today()}", styles["Normal"]))
    elements.append(Spacer(1, 20))

    data = [["#", "Product", "Details", "Price"]]
    
    for idx, item in enumerate(cart, 1):
        details = " - ".join([f"{k}: {v}" for k, v in item.items() if k not in ["Product", "Price"]])
        data.append([str(idx), item["Product"], details, f"${item['Price']}"])
    
    data.append(["", "", "Total", f"${round(total, 2)}"])

    table = Table(data, colWidths=[30, 100, 250, 80])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, -1), (-1, -1), colors.lightgrey),
        ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    
    elements.append(table)
    elements.append(Spacer(1, 20))
    elements.append(Paragraph("Terms & Conditions:", styles["Heading3"]))
    elements.append(Paragraph("• Prices are valid for 30 days from the quotation date.", styles["Normal"]))
    elements.append(Paragraph("• 50% deposit required to start production.", styles["Normal"]))
    elements.append(Paragraph("• Delivery time: 2-4 weeks depending on order size.", styles["Normal"]))
    
    doc.build(elements)

    with open(filename, "rb") as f:
        st.download_button(
            "⬇️ تحميل PDF",
            f,
            file_name=f"asankar_quotation_{datetime.date.today()}.pdf",
            mime="application/pdf"
        )
