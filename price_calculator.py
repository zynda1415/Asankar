import streamlit as st
import pandas as pd

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

def show_price_calculator():
    st.title("🧮 Price Calculator")
    
    if "material" not in st.session_state:
        st.session_state.material = None
    if "product" not in st.session_state:
        st.session_state.product = None
    if "layout" not in st.session_state:
        st.session_state.layout = None
    
    st.subheader("Step 1: Select Material")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.image("images/materials/mdf.png", use_column_width=True)
        if st.button("MDF - $120/m²", use_container_width=True):
            st.session_state.material = "MDF"
            st.rerun()
    
    with col2:
        st.image("images/materials/balloon_press.png", use_column_width=True)
        if st.button("Balloon Press - $160/m²", use_container_width=True):
            st.session_state.material = "Balloon Press"
            st.rerun()
    
    with col3:
        st.image("images/materials/glass.png", use_column_width=True)
        if st.button("Glass - $170/m²", use_container_width=True):
            st.session_state.material = "Glass"
            st.rerun()
    
    if st.session_state.material is None:
        st.info("👆 Please select a material to continue")
        return
    
    st.success(f"✓ Selected: {st.session_state.material} (${MATERIAL_PRICES[st.session_state.material]}/m²)")
    
    st.markdown("---")
    st.subheader("Step 2: Select Product Type")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.image("images/products/kitchen.png", use_column_width=True)
        if st.button("Kitchen", use_container_width=True):
            st.session_state.product = "Kitchen"
            st.session_state.layout = None
            st.rerun()
    
    with col2:
        st.image("images/products/wardrobe.png", use_column_width=True)
        if st.button("Wardrobe", use_container_width=True):
            st.session_state.product = "Wardrobe"
            st.session_state.layout = None
            st.rerun()
    
    if st.session_state.product is None:
        st.info("👆 Please select a product type to continue")
        return
    
    st.success(f"✓ Selected: {st.session_state.product}")
    
    st.markdown("---")
    
    if st.session_state.product == "Kitchen":
        show_kitchen_calculator()
    elif st.session_state.product == "Wardrobe":
        show_wardrobe_calculator()


def show_kitchen_calculator():
    st.subheader("Step 3: Select Kitchen Layout")
    
    col1, col2 = st.columns(2)
    col3, col4 = st.columns(2)
    
    with col1:
        st.image("images/layouts/one_wall.png", use_column_width=True)
        if st.button("One-Wall", use_container_width=True):
            st.session_state.layout = "One-Wall"
            st.rerun()
    
    with col2:
        st.image("images/layouts/l_shaped.png", use_column_width=True)
        if st.button("L-Shaped", use_container_width=True):
            st.session_state.layout = "L-Shaped"
            st.rerun()
    
    with col3:
        st.image("images/layouts/u_shaped.png", use_column_width=True)
        if st.button("U-Shaped", use_container_width=True):
            st.session_state.layout = "U-Shaped"
            st.rerun()
    
    with col4:
        st.image("images/layouts/galley.png", use_column_width=True)
        if st.button("Galley (Parallel)", use_container_width=True):
            st.session_state.layout = "Galley"
            st.rerun()
    
    if st.session_state.layout is None:
        st.info("👆 Please select a kitchen layout to continue")
        return
    
    st.success(f"✓ Selected Layout: {st.session_state.layout}")
    
    st.markdown("---")
    st.subheader("Step 4: Enter Dimensions & Appliances")
    
    if st.session_state.layout == "One-Wall":
        calculate_one_wall()
    elif st.session_state.layout == "L-Shaped":
        calculate_l_shaped()
    elif st.session_state.layout == "U-Shaped":
        calculate_u_shaped()
    elif st.session_state.layout == "Galley":
        calculate_galley()


