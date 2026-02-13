import streamlit as st
import pandas as pd
from datetime import datetime
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image as RLImage
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER, TA_LEFT
import io

MATERIAL_PRICES = {"MDF": 120, "Balloon Press": 160, "Glass": 170}
FRIDGE_DEPTH, CABINET_DEPTH, OVEN_HEIGHT, VITRINE_BASE_HEIGHT = 0.6, 0.6, 0.85, 0.6
DISHWASHER_AREA = 0.51

BED_PRICES = {
    "simple": {"90cm": 310, "120cm": 350, "180cm": 420},
    "rabbet": {"90cm": 500, "120cm": 590, "180cm": 750},
    "mdf": {"90cm": 200, "120cm": 230, "180cm": 300}
}

def css():
    st.markdown("""<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap');
    * {font-family: 'Inter', sans-serif;}
    .stButton>button {border-radius: 10px; font-weight: 500; transition: all 0.2s; border: 1px solid #e5e7eb; 
        background: white; color: #1f2937; padding: 0.75rem 1.5rem; box-shadow: 0 1px 3px rgba(0,0,0,0.1);}
    .stButton>button:hover {transform: translateY(-2px); box-shadow: 0 4px 12px rgba(0,0,0,0.15); 
        border-color: #10b981; background: #f0fdf4;}
    .stImage {border-radius: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);}
    .success-badge {background: #10b981; color: white; padding: 8px 20px; border-radius: 20px; 
        font-weight: 600; font-size: 15px; display: inline-block; margin: 12px 0;}
    .price-box {background: linear-gradient(135deg, #1f2937 0%, #374151 100%); color: white; 
        padding: 30px; border-radius: 15px; text-align: center; font-size: 36px; font-weight: 700; 
        margin: 25px 0; box-shadow: 0 10px 25px rgba(0,0,0,0.2);}
    .step-header {background: #f9fafb; color: #1f2937; padding: 15px 25px; border-radius: 10px; 
        border-left: 5px solid #10b981; margin: 25px 0 20px 0; font-size: 18px; font-weight: 600;}
    #MainMenu, footer {visibility: hidden;}
    </style>""", unsafe_allow_html=True)

