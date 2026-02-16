import streamlit as st
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4

MATERIAL_PRICES = {"MDF": 120, "Balloon Press": 160, "Glass": 170}
BED_PRICES = {
    "Simple": {"90": 310, "120": 350, "180": 420},
    "Rabbet": {"90": 500, "120": 590, "180": 750},
    "MDF": {"90": 200, "120": 230, "180": 300}
}

if "cart" not in st.session_state:
    st.session_state.cart = []
if "step" not in st.session_state:
    st.session_state.step = 1
if "product_type" not in st.session_state:
    st.session_state.product_type = None

def show_price_calculator():
    st.title("💰 Price Calculator")
    
    if st.session_state.step > 1:
        progress = st.session_state.step / 3
        st.progress(progress)
    
    st.markdown("---")
    
    if st.session_state.step == 1:
        show_product_selection()
    elif st.session_state.step == 2:
        if st.session_state.product_type in ["Kitchen", "Wardrobe"]:
            show_material_selection()
        else:
            show_bed_size_selection()
    elif st.session_state.step == 3:
        if st.session_state.product_type in ["Kitchen", "Wardrobe"]:
            show_measurements()
        else:
            show_bed_type_selection()
    
    st.markdown("---")
    show_cart()

def show_product_selection():
    st.subheader("Select Product Type")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("### 🍳 Kitchen")
        if st.button("Select Kitchen", key="btn_kitchen", use_container_width=True):
            st.session_state.product_type = "Kitchen"
            st.session_state.step = 2
            st.rerun()
    
    with col2:
        st.markdown("### 👔 Wardrobe")
        if st.button("Select Wardrobe", key="btn_wardrobe", use_container_width=True):
            st.session_state.product_type = "Wardrobe"
            st.session_state.step = 2
            st.rerun()
    
    with col3:
        st.markdown("### 🛏️ Bed")
        if st.button("Select Bed", key="btn_bed", use_container_width=True):
            st.session_state.product_type = "Bed"
            st.session_state.step = 2
            st.rerun()

def show_material_selection():
    st.subheader(f"Choose Material - {st.session_state.product_type}")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"### MDF")
        st.markdown(f"**${MATERIAL_PRICES['MDF']}/m²**")
        if st.button("Select MDF", key="btn_mdf", use_container_width=True):
            st.session_state.selected_material = "MDF"
            st.session_state.step = 3
            st.rerun()
    
    with col2:
        st.markdown(f"### Balloon Press")
        st.markdown(f"**${MATERIAL_PRICES['Balloon Press']}/m²**")
        if st.button("Select Balloon Press", key="btn_bp", use_container_width=True):
            st.session_state.selected_material = "Balloon Press"
            st.session_state.step = 3
            st.rerun()
    
    with col3:
        st.markdown(f"### Glass")
        st.markdown(f"**${MATERIAL_PRICES['Glass']}/m²**")
        if st.button("Select Glass", key="btn_glass", use_container_width=True):
            st.session_state.selected_material = "Glass"
            st.session_state.step = 3
            st.rerun()
    
    if st.button("← Back", key="back_mat"):
        st.session_state.step = 1
        st.rerun()

def show_measurements():
    st.subheader(f"Enter Dimensions - {st.session_state.product_type}")
    st.write(f"Material: {st.session_state.selected_material} (${MATERIAL_PRICES[st.session_state.selected_material]}/m²)")
    
    col1, col2 = st.columns(2)
    
    with col1:
        height = st.number_input("Height (m)", 0.0, 10.0, 2.5, 0.1)
        length = st.number_input("Length (m)", 0.0, 20.0, 3.0, 0.1)
    
    with col2:
        if st.session_state.product_type == "Kitchen":
            fridge_width = st.number_input("Fridge Width (m)", 0.0, 5.0, 0.0, 0.1)
            dishwasher = st.checkbox("Dishwasher Space (0.6m)")
            cabinet_width = st.number_input("Cabinet Width (m)", 0.0, 10.0, 0.0, 0.1)
            stove_width = st.number_input("Stove Width (m)", 0.0, 5.0, 0.0, 0.1)
            has_oven = st.checkbox("Oven Below Stove")
        else:
            fridge_width = dishwasher = cabinet_width = stove_width = has_oven = 0
    
    col_back, col_calc = st.columns([1, 2])
    
    with col_back:
        if st.button("← Back", key="back_meas"):
            st.session_state.step = 2
            st.rerun()
    
    with col_calc:
        if st.button("Calculate", key="calc", use_container_width=True):
            base_area = height * length
            deductions = 0
            additions = 0
            
            if st.session_state.product_type == "Kitchen":
                deductions += fridge_width * height if fridge_width > 0 else 0
                deductions += 0.6 * height if dishwasher else 0
                deductions += stove_width * height if stove_width > 0 else 0
                additions += cabinet_width * 0.35
                if has_oven and stove_width > 0:
                    additions += stove_width * 0.7
            
            final_area = base_area + additions - deductions
            total_price = final_area * MATERIAL_PRICES[st.session_state.selected_material]
            
            st.success("✅ Calculation Complete")
            st.write(f"Base Area: {base_area:.2f} m²")
            st.write(f"Additions: {additions:.2f} m²")
            st.write(f"Deductions: {deductions:.2f} m²")
            st.write(f"Final Area: {final_area:.2f} m²")
            st.markdown(f"### Total: ${total_price:.2f}")
            
            if st.button("Add to Cart", key="add_cart"):
                st.session_state.cart.append({
                    "Product": st.session_state.product_type,
                    "Material": st.session_state.selected_material,
                    "Area": f"{final_area:.2f} m²",
                    "Price": total_price
                })
                st.session_state.step = 1
                st.rerun()