def calculate_one_wall():
    st.write("**Wall Dimensions**")
    col1, col2 = st.columns(2)
    with col1:
        height = st.number_input("Height (m)", min_value=0.0, value=2.4, step=0.1, key="h1")
    with col2:
        length = st.number_input("Length (m)", min_value=0.0, value=3.0, step=0.1, key="l1")
    
    st.write("**Appliances & Components**")
    
    has_fridge = st.checkbox("Refrigerator", key="fridge1")
    fridge_width = 0.0
    if has_fridge:
        fridge_width = st.number_input("Refrigerator width (m)", min_value=0.0, value=0.8, step=0.1, key="fw1")
    
    has_dishwasher = st.checkbox("Dishwasher", key="dish1")
    
    has_cabinet = st.checkbox("Cabinet", key="cab1")
    cabinet_width = 0.0
    if has_cabinet:
        cabinet_width = st.number_input("Cabinet width (m)", min_value=0.0, value=0.6, step=0.1, key="cw1")
    
    has_stove = st.checkbox("Stove", key="stove1")
    stove_width = 0.0
    has_oven = False
    if has_stove:
        stove_width = st.number_input("Stove width (m)", min_value=0.0, value=0.6, step=0.1, key="sw1")
        has_oven = st.checkbox("With oven underneath", key="oven1")
    
    has_vitrine = st.checkbox("Vitrine (glass cabinet)", key="vit1")
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
    st.write("**Wall Dimensions**")
    col1, col2 = st.columns(2)
    with col1:
        height = st.number_input("Height (m)", min_value=0.0, value=2.4, step=0.1, key="h2")
    with col2:
        st.write("")
    
    col1, col2 = st.columns(2)
    with col1:
        length1 = st.number_input("Wall 1 Length (m)", min_value=0.0, value=3.0, step=0.1, key="l2a")
    with col2:
        length2 = st.number_input("Wall 2 Length (m)", min_value=0.0, value=2.5, step=0.1, key="l2b")
    
    st.write("**Appliances & Components**")
    
    has_fridge = st.checkbox("Refrigerator", key="fridge2")
    fridge_width = 0.0
    if has_fridge:
        fridge_width = st.number_input("Refrigerator width (m)", min_value=0.0, value=0.8, step=0.1, key="fw2")
    
    has_dishwasher = st.checkbox("Dishwasher", key="dish2")
    
    has_cabinet = st.checkbox("Cabinet", key="cab2")
    cabinet_width = 0.0
    if has_cabinet:
        cabinet_width = st.number_input("Cabinet width (m)", min_value=0.0, value=0.6, step=0.1, key="cw2")
    
    has_stove = st.checkbox("Stove", key="stove2")
    stove_width = 0.0
    has_oven = False
    if has_stove:
        stove_width = st.number_input("Stove width (m)", min_value=0.0, value=0.6, step=0.1, key="sw2")
        has_oven = st.checkbox("With oven underneath", key="oven2")
    
    has_vitrine = st.checkbox("Vitrine (glass cabinet)", key="vit2")
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
    st.write("**Wall Dimensions**")
    col1, col2 = st.columns(2)
    with col1:
        height = st.number_input("Height (m)", min_value=0.0, value=2.4, step=0.1, key="h3")
    with col2:
        st.write("")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        length1 = st.number_input("Wall 1 Length (m)", min_value=0.0, value=3.0, step=0.1, key="l3a")
    with col2:
        length2 = st.number_input("Wall 2 Length (m)", min_value=0.0, value=2.0, step=0.1, key="l3b")
    with col3:
        length3 = st.number_input("Wall 3 Length (m)", min_value=0.0, value=3.0, step=0.1, key="l3c")
    
    st.write("**Appliances & Components**")
    
    has_fridge = st.checkbox("Refrigerator", key="fridge3")
    fridge_width = 0.0
    if has_fridge:
        fridge_width = st.number_input("Refrigerator width (m)", min_value=0.0, value=0.8, step=0.1, key="fw3")
    
    has_dishwasher = st.checkbox("Dishwasher", key="dish3")
    
    has_cabinet = st.checkbox("Cabinet", key="cab3")
    cabinet_width = 0.0
    if has_cabinet:
        cabinet_width = st.number_input("Cabinet width (m)", min_value=0.0, value=0.6, step=0.1, key="cw3")
    
    has_stove = st.checkbox("Stove", key="stove3")
    stove_width = 0.0
    has_oven = False
    if has_stove:
        stove_width = st.number_input("Stove width (m)", min_value=0.0, value=0.6, step=0.1, key="sw3")
        has_oven = st.checkbox("With oven underneath", key="oven3")
    
    has_vitrine = st.checkbox("Vitrine (glass cabinet)", key="vit3")
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
    st.write("**Wall Dimensions**")
    col1, col2 = st.columns(2)
    with col1:
        height = st.number_input("Height (m)", min_value=0.0, value=2.4, step=0.1, key="h4")
    with col2:
        st.write("")
    
    col1, col2 = st.columns(2)
    with col1:
        length1 = st.number_input("Wall 1 Length (m)", min_value=0.0, value=3.0, step=0.1, key="l4a")
    with col2:
        length2 = st.number_input("Wall 2 Length (m)", min_value=0.0, value=3.0, step=0.1, key="l4b")
    
    st.write("**Appliances & Components**")
    
    has_fridge = st.checkbox("Refrigerator", key="fridge4")
    fridge_width = 0.0
    if has_fridge:
        fridge_width = st.number_input("Refrigerator width (m)", min_value=0.0, value=0.8, step=0.1, key="fw4")
    
    has_dishwasher = st.checkbox("Dishwasher", key="dish4")
    
    has_cabinet = st.checkbox("Cabinet", key="cab4")
    cabinet_width = 0.0
    if has_cabinet:
        cabinet_width = st.number_input("Cabinet width (m)", min_value=0.0, value=0.6, step=0.1, key="cw4")
    
    has_stove = st.checkbox("Stove", key="stove4")
    stove_width = 0.0
    has_oven = False
    if has_stove:
        stove_width = st.number_input("Stove width (m)", min_value=0.0, value=0.6, step=0.1, key="sw4")
        has_oven = st.checkbox("With oven underneath", key="oven4")
    
    has_vitrine = st.checkbox("Vitrine (glass cabinet)", key="vit4")
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
    st.subheader("Step 3: Wardrobe Configuration")
    
    st.write("**Basic Dimensions**")
    col1, col2 = st.columns(2)
    with col1:
        height = st.number_input("Height (m)", min_value=0.0, value=2.4, step=0.1, key="wh")
    with col2:
        width = st.number_input("Width (m)", min_value=0.0, value=2.0, step=0.1, key="ww")
    
    st.write("**Additional Features**")
    
    has_shelves = st.checkbox("Add shelves", key="shelves")
    num_shelves = 0
    if has_shelves:
        num_shelves = st.number_input("Number of shelves", min_value=0, max_value=20, value=5, step=1, key="ns")
    
    door_type = st.radio("Door type", ["Hinged", "Sliding"], key="door")
    
    has_mirror = st.checkbox("Mirror/Glass panels", key="mirror")
    glass_area = 0.0
    if has_mirror:
        glass_height = st.number_input("Glass panel height (m)", min_value=0.0, value=2.0, step=0.1, key="gh")
        glass_width = st.number_input("Glass panel width (m)", min_value=0.0, value=1.0, step=0.1, key="gw")
        glass_area = glass_height * glass_width
    
    if height > 0 and width > 0:
        base_area = height * width
        shelf_area = width * CABINET_DEPTH * num_shelves if has_shelves else 0
        
        total_area = (base_area + shelf_area + glass_area) * WASTE_FACTOR
        
        material_price = total_area * MATERIAL_PRICES[st.session_state.material]
        
        glass_cost = glass_area * 50 if has_mirror else 0
        sliding_cost = 200 if door_type == "Sliding" else 0
        
        total_price = material_price + glass_cost + sliding_cost
        
        breakdown = {
            "Base Wardrobe Area": base_area,
            "Shelves Area": shelf_area,
            "Glass Panel Area": glass_area,
            "Subtotal": base_area + shelf_area + glass_area,
            "Waste Factor (10%)": total_area - (base_area + shelf_area + glass_area),
            "Total Material Area": total_area
        }
        
        display_breakdown(breakdown, material_price, glass_cost=glass_cost, sliding_cost=sliding_cost, total_price=total_price)


