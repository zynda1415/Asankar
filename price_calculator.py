import streamlit as st
import pandas as pd
from datetime import datetime
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image as RLImage
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER, TA_RIGHT, TA_LEFT
import io

MATERIAL_PRICES = {
    "MDF": 120,
    "Balloon Press": 160,
    "Glass": 170
}

WASTE_FACTOR = 1.10
DISHWASHER_AREA = 0.51
FRIDGE_DEPTH = 0.6
CABINET_DEPTH = 0.6
OVEN_HEIGHT = 0.85
VITRINE_BASE_HEIGHT = 0.6

def add_custom_css():
    st.markdown("""
    <style>
    /* Modern Card Style */
    .material-card, .product-card, .layout-card {
        border-radius: 12px;
        padding: 10px;
        transition: all 0.3s ease;
        cursor: pointer;
        border: 2px solid transparent;
        background: #f8f9fa;
    }
    
    .material-card:hover, .product-card:hover, .layout-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 16px rgba(0,0,0,0.1);
        border-color: #4CAF50;
    }
    
    /* Image Animation */
    @keyframes fadeIn {
        from { opacity: 0; transform: scale(0.95); }
        to { opacity: 1; transform: scale(1); }
    }
    
    .stImage {
        animation: fadeIn 0.5s ease-in-out;
        border-radius: 8px;
        overflow: hidden;
    }
    
    /* Button Styling */
    .stButton > button {
        border-radius: 8px;
        font-weight: 600;
        transition: all 0.3s ease;
        border: 2px solid #e0e0e0;
    }
    
    .stButton > button:hover {
        transform: scale(1.02);
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        border-color: #4CAF50;
    }
    
    /* Success Badge */
    .success-badge {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 12px 24px;
        border-radius: 25px;
        font-weight: 600;
        display: inline-block;
        margin: 10px 0;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
    }
    
    /* Price Display */
    .price-display {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
        padding: 20px;
        border-radius: 15px;
        text-align: center;
        font-size: 28px;
        font-weight: bold;
        margin: 20px 0;
        box-shadow: 0 6px 20px rgba(245, 87, 108, 0.4);
    }
    
    /* Step Headers */
    .step-header {
        background: linear-gradient(90deg, #4CAF50 0%, #45a049 100%);
        color: white;
        padding: 15px 20px;
        border-radius: 10px;
        margin: 20px 0 15px 0;
        font-size: 20px;
        font-weight: 600;
    }
    
    /* Breakdown Table */
    .breakdown-table {
        background: white;
        border-radius: 10px;
        padding: 15px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    }
    </style>
    """, unsafe_allow_html=True)