def show_bed_size_selection():
    st.subheader("Select Bed Size")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("### Single (90cm)")
        if st.button("Select 90cm", key="btn_90", use_container_width=True):
            st.session_state.bed_size = "90"
            st.session_state.step = 3
            st.rerun()
    
    with col2:
        st.markdown("### Double (120cm)")
        if st.button("Select 120cm", key="btn_120", use_container_width=True):
            st.session_state.bed_size = "120"
            st.session_state.step = 3
            st.rerun()
    
    with col3:
        st.markdown("### King (180cm)")
        if st.button("Select 180cm", key="btn_180", use_container_width=True):
            st.session_state.bed_size = "180"
            st.session_state.step = 3
            st.rerun()
    
    if st.button("← Back", key="back_size"):
        st.session_state.step = 1
        st.rerun()

def show_bed_type_selection():
    st.subheader(f"Select Bed Type - {st.session_state.bed_size}cm")
    
    col1, col2, col3 = st.columns(3)
    
    types = ["Simple", "Rabbet", "MDF"]
    cols = [col1, col2, col3]
    
    for idx, bed_type in enumerate(types):
        with cols[idx]:
            price = BED_PRICES[bed_type][st.session_state.bed_size]
            st.markdown(f"### {bed_type}")
            st.markdown(f"**${price}**")
            if st.button(f"Select {bed_type}", key=f"btn_{bed_type}", use_container_width=True):
                st.session_state.cart.append({
                    "Product": "Bed",
                    "Type": bed_type,
                    "Size": f"{st.session_state.bed_size}cm",
                    "Price": price
                })
                st.session_state.step = 1
                st.success(f"Added {bed_type} Bed (${price})")
                st.rerun()
    
    if st.button("← Back", key="back_type"):
        st.session_state.step = 2
        st.rerun()

def show_cart():
    st.subheader("🛒 Cart")
    
    if not st.session_state.cart:
        st.info("Cart is empty")
        return
    
    for idx, item in enumerate(st.session_state.cart):
        col1, col2 = st.columns([4, 1])
        with col1:
            details = " - ".join([f"{k}: {v}" for k, v in item.items() if k != "Price"])
            st.write(f"{details} - **${item['Price']:.2f}**")
        with col2:
            if st.button("🗑️", key=f"del_{idx}"):
                st.session_state.cart.pop(idx)
                st.rerun()
    
    total = sum(item["Price"] for item in st.session_state.cart)
    st.markdown(f"### Total: ${total:.2f}")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Clear Cart", use_container_width=True):
            st.session_state.cart = []
            st.rerun()
    with col2:
        if st.button("Generate PDF", use_container_width=True):
            generate_pdf(total)

def generate_pdf(total):
    file_path = "/mnt/user-data/outputs/quotation.pdf"
    doc = SimpleDocTemplate(file_path, pagesize=A4)
    elements = []
    
    data = [["Product", "Details", "Price"]]
    for item in st.session_state.cart:
        details = " - ".join([str(v) for k, v in item.items() if k not in ["Product", "Price"]])
        data.append([item["Product"], details, f"${item['Price']:.2f}"])
    data.append(["", "TOTAL", f"${total:.2f}"])
    
    table = Table(data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    
    elements.append(table)
    doc.build(elements)
    
    with open(file_path, "rb") as f:
        st.download_button("Download PDF", f, file_name="quotation.pdf", use_container_width=True)