def display_breakdown(breakdown, material_price, glass_cost=0, sliding_cost=0, total_price=None):
    st.markdown("---")
    st.subheader("📊 Price Breakdown")
    
    df_data = []
    for item, value in breakdown.items():
        if value != 0:
            df_data.append({"Item": item, "Value": f"{value:.2f} m²"})
    
    df = pd.DataFrame(df_data)
    st.table(df)
    
    st.markdown("---")
    st.write(f"**Material:** {st.session_state.material} @ ${MATERIAL_PRICES[st.session_state.material]}/m²")
    st.write(f"**Material Cost:** ${material_price:.2f}")
    
    if glass_cost > 0:
        st.write(f"**Glass Cost:** ${glass_cost:.2f}")
    if sliding_cost > 0:
        st.write(f"**Sliding System Cost:** ${sliding_cost:.2f}")
    
    final_price = total_price if total_price is not None else material_price
    
    st.markdown("---")
    st.markdown(f"### 💰 **TOTAL PRICE: ${final_price:,.2f}**")
    
    st.markdown("---")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔄 Start New Calculation", use_container_width=True):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()
    with col2:
        st.download_button(
            label="📄 Download Quote (PDF)",
            data=f"PRICE QUOTATION\n\nMaterial: {st.session_state.material}\nProduct: {st.session_state.product}\n\nTotal Price: ${final_price:,.2f}",
            file_name="quote.txt",
            mime="text/plain",
            use_container_width=True
        )