def generate_pdf(breakdown_data, calculation_details, material, product, layout=None):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, topMargin=0.5*inch, bottomMargin=0.5*inch)
    story = []
    styles = getSampleStyleSheet()
    
    # Custom Styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#2E7D32'),
        spaceAfter=30,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    
    subtitle_style = ParagraphStyle(
        'CustomSubtitle',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=colors.HexColor('#424242'),
        spaceAfter=12,
        alignment=TA_LEFT,
        fontName='Helvetica-Bold'
    )
    
    # Header
    story.append(Paragraph("KITCHEN & WARDROBE FACTORY", title_style))
    story.append(Paragraph("PRICE QUOTATION", subtitle_style))
    story.append(Spacer(1, 0.2*inch))
    
    # Quote Info
    quote_date = datetime.now().strftime("%B %d, %Y")
    quote_num = datetime.now().strftime("%Y%m%d%H%M%S")
    
    info_data = [
        ['Quote Number:', quote_num, 'Date:', quote_date],
        ['Material:', material, 'Product Type:', product]
    ]
    if layout:
        info_data.append(['Layout:', layout, '', ''])
    
    info_table = Table(info_data, colWidths=[1.5*inch, 2*inch, 1*inch, 1.5*inch])
    info_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#F5F5F5')),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#212121')),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#E0E0E0')),
    ]))
    story.append(info_table)
    story.append(Spacer(1, 0.3*inch))
    
    # Project Details
    story.append(Paragraph("PROJECT DETAILS", subtitle_style))
    story.append(Spacer(1, 0.1*inch))
    
    details_data = [['Description', 'Specification']]
    for key, value in calculation_details.items():
        if isinstance(value, float):
            details_data.append([key, f"{value:.2f} m"])
        elif isinstance(value, bool):
            details_data.append([key, "Yes" if value else "No"])
        else:
            details_data.append([key, str(value)])
    
    details_table = Table(details_data, colWidths=[3*inch, 3*inch])
    details_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#4CAF50')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 11),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ('TOPPADDING', (0, 0), (-1, -1), 10),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#E0E0E0')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F9F9F9')]),
    ]))
    story.append(details_table)
    story.append(Spacer(1, 0.3*inch))
    
    # Area Breakdown
    story.append(Paragraph("AREA CALCULATION BREAKDOWN", subtitle_style))
    story.append(Spacer(1, 0.1*inch))
    
    breakdown_table_data = [['Item', 'Area (m²)', 'Notes']]
    for item, value in breakdown_data.items():
        if value != 0:
            note = ""
            if "deduction" in item.lower():
                note = "Subtracted"
            elif "waste" in item.lower():
                note = "Added (10%)"
            elif "total" in item.lower() or "subtotal" in item.lower():
                note = "Calculated"
            
            breakdown_table_data.append([item, f"{abs(value):.2f}", note])
    
    breakdown_table = Table(breakdown_table_data, colWidths=[2.5*inch, 1.5*inch, 2*inch])
    breakdown_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#4CAF50')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (1, -1), 'LEFT'),
        ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 11),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ('TOPPADDING', (0, 0), (-1, -1), 10),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#E0E0E0')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F9F9F9')]),
    ]))
    
    # Highlight total row
    for i, row in enumerate(breakdown_table_data):
        if 'Total Area' in row[0]:
            breakdown_table.setStyle(TableStyle([
                ('BACKGROUND', (0, i), (-1, i), colors.HexColor('#E8F5E9')),
                ('FONTNAME', (0, i), (-1, i), 'Helvetica-Bold'),
            ]))
    
    story.append(breakdown_table)
    story.append(Spacer(1, 0.3*inch))
    
    # Price Summary
    story.append(Paragraph("PRICE SUMMARY", subtitle_style))
    story.append(Spacer(1, 0.1*inch))
    
    total_area = breakdown_data.get('Total Area', 0)
    material_rate = MATERIAL_PRICES[material]
    material_cost = total_area * material_rate
    
    price_data = [
        ['Description', 'Quantity', 'Rate', 'Amount'],
        [f'{material} Material', f'{total_area:.2f} m²', f'${material_rate}/m²', f'${material_cost:.2f}']
    ]
    
    # Add additional costs if any
    if 'glass_cost' in calculation_details and calculation_details['glass_cost'] > 0:
        price_data.append(['Glass Panels', '-', '-', f"${calculation_details['glass_cost']:.2f}"])
    
    if 'sliding_cost' in calculation_details and calculation_details['sliding_cost'] > 0:
        price_data.append(['Sliding Door System', '-', '-', f"${calculation_details['sliding_cost']:.2f}"])
    
    total_price = calculation_details.get('total_price', material_cost)
    
    price_data.append(['', '', 'SUBTOTAL:', f'${total_price:.2f}'])
    price_data.append(['', '', 'TAX (if applicable):', '$0.00'])
    price_data.append(['', '', 'TOTAL:', f'${total_price:.2f}'])
    
    price_table = Table(price_data, colWidths=[2.5*inch, 1.3*inch, 1.2*inch, 1*inch])
    price_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#4CAF50')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, 0), 'LEFT'),
        ('ALIGN', (2, 0), (-1, -1), 'RIGHT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 11),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -3), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ('TOPPADDING', (0, 0), (-1, -1), 10),
        ('GRID', (0, 0), (-1, -4), 0.5, colors.HexColor('#E0E0E0')),
        ('LINEABOVE', (2, -3), (-1, -3), 1, colors.HexColor('#BDBDBD')),
        ('LINEABOVE', (2, -1), (-1, -1), 2, colors.HexColor('#4CAF50')),
        ('BACKGROUND', (2, -1), (-1, -1), colors.HexColor('#E8F5E9')),
        ('FONTNAME', (2, -1), (-1, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (2, -1), (-1, -1), 12),
        ('ROWBACKGROUNDS', (0, 1), (-1, -4), [colors.white, colors.HexColor('#F9F9F9')]),
    ]))
    story.append(price_table)
    story.append(Spacer(1, 0.4*inch))
    
    # Terms & Conditions
    story.append(Paragraph("TERMS & CONDITIONS", subtitle_style))
    terms_text = """
    1. This quotation is valid for 30 days from the date of issue.<br/>
    2. Prices include materials and installation labor.<br/>
    3. A 50% deposit is required to commence work.<br/>
    4. Final dimensions will be confirmed on-site before production.<br/>
    5. Installation timeline: 2-4 weeks from deposit confirmation.<br/>
    6. Warranty: 2 years on materials and workmanship.<br/>
    """
    story.append(Paragraph(terms_text, styles['Normal']))
    story.append(Spacer(1, 0.3*inch))
    
    # Footer
    footer_style = ParagraphStyle(
        'Footer',
        parent=styles['Normal'],
        fontSize=9,
        textColor=colors.HexColor('#757575'),
        alignment=TA_CENTER
    )
    story.append(Paragraph("Thank you for choosing Kitchen & Wardrobe Factory", footer_style))
    story.append(Paragraph("Contact: info@kwfactory.com | Phone: +1-234-567-8900", footer_style))
    
    doc.build(story)
    buffer.seek(0)
    return buffer