def gen_pdf(items):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, topMargin=0.5*inch, bottomMargin=0.5*inch)
    story = []
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle('Title', parent=styles['Heading1'], fontSize=24, 
        textColor=colors.HexColor('#10b981'), spaceAfter=30, alignment=TA_CENTER, fontName='Helvetica-Bold')
    
    subtitle_style = ParagraphStyle('Subtitle', parent=styles['Heading2'], fontSize=14, 
        textColor=colors.HexColor('#1f2937'), spaceAfter=15, alignment=TA_LEFT, fontName='Helvetica-Bold')
    
    # Logo placeholder
    story.append(Paragraph("ASANKAR COMPANY", title_style))
    story.append(Paragraph("Price Quotation", subtitle_style))
    story.append(Spacer(1, 0.3*inch))
    
    # Quote info
    quote_date = datetime.now().strftime("%B %d, %Y")
    quote_num = datetime.now().strftime("%Y%m%d%H%M%S")
    
    info_data = [['Quote Number', quote_num, 'Date', quote_date]]
    info_table = Table(info_data, colWidths=[1.5*inch, 2*inch, 1*inch, 2*inch])
    info_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#f9fafb')),
        ('GRID', (0,0), (-1,-1), 1, colors.HexColor('#e5e7eb')),
        ('FONTNAME', (0,0), (-1,-1), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 10),
        ('PADDING', (0,0), (-1,-1), 10),
    ]))
    story.append(info_table)
    story.append(Spacer(1, 0.4*inch))
    
    # Items table
    story.append(Paragraph("Items", subtitle_style))
    table_data = [['Product', 'Details', 'Price']]
    total = 0
    
    for item in items:
        table_data.append([item['product'], item['details'], f"${item['price']:,.2f}"])
        total += item['price']
    
    table_data.append(['', 'TOTAL', f"${total:,.2f}"])
    
    items_table = Table(table_data, colWidths=[2*inch, 3*inch, 1.5*inch])
    items_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#10b981')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,0), 11),
        ('ALIGN', (2,0), (2,-1), 'RIGHT'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#e5e7eb')),
        ('FONTNAME', (0,1), (-1,-2), 'Helvetica'),
        ('FONTSIZE', (0,1), (-1,-2), 9),
        ('BACKGROUND', (0,-1), (-1,-1), colors.HexColor('#d1fae5')),
        ('FONTNAME', (0,-1), (-1,-1), 'Helvetica-Bold'),
        ('FONTSIZE', (0,-1), (-1,-1), 12),
        ('PADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(items_table)
    story.append(Spacer(1, 0.5*inch))
    
    # Terms
    story.append(Paragraph("Terms & Conditions", subtitle_style))
    terms = """• Valid 30 days<br/>• Includes materials & installation<br/>• 50% deposit required<br/>
    • 2-4 weeks delivery<br/>• 2 year warranty<br/><br/>Contact: info@asankar.com | +964-xxx-xxxx"""
    story.append(Paragraph(terms, styles['Normal']))
    
    doc.build(story)
    buffer.seek(0)
    return buffer

def calc_kitchen_wardrobe(prod, mat):
    st.markdown(f"<div class='step-header'>📏 Dimensions & Appliances</div>", unsafe_allow_html=True)
    
    c1, c2 = st.columns(2)
    with c1: h = st.number_input("Height (m)", 0.0, value=2.4, step=0.1, key="h")
    with c2: l = st.number_input("Length (m)", 0.0, value=3.0, step=0.1, key="l")
    
    st.markdown("**Appliances**")
    c1, c2 = st.columns(2)
    with c1:
        fr = st.checkbox("🧊 Refrigerator", key="fr")
        fw = st.number_input("Width (m)", 0.0, value=0.8, step=0.1, key="fw") if fr else 0
    with c2: di = st.checkbox("🍽️ Dishwasher", key="di")
    
    c1, c2 = st.columns(2)
    with c1:
        ca = st.checkbox("🗄️ Cabinet", key="ca")
        cw = st.number_input("Width (m)", 0.0, value=0.6, step=0.1, key="cw") if ca else 0
    with c2:
        st_ = st.checkbox("🔥 Stove", key="st")
        sw, ov = (st.number_input("Width (m)", 0.0, value=0.6, step=0.1, key="sw"), 
                  st.checkbox("With oven", key="ov")) if st_ else (0, False)
    
    if h > 0 and l > 0:
        ba = l * h
        fa = fw * FRIDGE_DEPTH if fr else 0
        caa = cw * CABINET_DEPTH if ca else 0
        da = DISHWASHER_AREA if di else 0
        oa = sw * OVEN_HEIGHT if (st_ and ov) else 0
        
        total = ba + fa + caa - da - oa
        price = total * MATERIAL_PRICES[mat]
        
        st.markdown("---")
        st.markdown(f"<div class='step-header'>📊 Breakdown</div>", unsafe_allow_html=True)
        
        df = pd.DataFrame([
            {"Item": "Base Area", "Area": f"{ba:.2f} m²"},
            {"Item": "Refrigerator", "Area": f"{fa:.2f} m²"},
            {"Item": "Cabinet", "Area": f"{caa:.2f} m²"},
            {"Item": "Dishwasher (-)", "Area": f"{-da:.2f} m²"},
            {"Item": "Oven (-)", "Area": f"{-oa:.2f} m²"},
            {"Item": "TOTAL", "Area": f"{total:.2f} m²"}
        ])
        st.dataframe(df, use_container_width=True, hide_index=True)
        
        st.markdown(f"<div class='price-box'>💰 ${price:,.2f}</div>", unsafe_allow_html=True)
        
        return {
            'product': prod,
            'details': f"{mat} | {h}m x {l}m | {total:.2f}m²",
            'price': price
        }
    return None

def calc_bed(size, bed_type):
    price = BED_PRICES[bed_type][size]
    
    st.markdown("---")
    st.markdown(f"<div class='step-header'>📊 Summary</div>", unsafe_allow_html=True)
    
    df = pd.DataFrame([
        {"Item": "Size", "Value": size},
        {"Item": "Type", "Value": bed_type.upper()},
        {"Item": "Price", "Value": f"${price}"}
    ])
    st.dataframe(df, use_container_width=True, hide_index=True)
    
    st.markdown(f"<div class='price-box'>💰 ${price:,.2f}</div>", unsafe_allow_html=True)
    
    return {
        'product': f"Bed {size}",
        'details': f"{bed_type.upper()} type",
        'price': price
    }

def show_price_calculator():
    css()
    
    # Logo
    st.markdown("<h1 style='text-align: center; color: #10b981; margin: 20px 0;'>🏢 ASANKAR</h1>", 
                unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #6b7280; margin-bottom: 40px;'>Price Calculator</p>", 
                unsafe_allow_html=True)
    
    if "cart" not in st.session_state:
        st.session_state.cart = []
    if "product" not in st.session_state:
        st.session_state.product = None
    if "material" not in st.session_state:
        st.session_state.material = None
    if "bed_size" not in st.session_state:
        st.session_state.bed_size = None
    if "bed_type" not in st.session_state:
        st.session_state.bed_type = None
    
    # Step 1: Product Selection
    st.markdown("<div class='step-header'>🛋️ Step 1: Select Product</div>", unsafe_allow_html=True)
    st.image("images/products/products.png", use_column_width=True)
    
    c1, c2, c3 = st.columns(3)
    with c1:
        if st.button("Kitchen", use_container_width=True, key="prod_kitchen"):
            st.session_state.product = "Kitchen"
            st.session_state.material = None
            st.rerun()
    with c2:
        if st.button("Wardrobe", use_container_width=True, key="prod_wardrobe"):
            st.session_state.product = "Wardrobe"
            st.session_state.material = None
            st.rerun()
    with c3:
        if st.button("Bed", use_container_width=True, key="prod_bed"):
            st.session_state.product = "Bed"
            st.session_state.bed_size = None
            st.session_state.bed_type = None
            st.rerun()
    
    if st.session_state.product is None:
        return
    
    st.markdown(f"<div class='success-badge'>✓ {st.session_state.product}</div>", unsafe_allow_html=True)
    
    # Kitchen/Wardrobe Path
    if st.session_state.product in ["Kitchen", "Wardrobe"]:
        st.markdown("<div class='step-header'>📦 Step 2: Select Material</div>", unsafe_allow_html=True)
        st.image("images/materials/material.png", use_column_width=True)
        
        c1, c2, c3 = st.columns(3)
        with c1:
            if st.button("MDF - $120/m²", use_container_width=True, key="mat_mdf"):
                st.session_state.material = "MDF"
                st.rerun()
        with c2:
            if st.button("Balloon Press - $160/m²", use_container_width=True, key="mat_bp"):
                st.session_state.material = "Balloon Press"
                st.rerun()
        with c3:
            if st.button("Glass - $170/m²", use_container_width=True, key="mat_glass"):
                st.session_state.material = "Glass"
                st.rerun()
        
        if st.session_state.material:
            st.markdown(f"<div class='success-badge'>✓ {st.session_state.material}</div>", 
                       unsafe_allow_html=True)
            
            item = calc_kitchen_wardrobe(st.session_state.product, st.session_state.material)
            
            if item:
                st.markdown("---")
                c1, c2, c3 = st.columns(3)
                with c1:
                    if st.button("➕ Add to Cart", use_container_width=True):
                        st.session_state.cart.append(item)
                        st.session_state.product = None
                        st.session_state.material = None
                        st.success("Added to cart!")
                        st.rerun()
                with c2:
                    if st.button("🔄 Clear", use_container_width=True):
                        st.session_state.product = None
                        st.session_state.material = None
                        st.rerun()
                with c3:
                    if st.session_state.cart:
                        pdf = gen_pdf(st.session_state.cart)
                        st.download_button("📄 Generate PDF", pdf, 
                                         f"quote_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf", 
                                         "application/pdf", use_container_width=True)
    
    # Bed Path
    elif st.session_state.product == "Bed":
        st.markdown("<div class='step-header'>📐 Step 2: Select Size</div>", unsafe_allow_html=True)
        st.image("images/products/bed_size.png", use_column_width=True)
        
        c1, c2, c3 = st.columns(3)
        with c1:
            if st.button("90cm", use_container_width=True, key="size_90"):
                st.session_state.bed_size = "90cm"
                st.rerun()
        with c2:
            if st.button("120cm", use_container_width=True, key="size_120"):
                st.session_state.bed_size = "120cm"
                st.rerun()
        with c3:
            if st.button("180cm", use_container_width=True, key="size_180"):
                st.session_state.bed_size = "180cm"
                st.rerun()
        
        if st.session_state.bed_size:
            st.markdown(f"<div class='success-badge'>✓ {st.session_state.bed_size}</div>", 
                       unsafe_allow_html=True)
            
            st.markdown("<div class='step-header'>🛏️ Step 3: Select Type</div>", unsafe_allow_html=True)
            st.image("images/materials/bed_types.png", use_column_width=True)
            
            c1, c2, c3 = st.columns(3)
            with c1:
                if st.button("Simple", use_container_width=True, key="type_simple"):
                    st.session_state.bed_type = "simple"
                    st.rerun()
            with c2:
                if st.button("Rabbet", use_container_width=True, key="type_rabbet"):
                    st.session_state.bed_type = "rabbet"
                    st.rerun()
            with c3:
                if st.button("MDF", use_container_width=True, key="type_mdf"):
                    st.session_state.bed_type = "mdf"
                    st.rerun()
            
            if st.session_state.bed_type:
                st.markdown(f"<div class='success-badge'>✓ {st.session_state.bed_type.upper()}</div>", 
                           unsafe_allow_html=True)
                
                item = calc_bed(st.session_state.bed_size, st.session_state.bed_type)
                
                st.markdown("---")
                c1, c2, c3 = st.columns(3)
                with c1:
                    if st.button("➕ Add to Cart", use_container_width=True, key="add_bed"):
                        st.session_state.cart.append(item)
                        st.session_state.product = None
                        st.session_state.bed_size = None
                        st.session_state.bed_type = None
                        st.success("Added to cart!")
                        st.rerun()
                with c2:
                    if st.button("🔄 Clear", use_container_width=True, key="clear_bed"):
                        st.session_state.product = None
                        st.session_state.bed_size = None
                        st.session_state.bed_type = None
                        st.rerun()
                with c3:
                    if st.session_state.cart:
                        pdf = gen_pdf(st.session_state.cart)
                        st.download_button("📄 Generate PDF", pdf, 
                                         f"quote_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf", 
                                         "application/pdf", use_container_width=True)
    
    # Cart display
    if st.session_state.cart:
        st.markdown("---")
        st.markdown("<div class='step-header'>🛒 Cart</div>", unsafe_allow_html=True)
        
        cart_df = pd.DataFrame([
            {"Product": item['product'], "Details": item['details'], "Price": f"${item['price']:,.2f}"}
            for item in st.session_state.cart
        ])
        st.dataframe(cart_df, use_container_width=True, hide_index=True)
        
        total = sum(item['price'] for item in st.session_state.cart)
        st.markdown(f"<div class='price-box'>TOTAL: ${total:,.2f}</div>", unsafe_allow_html=True)
        
        if st.button("🗑️ Clear All", use_container_width=True):
            st.session_state.cart = []
            st.rerun()
