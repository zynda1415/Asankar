import streamlit as st
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image as RLImage
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER, TA_RIGHT
import os

MATERIAL_PRICES = {"MDF": 120, "Balloon Press": 160, "Glass": 170}
BED_PRICES = {
    "Simple": {"90": 310, "120": 350, "180": 420},
    "Rabbet": {"90": 500, "120": 590, "180": 750},
    "MDF": {"90": 200, "120": 230, "180": 300}
}

# Material descriptions
MATERIAL_INFO = {
    "MDF": "🪵 Medium Density Fiberboard - Smooth, durable, and affordable",
    "Balloon Press": "💪 High-pressure laminate - Extra strong and resistant",
    "Glass": "✨ Premium tempered glass - Elegant and modern"
}

BED_TYPE_INFO = {
    "Simple": "🛏️ Classic design - Clean lines and timeless style",
    "Rabbet": "🎨 Rabbeted joints - Superior craftsmanship",
    "MDF": "🌟 MDF construction - Economical and versatile"
}

if "cart" not in st.session_state:
    st.session_state.cart = []
if "step" not in st.session_state:
    st.session_state.step = 1
if "product_type" not in st.session_state:
    st.session_state.product_type = None

def reset_calculator():
    st.session_state.step = 1
    st.session_state.product_type = None