def show_price_calculator():
    add_custom_css()
    
    st.markdown("<h1 style='text-align: center; color: #2E7D32;'>🧮 Price Calculator</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #757575; margin-bottom: 30px;'>Configure your dream kitchen or wardrobe</p>", unsafe_allow_html=True)
    
    if "material" not in st.session_state:
        st.session_state.material = None
    if "product" not in st.session_state:
        st.session_state.product = None
    if "layout" not in st.session_state:
        st.session_state.layout = None
    if "calculation_details" not in st.session_state:
        st.session_state.calculation_details = {}
    
    # Step 1: Material Selection
    st.markdown("<div class='step-header'>📦 Step 1: Select Material</div>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.image("images/materials/mdf.png", width=150)
        if st.button("MDF\n$120/m²", use_container_width=True, key="mat1"):
            st.session_state.material = "MDF"
            st.rerun()
    
    with col2:
        st.image("images/materials/balloon_press.png", width=150)
        if st.button("Balloon Press\n$160/m²", use_container_width=True, key="mat2"):
            st.session_state.material = "Balloon Press"
            st.rerun()
    
    with col3:
        st.image("images/materials/glass.png", width=150)
        if st.button("Glass\n$170/m²", use_container_width=True, key="mat3"):
            st.session_state.material = "Glass"
            st.rerun()
    
    if st.session_state.material is None:
        st.info("👆 Please select a material to continue")
        return
    
    st.markdown(f"<div class='success-badge'>✓ {st.session_state.material} - ${MATERIAL_PRICES[st.session_state.material]}/m²</div>", unsafe_allow_html=True)
    
    # Step 2: Product Selection
    st.markdown("<div class='step-header'>🏠 Step 2: Select Product Type</div>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col1:
        st.write("")
    
    with col2:
        subcol1, subcol2 = st.columns(2)
        with subcol1:
            st.image("images/products/kitchen.png", width=180)
            if st.button("Kitchen", use_container_width=True, key="prod1"):
                st.session_state.product = "Kitchen"
                st.session_state.layout = None
                st.rerun()
        
        with subcol2:
            st.image("images/products/wardrobe.png", width=180)
            if st.button("Wardrobe", use_container_width=True, key="prod2"):
                st.session_state.product = "Wardrobe"
                st.session_state.layout = None
                st.rerun()
    
    with col3:
        st.write("")
    
    if st.session_state.product is None:
        st.info("👆 Please select a product type to continue")
        return
    
    st.markdown(f"<div class='success-badge'>✓ {st.session_state.product}</div>", unsafe_allow_html=True)
    
    if st.session_state.product == "Kitchen":
        show_kitchen_calculator()
    elif st.session_state.product == "Wardrobe":
        show_wardrobe_calculator()

def show_kitchen_calculator():
    st.markdown("<div class='step-header'>🔲 Step 3: Select Kitchen Layout</div>", unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.image("images/layouts/one_wall.png", width=120)
        if st.button("One-Wall", use_container_width=True, key="lay1"):
            st.session_state.layout = "One-Wall"
            st.rerun()
    
    with col2:
        st.image("images/layouts/l_shaped.png", width=120)
        if st.button("L-Shaped", use_container_width=True, key="lay2"):
            st.session_state.layout = "L-Shaped"
            st.rerun()
    
    with col3:
        st.image("images/layouts/u_shaped.png", width=120)
        if st.button("U-Shaped", use_container_width=True, key="lay3"):
            st.session_state.layout = "U-Shaped"
            st.rerun()
    
    with col4:
        st.image("images/layouts/galley.png", width=120)
        if st.button("Galley", use_container_width=True, key="lay4"):
            st.session_state.layout = "Galley"
            st.rerun()
    
    if st.session_state.layout is None:
        st.info("👆 Please select a kitchen layout to continue")
        return
    
    st.markdown(f"<div class='success-badge'>✓ {st.session_state.layout} Layout</div>", unsafe_allow_html=True)
    
    st.markdown("<div class='step-header'>📏 Step 4: Enter Dimensions & Appliances</div>", unsafe_allow_html=True)
    
    if st.session_state.layout == "One-Wall":
        calculate_one_wall()
    elif st.session_state.layout == "L-Shaped":
        calculate_l_shaped()
    elif st.session_state.layout == "U-Shaped":
        calculate_u_shaped()
    elif st.session_state.layout == "Galley":
        calculate_galley()

def calculate_one_wall():
    st.markdown("**Wall Dimensions**")
    col1, col2 = st.columns(2)
    with col1:
        height = st.number_input("Height (m)", min_value=0.0, value=2.4, step=0.1, key="h1")
    with col2:
        length = st.number_input("Length (m)", min_value=0.0, value=3.0, step=0.1, key="l1")
    
    st.markdown("**Appliances & Components**")
    
    col1, col2 = st.columns(2)
    with col1:
        has_fridge = st.checkbox("🧊 Refrigerator", key="fridge1")
        fridge_width = 0.0
        if has_fridge:
            fridge_width = st.number_input("Width (m)", min_value=0.0, value=0.8, step=0.1, key="fw1")
    
    with col2:
        has_dishwasher = st.checkbox("🍽️ Dishwasher", key="dish1")
    
    col1, col2 = st.columns(2)
    with col1:
        has_cabinet = st.checkbox("🗄️ Cabinet", key="cab1")
        cabinet_width = 0.0
        if has_cabinet:
            cabinet_width = st.number_input("Width (m)", min_value=0.0, value=0.6, step=0.1, key="cw1")
    
    with col2:
        has_stove = st.checkbox("🔥 Stove", key="stove1")
        stove_width = 0.0
        has_oven = False
        if has_stove:
            stove_width = st.number_input("Width (m)", min_value=0.0, value=0.6, step=0.1, key="sw1")
            has_oven = st.checkbox("With oven", key="oven1")
    
    has_vitrine = st.checkbox("🪟 Vitrine (glass cabinet)", key="vit1")
    vitrine_width = 0.0
    if has_vitrine:
        vitrine_width = st.number_input("Vitrine width (m)", min_value=0.0, value=0.6, step=0.1, key="vw1")
    
    if height > 0 and length > 0:
        base_area = length * height
        fridge_area = fridge_width * FRIDGE_DEPTH if has_fridge else 0
        cabinet_area = cabinet_width * CABINET_DEPTH if has_cabinet else 0
        dishwasher_area = DISHWASHER_AREA if has_dishwasher else 0
        oven_area = stove_width * OVEN_HEIGHT if (has_stove and has_oven) else 0
        vitrine_area = vitrine_width * (height - VITRINE_BASE_HEIGHT) if has_vitrine else 0
        
        total_area = base_area + fridge_area + cabinet_area - dishwasher_area - oven_area - vitrine_area
        final_area = total_area * WASTE_FACTOR
        price = final_area * MATERIAL_PRICES[st.session_state.material]
        
        details = {
            "Height": height,
            "Length": length,
            "Refrigerator": has_fridge,
            "Refrigerator Width": fridge_width if has_fridge else 0,
            "Dishwasher": has_dishwasher,
            "Cabinet": has_cabinet,
            "Cabinet Width": cabinet_width if has_cabinet else 0,
            "Stove": has_stove,
            "Stove Width": stove_width if has_stove else 0,
            "With Oven": has_oven,
            "Vitrine": has_vitrine,
            "Vitrine Width": vitrine_width if has_vitrine else 0,
            "total_price": price
        }
        
        st.session_state.calculation_details = details
        
        display_breakdown({
            "Base Wall Area": base_area,
            "Refrigerator Area": fridge_area,
            "Cabinet Area": cabinet_area,
            "Dishwasher (deduction)": -dishwasher_area,
            "Oven (deduction)": -oven_area,
            "Vitrine (deduction)": -vitrine_area,
            "Subtotal": total_area,
            "Waste Factor (10%)": final_area - total_area,
            "Total Area": final_area
        }, price)

def calculate_l_shaped():
    st.markdown("**Wall Dimensions**")
    col1, col2, col3 = st.columns(3)
    with col1:
        height = st.number_input("Height (m)", min_value=0.0, value=2.4, step=0.1, key="h2")
    with col2:
        length1 = st.number_input("Wall 1 Length (m)", min_value=0.0, value=3.0, step=0.1, key="l2a")
    with col3:
        length2 = st.number_input("Wall 2 Length (m)", min_value=0.0, value=2.5, step=0.1, key="l2b")
    
    st.markdown("**Appliances & Components**")
    
    col1, col2 = st.columns(2)
    with col1:
        has_fridge = st.checkbox("🧊 Refrigerator", key="fridge2")
        fridge_width = 0.0
        if has_fridge:
            fridge_width = st.number_input("Width (m)", min_value=0.0, value=0.8, step=0.1, key="fw2")
    
    with col2:
        has_dishwasher = st.checkbox("🍽️ Dishwasher", key="dish2")
    
    col1, col2 = st.columns(2)
    with col1:
        has_cabinet = st.checkbox("🗄️ Cabinet", key="cab2")
        cabinet_width = 0.0
        if has_cabinet:
            cabinet_width = st.number_input("Width (m)", min_value=0.0, value=0.6, step=0.1, key="cw2")
    
    with col2:
        has_stove = st.checkbox("🔥 Stove", key="stove2")
        stove_width = 0.0
        has_oven = False
        if has_stove:
            stove_width = st.number_input("Width (m)", min_value=0.0, value=0.6, step=0.1, key="sw2")
            has_oven = st.checkbox("With oven", key="oven2")
    
    has_vitrine = st.checkbox("🪟 Vitrine (glass cabinet)", key="vit2")
    vitrine_width = 0.0
    if has_vitrine:
        vitrine_width = st.number_input("Vitrine width (m)", min_value=0.0, value=0.6, step=0.1, key="vw2")
    
    if height > 0 and length1 > 0 and length2 > 0:
        base_area = (length1 + length2) * height
        fridge_area = fridge_width * FRIDGE_DEPTH if has_fridge else 0
        cabinet_area = cabinet_width * CABINET_DEPTH if has_cabinet else 0
        dishwasher_area = DISHWASHER_AREA if has_dishwasher else 0
        oven_area = stove_width * OVEN_HEIGHT if (has_stove and has_oven) else 0
        vitrine_area = vitrine_width * (height - VITRINE_BASE_HEIGHT) if has_vitrine else 0
        
        total_area = base_area + fridge_area + cabinet_area - dishwasher_area - oven_area - vitrine_area
        final_area = total_area * WASTE_FACTOR
        price = final_area * MATERIAL_PRICES[st.session_state.material]
        
        details = {
            "Height": height,
            "Wall 1 Length": length1,
            "Wall 2 Length": length2,
            "Refrigerator": has_fridge,
            "Refrigerator Width": fridge_width if has_fridge else 0,
            "Dishwasher": has_dishwasher,
            "Cabinet": has_cabinet,
            "Cabinet Width": cabinet_width if has_cabinet else 0,
            "Stove": has_stove,
            "Stove Width": stove_width if has_stove else 0,
            "With Oven": has_oven,
            "Vitrine": has_vitrine,
            "Vitrine Width": vitrine_width if has_vitrine else 0,
            "total_price": price
        }
        
        st.session_state.calculation_details = details
        
        display_breakdown({
            "Base Walls Area": base_area,
            "Refrigerator Area": fridge_area,
            "Cabinet Area": cabinet_area,
            "Dishwasher (deduction)": -dishwasher_area,
            "Oven (deduction)": -oven_area,
            "Vitrine (deduction)": -vitrine_area,
            "Subtotal": total_area,
            "Waste Factor (10%)": final_area - total_area,
            "Total Area": final_area
        }, price)

def calculate_u_shaped():
    st.markdown("**Wall Dimensions**")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        height = st.number_input("Height (m)", min_value=0.0, value=2.4, step=0.1, key="h3")
    with col2:
        length1 = st.number_input("Wall 1 (m)", min_value=0.0, value=3.0, step=0.1, key="l3a")
    with col3:
        length2 = st.number_input("Wall 2 (m)", min_value=0.0, value=2.0, step=0.1, key="l3b")
    with col4:
        length3 = st.number_input("Wall 3 (m)", min_value=0.0, value=3.0, step=0.1, key="l3c")
    
    st.markdown("**Appliances & Components**")
    
    col1, col2 = st.columns(2)
    with col1:
        has_fridge = st.checkbox("🧊 Refrigerator", key="fridge3")
        fridge_width = 0.0
        if has_fridge:
            fridge_width = st.number_input("Width (m)", min_value=0.0, value=0.8, step=0.1, key="fw3")
    
    with col2:
        has_dishwasher = st.checkbox("🍽️ Dishwasher", key="dish3")
    
    col1, col2 = st.columns(2)
    with col1:
        has_cabinet = st.checkbox("🗄️ Cabinet", key="cab3")
        cabinet_width = 0.0
        if has_cabinet:
            cabinet_width = st.number_input("Width (m)", min_value=0.0, value=0.6, step=0.1, key="cw3")
    
    with col2:
        has_stove = st.checkbox("🔥 Stove", key="stove3")
        stove_width = 0.0
        has_oven = False
        if has_stove:
            stove_width = st.number_input("Width (m)", min_value=0.0, value=0.6, step=0.1, key="sw3")
            has_oven = st.checkbox("With oven", key="oven3")
    
    has_vitrine = st.checkbox("🪟 Vitrine (glass cabinet)", key="vit3")
    vitrine_width = 0.0
    if has_vitrine:
        vitrine_width = st.number_input("Vitrine width (m)", min_value=0.0, value=0.6, step=0.1, key="vw3")
    
    if height > 0 and length1 > 0 and length2 > 0 and length3 > 0:
        base_area = (length1 + length2 + length3) * height
        fridge_area = fridge_width * FRIDGE_DEPTH if has_fridge else 0
        cabinet_area = cabinet_width * CABINET_DEPTH if has_cabinet else 0
        dishwasher_area = DISHWASHER_AREA if has_dishwasher else 0
        oven_area = stove_width * OVEN_HEIGHT if (has_stove and has_oven) else 0
        vitrine_area = vitrine_width * (height - VITRINE_BASE_HEIGHT) if has_vitrine else 0
        
        total_area = base_area + fridge_area + cabinet_area - dishwasher_area - oven_area - vitrine_area
        final_area = total_area * WASTE_FACTOR
        price = final_area * MATERIAL_PRICES[st.session_state.material]
        
        details = {
            "Height": height,
            "Wall 1 Length": length1,
            "Wall 2 Length": length2,
            "Wall 3 Length": length3,
            "Refrigerator": has_fridge,
            "Refrigerator Width": fridge_width if has_fridge else 0,
            "Dishwasher": has_dishwasher,
            "Cabinet": has_cabinet,
            "Cabinet Width": cabinet_width if has_cabinet else 0,
            "Stove": has_stove,
            "Stove Width": stove_width if has_stove else 0,
            "With Oven": has_oven,
            "Vitrine": has_vitrine,
            "Vitrine Width": vitrine_width if has_vitrine else 0,
            "total_price": price
        }
        
        st.session_state.calculation_details = details
        
        display_breakdown({
            "Base Walls Area": base_area,
            "Refrigerator Area": fridge_area,
            "Cabinet Area": cabinet_area,
            "Dishwasher (deduction)": -dishwasher_area,
            "Oven (deduction)": -oven_area,
            "Vitrine (deduction)": -vitrine_area,
            "Subtotal": total_area,
            "Waste Factor (10%)": final_area - total_area,
            "Total Area": final_area
        }, price)

def calculate_galley():
    st.markdown("**Wall Dimensions**")
    col1, col2, col3 = st.columns(3)
    with col1:
        height = st.number_input("Height (m)", min_value=0.0, value=2.4, step=0.1, key="h4")
    with col2:
        length1 = st.number_input("Wall 1 Length (m)", min_value=0.0, value=3.0, step=0.1, key="l4a")
    with col3:
        length2 = st.number_input("Wall 2 Length (m)", min_value=0.0, value=3.0, step=0.1, key="l4b")
    
    st.markdown("**Appliances & Components**")
    
    col1, col2 = st.columns(2)
    with col1:
        has_fridge = st.checkbox("🧊 Refrigerator", key="fridge4")
        fridge_width = 0.0
        if has_fridge:
            fridge_width = st.number_input("Width (m)", min_value=0.0, value=0.8, step=0.1, key="fw4")
    
    with col2:
        has_dishwasher = st.checkbox("🍽️ Dishwasher", key="dish4")
    
    col1, col2 = st.columns(2)
    with col1:
        has_cabinet = st.checkbox("🗄️ Cabinet", key="cab4")
        cabinet_width = 0.0
        if has_cabinet:
            cabinet_width = st.number_input("Width (m)", min_value=0.0, value=0.6, step=0.1, key="cw4")
    
    with col2:
        has_stove = st.checkbox("🔥 Stove", key="stove4")
        stove_width = 0.0
        has_oven = False
        if has_stove:
            stove_width = st.number_input("Width (m)", min_value=0.0, value=0.6, step=0.1, key="sw4")
            has_oven = st.checkbox("With oven", key="oven4")
    
    has_vitrine = st.checkbox("🪟 Vitrine (glass cabinet)", key="vit4")
    vitrine_width = 0.0
    if has_vitrine:
        vitrine_width = st.number_input("Vitrine width (m)", min_value=0.0, value=0.6, step=0.1, key="vw4")
    
    if height > 0 and length1 > 0 and length2 > 0:
        base_area = (length1 + length2) * height
        fridge_area = fridge_width * FRIDGE_DEPTH if has_fridge else 0
        cabinet_area = cabinet_width * CABINET_DEPTH if has_cabinet else 0
        dishwasher_area = DISHWASHER_AREA if has_dishwasher else 0
        oven_area = stove_width * OVEN_HEIGHT if (has_stove and has_oven) else 0
        vitrine_area = vitrine_width * (height - VITRINE_BASE_HEIGHT) if has_vitrine else 0
        
        total_area = base_area + fridge_area + cabinet_area - dishwasher_area - oven_area - vitrine_area
        final_area = total_area * WASTE_FACTOR
        price = final_area * MATERIAL_PRICES[st.session_state.material]
        
        details = {
            "Height": height,
            "Wall 1 Length": length1,
            "Wall 2 Length": length2,
            "Refrigerator": has_fridge,
            "Refrigerator Width": fridge_width if has_fridge else 0,
            "Dishwasher": has_dishwasher,
            "Cabinet": has_cabinet,
            "Cabinet Width": cabinet_width if has_cabinet else 0,
            "Stove": has_stove,
            "Stove Width": stove_width if has_stove else 0,
            "With Oven": has_oven,
            "Vitrine": has_vitrine,
            "Vitrine Width": vitrine_width if has_vitrine else 0,
            "total_price": price
        }
        
        st.session_state.calculation_details = details
        
        display_breakdown({
            "Base Walls Area": base_area,
            "Refrigerator Area": fridge_area,
            "Cabinet Area": cabinet_area,
            "Dishwasher (deduction)": -dishwasher_area,
            "Oven (deduction)": -oven_area,
            "Vitrine (deduction)": -vitrine_area,
            "Subtotal": total_area,
            "Waste Factor (10%)": final_area - total_area,
            "Total Area": final_area
        }, price)

def show_wardrobe_calculator():
    st.markdown("<div class='step-header'>📏 Step 3: Wardrobe Configuration</div>", unsafe_allow_html=True)
    
    st.markdown("**Basic Dimensions**")
    col1, col2 = st.columns(2)
    with col1:
        height = st.number_input("Height (m)", min_value=0.0, value=2.4, step=0.1, key="wh")
    with col2:
        width = st.number_input("Width (m)", min_value=0.0, value=2.0, step=0.1, key="ww")
    
    st.markdown("**Additional Features**")
    
    col1, col2 = st.columns(2)
    with col1:
        has_shelves = st.checkbox("📚 Add shelves", key="shelves")
        num_shelves = 0
        if has_shelves:
            num_shelves = st.number_input("Number of shelves", min_value=0, max_value=20, value=5, step=1, key="ns")
    
    with col2:
        door_type = st.radio("🚪 Door type", ["Hinged", "Sliding"], key="door")
    
    has_mirror = st.checkbox("🪞 Mirror/Glass panels", key="mirror")
    glass_area = 0.0
    if has_mirror:
        col1, col2 = st.columns(2)
        with col1:
            glass_height = st.number_input("Glass height (m)", min_value=0.0, value=2.0, step=0.1, key="gh")
        with col2:
            glass_width = st.number_input("Glass width (m)", min_value=0.0, value=1.0, step=0.1, key="gw")
        glass_area = glass_height * glass_width
    
    if height > 0 and width > 0:
        base_area = height * width
        shelf_area = width * CABINET_DEPTH * num_shelves if has_shelves else 0
        
        total_area = (base_area + shelf_area + glass_area) * WASTE_FACTOR
        
        material_price = total_area * MATERIAL_PRICES[st.session_state.material]
        
        glass_cost = glass_area * 50 if has_mirror else 0
        sliding_cost = 200 if door_type == "Sliding" else 0
        
        total_price = material_price + glass_cost + sliding_cost
        
        details = {
            "Height": height,
            "Width": width,
            "Shelves": has_shelves,
            "Number of Shelves": num_shelves,
            "Door Type": door_type,
            "Mirror/Glass": has_mirror,
            "Glass Height": glass_height if has_mirror else 0,
            "Glass Width": glass_width if has_mirror else 0,
            "glass_cost": glass_cost,
            "sliding_cost": sliding_cost,
            "total_price": total_price
        }
        
        st.session_state.calculation_details = details
        
        breakdown = {
            "Base Wardrobe Area": base_area,
            "Shelves Area": shelf_area,
            "Glass Panel Area": glass_area,
            "Subtotal": base_area + shelf_area + glass_area,
            "Waste Factor (10%)": total_area - (base_area + shelf_area + glass_area),
            "Total Area": total_area
        }
        
        display_breakdown(breakdown, material_price, glass_cost=glass_cost, sliding_cost=sliding_cost, total_price=total_price)

def display_breakdown(breakdown, material_price, glass_cost=0, sliding_cost=0, total_price=None):
    st.markdown("---")
    st.markdown("<div class='step-header'>📊 Price Breakdown</div>", unsafe_allow_html=True)
    
    df_data = []
    for item, value in breakdown.items():
        if value != 0:
            df_data.append({"Component": item, "Area (m²)": f"{value:.2f}"})
    
    df = pd.DataFrame(df_data)
    
    st.markdown("<div class='breakdown-table'>", unsafe_allow_html=True)
    st.dataframe(df, use_container_width=True, hide_index=True)
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Material", st.session_state.material)
        st.metric("Price per m²", f"${MATERIAL_PRICES[st.session_state.material]}")
    with col2:
        st.metric("Material Cost", f"${material_price:.2f}")
        if glass_cost > 0:
            st.metric("Glass Cost", f"${glass_cost:.2f}")
        if sliding_cost > 0:
            st.metric("Sliding System", f"${sliding_cost:.2f}")
    
    final_price = total_price if total_price is not None else material_price
    
    st.markdown(f"<div class='price-display'>💰 TOTAL PRICE: ${final_price:,.2f}</div>", unsafe_allow_html=True)
    
    st.markdown("---")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🔄 New Calculation", use_container_width=True):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()
    
    with col2:
        # Generate PDF
        breakdown_data = breakdown
        calculation_details = st.session_state.calculation_details
        material = st.session_state.material
        product = st.session_state.product
        layout = st.session_state.layout if st.session_state.product == "Kitchen" else None
        
        pdf_buffer = generate_pdf(breakdown_data, calculation_details, material, product, layout)
        
        st.download_button(
            label="📄 Download PDF Quote",
            data=pdf_buffer,
            file_name=f"quotation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
            mime="application/pdf",
            use_container_width=True
        )
    
    with col3:
        whatsapp_text = f"Hi! I got a quote: {st.session_state.product} in {st.session_state.material} - ${final_price:,.2f}"
        whatsapp_url = f"https://wa.me/?text={whatsapp_text.replace(' ', '%20')}"
        st.markdown(f"[💬 Share on WhatsApp]({whatsapp_url})", unsafe_allow_html=True)