def show_price_calculator():
    st.markdown("""
    <div style='text-align: center; padding: 20px;'>
        <h1 style='color: #1e3c72; font-size: 42px;'>💰 Price Calculator</h1>
        <p style='font-size: 18px; color: #666;'>Get instant quotes for your dream furniture</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Progress indicator
    total_steps = 3 if st.session_state.product_type in ["Kitchen", "Wardrobe"] else 4
    if st.session_state.product_type:
        progress = st.session_state.step / total_steps
        st.progress(progress)
        st.markdown(f"**Step {st.session_state.step} of {total_steps}**")
    
    st.markdown("---")
    
    # STEP 1: Product Selection
    if st.session_state.step == 1:
        show_product_selection()
    
    # STEP 2: Material/Size Selection
    elif st.session_state.step == 2:
        if st.session_state.product_type in ["Kitchen", "Wardrobe"]:
            show_material_selection()
        else:  # Bed
            show_bed_size_selection()
    
    # STEP 3: Measurements/Type
    elif st.session_state.step == 3:
        if st.session_state.product_type in ["Kitchen", "Wardrobe"]:
            show_measurements()
        else:  # Bed
            show_bed_type_selection()
    
    # STEP 4: Calculation Result (only for Kitchen/Wardrobe after step 3)
    elif st.session_state.step == 4:
        if st.session_state.product_type == "Bed":
            show_bed_result()
    
    # Shopping Cart Section
    st.markdown("---")
    show_cart()

def show_product_selection():
    st.markdown("### 🏠 Select Your Product Type")
    
    # Display product images if available
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if os.path.exists("products.png"):
            st.image("products.png", use_container_width=True)
        st.markdown("""
        <div class='custom-card' style='text-align: center;'>
            <div style='font-size: 60px; margin-bottom: 10px;'>🍳</div>
            <h3>Kitchen</h3>
            <p style='color: #666;'>Custom kitchen cabinets and storage</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Select Kitchen", key="btn_kitchen", use_container_width=True):
            st.session_state.product_type = "Kitchen"
            st.session_state.step = 2
            st.rerun()
    
    with col2:
        st.markdown("""
        <div class='custom-card' style='text-align: center;'>
            <div style='font-size: 60px; margin-bottom: 10px;'>👔</div>
            <h3>Wardrobe</h3>
            <p style='color: #666;'>Elegant wardrobe solutions</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Select Wardrobe", key="btn_wardrobe", use_container_width=True):
            st.session_state.product_type = "Wardrobe"
            st.session_state.step = 2
            st.rerun()
    
    with col3:
        st.markdown("""
        <div class='custom-card' style='text-align: center;'>
            <div style='font-size: 60px; margin-bottom: 10px;'>🛏️</div>
            <h3>Bed</h3>
            <p style='color: #666;'>Comfortable bed frames</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Select Bed", key="btn_bed", use_container_width=True):
            st.session_state.product_type = "Bed"
            st.session_state.step = 2
            st.rerun()

def show_material_selection():
    st.markdown(f"### 🎨 Choose Material for Your {st.session_state.product_type}")
    
    if os.path.exists("materials.png"):
        st.image("materials.png", use_container_width=True)
    
    col1, col2, col3 = st.columns(3)
    
    materials = ["MDF", "Balloon Press", "Glass"]
    cols = [col1, col2, col3]
    
    for idx, material in enumerate(materials):
        with cols[idx]:
            st.markdown(f"""
            <div class='custom-card' style='text-align: center;'>
                <h3>{material}</h3>
                <div class='price-tag' style='font-size: 18px; padding: 10px 20px;'>${MATERIAL_PRICES[material]}/m²</div>
                <p style='margin-top: 15px; color: #666;'>{MATERIAL_INFO[material]}</p>
            </div>
            """, unsafe_allow_html=True)
            if st.button(f"Select {material}", key=f"btn_mat_{material}", use_container_width=True):
                st.session_state.selected_material = material
                st.session_state.step = 3
                st.rerun()
    
    if st.button("← Back", key="back_material"):
        st.session_state.step = 1
        st.rerun()

def show_measurements():
    st.markdown(f"### 📏 Enter Dimensions for Your {st.session_state.product_type}")
    st.markdown(f"**Selected Material:** {st.session_state.selected_material} (${MATERIAL_PRICES[st.session_state.selected_material]}/m²)")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 📐 Basic Dimensions")
        height = st.number_input("Height (meters)", min_value=0.0, max_value=10.0, value=2.5, step=0.1, key="height")
        length = st.number_input("Length (meters)", min_value=0.0, max_value=20.0, value=3.0, step=0.1, key="length")
    
    with col2:
        st.markdown("#### 🔧 Additional Features")
        if st.session_state.product_type == "Kitchen":
            fridge_width = st.number_input("Fridge Width (m)", min_value=0.0, max_value=5.0, value=0.0, step=0.1, key="fridge")
            dishwasher = st.checkbox("Include Dishwasher Space (0.6m)", key="dishwasher")
            cabinet_width = st.number_input("Wall Cabinet Width (m)", min_value=0.0, max_value=10.0, value=0.0, step=0.1, key="cabinet")
            stove_width = st.number_input("Stove Width (m)", min_value=0.0, max_value=5.0, value=0.0, step=0.1, key="stove")
            has_oven = st.checkbox("Include Oven Below Stove", key="oven")
        else:
            fridge_width = dishwasher = cabinet_width = stove_width = has_oven = 0
    
    st.markdown("---")
    
    col_back, col_calc = st.columns([1, 2])
    with col_back:
        if st.button("← Back", key="back_measurements"):
            st.session_state.step = 2
            st.rerun()
    
    with col_calc:
        if st.button("✨ Calculate Price", key="calculate", use_container_width=True):
            # Calculate areas
            base_area = height * length
            deductions = 0
            additions = 0
            
            if st.session_state.product_type == "Kitchen":
                # Deductions
                deductions += fridge_width * height if fridge_width > 0 else 0
                deductions += 0.6 * height if dishwasher else 0
                deductions += stove_width * height if stove_width > 0 else 0
                
                # Additions
                additions += cabinet_width * 0.35  # Wall cabinets
                if has_oven and stove_width > 0:
                    additions += stove_width * 0.7  # Oven space
            
            final_area = base_area + additions - deductions
            total_price = final_area * MATERIAL_PRICES[st.session_state.selected_material]
            
            # Store calculation details
            st.session_state.calc_details = {
                "base_area": base_area,
                "additions": additions,
                "deductions": deductions,
                "final_area": final_area,
                "total_price": total_price
            }
            
            # Show results
            show_calculation_results()

def show_calculation_results():
    details = st.session_state.calc_details
    
    st.success("✅ Calculation Complete!")
    
    # Breakdown display
    st.markdown("### 📊 Price Breakdown")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Create breakdown table
        breakdown_data = {
            "Description": [
                "Base Area (H × L)",
                "Additional Features",
                "Deductions (Appliances)",
                "Final Area",
                "Material Rate",
                "Total Price"
            ],
            "Value": [
                f"{details['base_area']:.2f} m²",
                f"{details['additions']:.2f} m²",
                f"-{details['deductions']:.2f} m²",
                f"{details['final_area']:.2f} m²",
                f"${MATERIAL_PRICES[st.session_state.selected_material]}/m²",
                ""
            ]
        }
        
        for desc, val in zip(breakdown_data["Description"][:-1], breakdown_data["Value"][:-1]):
            st.markdown(f"**{desc}:** {val}")
    
    with col2:
        st.markdown(f"""
        <div style='text-align: center; padding: 30px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 15px;'>
            <div style='color: white; font-size: 16px; margin-bottom: 10px;'>Total Price</div>
            <div style='color: white; font-size: 36px; font-weight: 700;'>${details['total_price']:.2f}</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🔄 Start Over", use_container_width=True):
            reset_calculator()
            st.rerun()
    
    with col2:
        if st.button("🛒 Add to Cart", key="add_to_cart", use_container_width=True):
            item = {
                "Product": st.session_state.product_type,
                "Material": st.session_state.selected_material,
                "Area": f"{details['final_area']:.2f} m²",
                "Price": details['total_price']
            }
            st.session_state.cart.append(item)
            st.success("Added to cart!")
            reset_calculator()
            st.rerun()
    
    with col3:
        if st.button("💬 Contact Us", use_container_width=True):
            st.info("Switch to 'Contact Us' page to get in touch!")

def show_bed_size_selection():
    st.markdown("### 📏 Select Bed Size")
    
    if os.path.exists("bed_size.png"):
        st.image("bed_size.png", use_container_width=True)
    
    col1, col2, col3 = st.columns(3)
    
    sizes = ["90", "120", "180"]
    size_names = ["Single (90cm)", "Double (120cm)", "King (180cm)"]
    cols = [col1, col2, col3]
    
    for idx, (size, name) in enumerate(zip(sizes, size_names)):
        with cols[idx]:
            st.markdown(f"""
            <div class='custom-card' style='text-align: center;'>
                <div style='font-size: 48px; margin-bottom: 10px;'>🛏️</div>
                <h3>{name}</h3>
                <p style='color: #666; margin-top: 10px;'>Width: {size}cm</p>
            </div>
            """, unsafe_allow_html=True)
            if st.button(f"Select {name}", key=f"btn_size_{size}", use_container_width=True):
                st.session_state.bed_size = size
                st.session_state.step = 3
                st.rerun()
    
    if st.button("← Back", key="back_size"):
        st.session_state.step = 1
        st.rerun()

def show_bed_type_selection():
    st.markdown("### 🎨 Select Bed Type")
    st.markdown(f"**Selected Size:** {st.session_state.bed_size}cm")
    
    if os.path.exists("bed_types.png"):
        st.image("bed_types.png", use_container_width=True)
    
    col1, col2, col3 = st.columns(3)
    
    bed_types = ["Simple", "Rabbet", "MDF"]
    cols = [col1, col2, col3]
    
    for idx, bed_type in enumerate(bed_types):
        with cols[idx]:
            price = BED_PRICES[bed_type][st.session_state.bed_size]
            st.markdown(f"""
            <div class='custom-card' style='text-align: center;'>
                <h3>{bed_type}</h3>
                <div class='price-tag' style='font-size: 20px;'>${price}</div>
                <p style='margin-top: 15px; color: #666;'>{BED_TYPE_INFO[bed_type]}</p>
            </div>
            """, unsafe_allow_html=True)
            if st.button(f"Select {bed_type}", key=f"btn_type_{bed_type}", use_container_width=True):
                st.session_state.bed_type = bed_type
                st.session_state.step = 4
                st.rerun()
    
    if st.button("← Back", key="back_type"):
        st.session_state.step = 2
        st.rerun()

def show_bed_result():
    price = BED_PRICES[st.session_state.bed_type][st.session_state.bed_size]
    
    st.success("✅ Your Bed Configuration is Ready!")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### 🛏️ Selected Configuration")
        st.markdown(f"**Type:** {st.session_state.bed_type}")
        st.markdown(f"**Size:** {st.session_state.bed_size}cm")
        st.markdown(f"**Description:** {BED_TYPE_INFO[st.session_state.bed_type]}")
    
    with col2:
        st.markdown(f"""
        <div style='text-align: center; padding: 30px; background: linear-gradient(135deg, #FFA726 0%, #FF6F00 100%); border-radius: 15px;'>
            <div style='color: white; font-size: 16px; margin-bottom: 10px;'>Fixed Price</div>
            <div style='color: white; font-size: 36px; font-weight: 700;'>${price}</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🔄 Start Over", key="bed_start_over", use_container_width=True):
            reset_calculator()
            st.rerun()
    
    with col2:
        if st.button("🛒 Add to Cart", key="bed_add_cart", use_container_width=True):
            item = {
                "Product": "Bed",
                "Type": st.session_state.bed_type,
                "Size": f"{st.session_state.bed_size}cm",
                "Price": price
            }
            st.session_state.cart.append(item)
            st.success("Added to cart!")
            reset_calculator()
            st.rerun()
    
    with col3:
        if st.button("💬 Contact Us", key="bed_contact", use_container_width=True):
            st.info("Switch to 'Contact Us' page to get in touch!")

def show_cart():
    st.markdown("### 🛒 Shopping Cart")
    
    if not st.session_state.cart:
        st.info("Your cart is empty. Start calculating to add items!")
        return
    
    # Display cart items
    for idx, item in enumerate(st.session_state.cart):
        col1, col2, col3 = st.columns([3, 2, 1])
        
        with col1:
            product_desc = f"**{item['Product']}**"
            if "Material" in item:
                product_desc += f" - {item['Material']}"
            if "Type" in item:
                product_desc += f" - {item['Type']}"
            if "Size" in item:
                product_desc += f" - {item['Size']}"
            if "Area" in item:
                product_desc += f" - {item['Area']}"
            st.markdown(product_desc)
        
        with col2:
            st.markdown(f"**${item['Price']:.2f}**")
        
        with col3:
            if st.button("🗑️", key=f"remove_{idx}"):
                st.session_state.cart.pop(idx)
                st.rerun()
    
    # Total
    total = sum(item["Price"] for item in st.session_state.cart)
    st.markdown("---")
    st.markdown(f"""
    <div style='text-align: right; font-size: 24px; font-weight: 700; color: #1e3c72;'>
        Total: <span style='color: #FFA726;'>${total:.2f}</span>
    </div>
    """, unsafe_allow_html=True)
    
    # Action buttons
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🗑️ Clear Cart", use_container_width=True):
            st.session_state.cart = []
            st.rerun()
    
    with col2:
        if st.button("📄 Generate PDF Quote", key="gen_pdf", use_container_width=True):
            generate_pdf(total)

def generate_pdf(total):
    file_path = "/home/claude/quotation.pdf"
    doc = SimpleDocTemplate(file_path, pagesize=A4, topMargin=0.5*inch, bottomMargin=0.5*inch)
    elements = []
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#1e3c72'),
        spaceAfter=30,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    
    # Title
    elements.append(Paragraph("🏭 Asankar Factory", title_style))
    elements.append(Paragraph("Price Quotation", styles['Heading2']))
    elements.append(Spacer(1, 0.3*inch))
    
    # Cart items table
    data = [["Product", "Details", "Price (USD)"]]
    
    for item in st.session_state.cart:
        product_name = item["Product"]
        details_parts = []
        for k, v in item.items():
            if k not in ["Product", "Price"]:
                details_parts.append(f"{k}: {v}")
        details = ", ".join(details_parts)
        data.append([product_name, details, f"${item['Price']:.2f}"])
    
    data.append(["", "TOTAL", f"${total:.2f}"])
    
    # Table styling
    table = Table(data, colWidths=[2*inch, 3.5*inch, 1.5*inch])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1e3c72')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('ALIGN', (2, 0), (2, -1), 'RIGHT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, -1), (-1, -1), colors.HexColor('#FFA726')),
        ('TEXTCOLOR', (0, -1), (-1, -1), colors.whitesmoke),
        ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, -1), (-1, -1), 14),
        ('GRID', (0, 0), (-1, -1), 1, colors.grey),
        ('ROWBACKGROUNDS', (0, 1), (-1, -2), [colors.white, colors.HexColor('#f5f5f5')])
    ]))
    
    elements.append(table)
    elements.append(Spacer(1, 0.5*inch))
    
    # Footer
    footer_text = "Thank you for choosing Asankar Factory!<br/>Contact: +9647501003839"
    elements.append(Paragraph(footer_text, styles['Normal']))
    
    doc.build(elements)
    
    with open(file_path, "rb") as f:
        st.download_button(
            "📥 Download PDF Quotation",
            f,
            file_name="asankar_quotation.pdf",
            mime="application/pdf",
            use_container_width=True
        )
