import streamlit as st
import pandas as pd
from datetime import datetime

# Config
MATERIAL_PRICES = {"MDF": 120, "Balloon Press": 160, "Glass": 170}
WASTE_FACTOR, DISHWASHER_AREA, FRIDGE_DEPTH, CABINET_DEPTH, OVEN_HEIGHT, VITRINE_BASE_HEIGHT = 1.10, 0.51, 0.6, 0.6, 0.85, 0.6

# Translations
T = {
    "en": {"company": "Asankar Company", "calc": "Price Calculator", "sub": "Configure your dream kitchen or wardrobe", "s1": "Step 1: Select Material", "s2": "Step 2: Select Product", "s3k": "Step 3: Kitchen Layout", "s3w": "Step 3: Wardrobe Config", "s4": "Step 4: Dimensions & Appliances", "kitchen": "Kitchen", "wardrobe": "Wardrobe", "1wall": "One-Wall", "lshape": "L-Shaped", "ushape": "U-Shaped", "galley": "Galley", "dims": "Wall Dimensions", "h": "Height (m)", "l": "Length (m)", "w": "Width (m)", "app": "Appliances", "fridge": "🧊 Refrigerator", "dish": "🍽️ Dishwasher", "cab": "🗄️ Cabinet", "stove": "🔥 Stove", "oven": "With oven", "vit": "🪟 Vitrine", "shelf": "📚 Shelves", "nshelf": "Number of shelves", "door": "🚪 Door type", "hinge": "Hinged", "slide": "Sliding", "mirror": "🪞 Mirror/Glass", "gh": "Glass height (m)", "gw": "Glass width (m)", "break": "Price Breakdown", "comp": "Component", "area": "Area (m²)", "mat": "Material", "perm2": "Price/m²", "matcost": "Material Cost", "glasscost": "Glass Cost", "slidecost": "Sliding System", "total": "TOTAL PRICE", "new": "🔄 New Calc", "down": "📄 Download", "share": "💬 WhatsApp", "sel": "Please select to continue", "basic": "Basic Dimensions", "feat": "Additional Features"},
    "ku": {"company": "کۆمپانیای ئاسانکار", "calc": "حیسابکەری نرخ", "sub": "چێشتخانە یان جلخانە ڕێکبخە", "s1": "هەنگاو ١: ماددە هەڵبژێرە", "s2": "هەنگاو ٢: بەرهەم هەڵبژێرە", "s3k": "هەنگاو ٣: شێوەی چێشتخانە", "s3w": "هەنگاو ٣: ڕێکخستنی جلخانە", "s4": "هەنگاو ٤: پێوانە و ئامێر", "kitchen": "چێشتخانە", "wardrobe": "جلخانە", "1wall": "یەک-دیوار", "lshape": "L شێوەی", "ushape": "U شێوەی", "galley": "هاوتەریب", "dims": "پێوانەی دیوار", "h": "بەرزی (م)", "l": "درێژی (م)", "w": "پانی (م)", "app": "ئامێرەکان", "fridge": "🧊 سارکەرەوە", "dish": "🍽️ قاپشۆر", "cab": "🗄️ کابینێت", "stove": "🔥 هێڵان", "oven": "لەگەڵ تەنوور", "vit": "🪟 ڤیترین", "shelf": "📚 تەختە", "nshelf": "ژمارەی تەختە", "door": "🚪 دەرگا", "hinge": "پاشۆڵە", "slide": "خلیسکان", "mirror": "🪞 ئاوێنە", "gh": "بەرزی شووشە (م)", "gw": "پانی شووشە (م)", "break": "وردەکاری نرخ", "comp": "پێکهاتە", "area": "ڕووبەر (م²)", "mat": "ماددە", "perm2": "نرخ/م²", "matcost": "تێچووی ماددە", "glasscost": "تێچووی شووشە", "slidecost": "سیستەمی خلیسکان", "total": "کۆی گشتی", "new": "🔄 نوێ", "down": "📄 داگرتن", "share": "💬 واتساپ", "sel": "تکایە هەڵبژێرە", "basic": "پێوانە بنەڕەتی", "feat": "تایبەتمەندی زیادە"},
    "ar": {"company": "شركة أسانكار", "calc": "حاسبة الأسعار", "sub": "قم بتكوين مطبخ أو خزانة", "s1": "الخطوة ١: اختر المادة", "s2": "الخطوة ٢: اختر المنتج", "s3k": "الخطوة ٣: تصميم المطبخ", "s3w": "الخطوة ٣: تكوين الخزانة", "s4": "الخطوة ٤: الأبعاد والأجهزة", "kitchen": "مطبخ", "wardrobe": "خزانة", "1wall": "جدار واحد", "lshape": "شكل L", "ushape": "شكل U", "galley": "متوازي", "dims": "أبعاد الجدار", "h": "الارتفاع (م)", "l": "الطول (م)", "w": "العرض (م)", "app": "الأجهزة", "fridge": "🧊 ثلاجة", "dish": "🍽️ غسالة صحون", "cab": "🗄️ خزانة", "stove": "🔥 موقد", "oven": "مع فرن", "vit": "🪟 فاترينا", "shelf": "📚 رفوف", "nshelf": "عدد الرفوف", "door": "🚪 الباب", "hinge": "مفصلي", "slide": "منزلق", "mirror": "🪞 مرآة", "gh": "ارتفاع الزجاج (م)", "gw": "عرض الزجاج (م)", "break": "تفاصيل السعر", "comp": "المكون", "area": "المساحة (م²)", "mat": "المادة", "perm2": "السعر/م²", "matcost": "تكلفة المواد", "glasscost": "تكلفة الزجاج", "slidecost": "نظام الانزلاق", "total": "السعر الإجمالي", "new": "🔄 جديد", "down": "📄 تحميل", "share": "💬 واتساب", "sel": "الرجاء الاختيار", "basic": "الأبعاد الأساسية", "feat": "ميزات إضافية"}
}
def t(k, l="en"): return T.get(l, T["en"]).get(k, k)

def css():
    st.markdown("""<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&display=swap');
    * {font-family: 'Inter', sans-serif;}
    .stButton>button {border-radius: 12px; font-weight: 500; transition: all 0.2s; border: 1px solid #e5e7eb; background: white; color: #1f2937; padding: 0.75rem 1rem; box-shadow: 0 1px 2px rgba(0,0,0,0.05);}
    .stButton>button:hover {transform: translateY(-1px); box-shadow: 0 4px 6px rgba(0,0,0,0.1); border-color: #10b981; background: #f9fafb;}
    @keyframes fadeIn {from {opacity: 0; transform: scale(0.98);} to {opacity: 1; transform: scale(1);}}
    .stImage {animation: fadeIn 0.3s; border-radius: 8px; transition: transform 0.2s;}
    .stImage:hover {transform: scale(1.02);}
    .success-badge {background: #10b981; color: white; padding: 8px 16px; border-radius: 8px; font-weight: 500; font-size: 14px; display: inline-block; margin: 8px 0;}
    .price-display {background: linear-gradient(135deg, #1f2937 0%, #374151 100%); color: white; padding: 24px; border-radius: 12px; text-align: center; font-size: 32px; font-weight: 600; margin: 24px 0;}
    .step-header {background: #f9fafb; color: #1f2937; padding: 12px 20px; border-radius: 8px; border-left: 4px solid #10b981; margin: 20px 0 16px 0; font-size: 16px; font-weight: 600;}
    .breakdown-table {background: white; border-radius: 8px; padding: 16px; border: 1px solid #e5e7eb;}
    #MainMenu, footer {visibility: hidden;}
    </style>""", unsafe_allow_html=True)

def quote_txt(bd, cd, mat, prod, lay=None):
    d, n = datetime.now().strftime("%B %d, %Y"), datetime.now().strftime("%Y%m%d%H%M%S")
    txt = f"""╔═══════════════════════════════════════════╗
║    کۆمپانیای ئاسانکار - ASANKAR COMPANY   ║
║         PRICE QUOTATION - پسوڵەی نرخ        ║
╚═══════════════════════════════════════════╝

Quote: {n} | Date: {d}
Material/ماددە: {mat} | Product/بەرهەم: {prod}"""
    if lay: txt += f"\nLayout/شێواز: {lay}"
    txt += "\n\n" + "="*50 + "\nDETAILS / وردەکاری\n" + "="*50 + "\n"
    for k, v in cd.items():
        if k not in ['glass_cost', 'sliding_cost', 'total_price']:
            if isinstance(v, float): txt += f"{k}: {v:.2f}m\n"
            elif isinstance(v, bool): txt += f"{k}: {'Yes/بەڵێ' if v else 'No/نەخێر'}\n"
            else: txt += f"{k}: {v}\n"
    txt += "\n" + "="*50 + "\nAREA / ڕووبەر\n" + "="*50 + "\n"
    for i, v in bd.items():
        if v != 0: txt += f"{i:.<35} {abs(v):>10.2f} m²\n"
    ta, mr, mc = bd.get('Total Area', 0), MATERIAL_PRICES[mat], bd.get('Total Area', 0) * MATERIAL_PRICES[mat]
    txt += "\n" + "="*50 + "\nPRICE / نرخ\n" + "="*50 + f"\n{mat} @ ${mr}/m²\nArea/ڕووبەر: {ta:.2f}m² | Cost/تێچوو: ${mc:,.2f}\n"
    if cd.get('glass_cost', 0) > 0: txt += f"Glass/شووشە: ${cd['glass_cost']:,.2f}\n"
    if cd.get('sliding_cost', 0) > 0: txt += f"Sliding/خلیسکان: ${cd['sliding_cost']:,.2f}\n"
    tp = cd.get('total_price', mc)
    txt += f"\nTOTAL/کۆی گشتی: ${tp:,.2f}\n" + "="*50 + "\n\nTERMS: Valid 30 days | 50% deposit | 2-4 weeks install | 2yr warranty\nContact: info@asankar.com"
    return txt

def breakdown(bd, mp, gc=0, sc=0, tp=None, l="en"):
    st.markdown("---")
    st.markdown(f"<div class='step-header'>📊 {t('break', l)}</div>", unsafe_allow_html=True)
    df = pd.DataFrame([{"comp": i, "area": f"{v:.2f}"} for i, v in bd.items() if v != 0])
    df.columns = [t('comp', l), t('area', l)]
    st.markdown("<div class='breakdown-table'>", unsafe_allow_html=True)
    st.dataframe(df, use_container_width=True, hide_index=True)
    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("---")
    c1, c2 = st.columns(2)
    with c1:
        st.metric(t('mat', l), st.session_state.material)
        st.metric(t('perm2', l), f"${MATERIAL_PRICES[st.session_state.material]}")
    with c2:
        st.metric(t('matcost', l), f"${mp:.2f}")
        if gc > 0: st.metric(t('glasscost', l), f"${gc:.2f}")
        if sc > 0: st.metric(t('slidecost', l), f"${sc:.2f}")
    fp = tp if tp else mp
    st.markdown(f"<div class='price-display'>💰 {t('total', l)}: ${fp:,.2f}</div>", unsafe_allow_html=True)
    st.markdown("---")
    c1, c2, c3 = st.columns(3)
    with c1:
        if st.button(t('new', l), use_container_width=True):
            for k in list(st.session_state.keys()): del st.session_state[k]
            st.rerun()
    with c2:
        qt = quote_txt(bd, st.session_state.calculation_details, st.session_state.material, st.session_state.product, st.session_state.layout if st.session_state.product == "Kitchen" else None)
        st.download_button(t('down', l), qt, f"quote_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt", "text/plain", use_container_width=True)
    with c3:
        wa = f"Hi! Quote: {st.session_state.product} {st.session_state.material} - ${fp:,.2f}"
        st.markdown(f"[{t('share', l)}](https://wa.me/?text={wa.replace(' ', '%20')})", unsafe_allow_html=True)

def calc1w(l):
    st.markdown(f"**{t('dims', l)}**")
    c1, c2 = st.columns(2)
    with c1: h = st.number_input(t('h', l), 0.0, value=2.4, step=0.1, key="h1")
    with c2: le = st.number_input(t('l', l), 0.0, value=3.0, step=0.1, key="l1")
    st.markdown(f"**{t('app', l)}**")
    c1, c2 = st.columns(2)
    with c1:
        fr = st.checkbox(t('fridge', l), key="fr1")
        fw = st.number_input(t('w', l), 0.0, value=0.8, step=0.1, key="fw1") if fr else 0
    with c2: di = st.checkbox(t('dish', l), key="di1")
    c1, c2 = st.columns(2)
    with c1:
        ca = st.checkbox(t('cab', l), key="ca1")
        cw = st.number_input(t('w', l), 0.0, value=0.6, step=0.1, key="cw1") if ca else 0
    with c2:
        st_ = st.checkbox(t('stove', l), key="st1")
        sw, ov = (st.number_input(t('w', l), 0.0, value=0.6, step=0.1, key="sw1"), st.checkbox(t('oven', l), key="ov1")) if st_ else (0, False)
    vi = st.checkbox(t('vit', l), key="vi1")
    vw = st.number_input(t('w', l), 0.0, value=0.6, step=0.1, key="vw1") if vi else 0
    if h > 0 and le > 0:
        ba, fa, caa, da, oa, va = le*h, fw*FRIDGE_DEPTH if fr else 0, cw*CABINET_DEPTH if ca else 0, DISHWASHER_AREA if di else 0, sw*OVEN_HEIGHT if (st_ and ov) else 0, vw*(h-VITRINE_BASE_HEIGHT) if vi else 0
        ta, final = ba+fa+caa-da-oa-va, (ba+fa+caa-da-oa-va)*WASTE_FACTOR
        pr = final * MATERIAL_PRICES[st.session_state.material]
        st.session_state.calculation_details = {"Height": h, "Length": le, "Fridge": fr, "Fridge W": fw, "Dish": di, "Cabinet": ca, "Cab W": cw, "Stove": st_, "Stove W": sw, "Oven": ov, "Vitrine": vi, "Vit W": vw, "total_price": pr}
        breakdown({"Base": ba, "Fridge": fa, "Cabinet": caa, "Dish (-)": -da, "Oven (-)": -oa, "Vitrine (-)": -va, "Subtotal": ta, "Waste 10%": final-ta, "Total Area": final}, pr, l=l)

def calcL(l):
    st.markdown(f"**{t('dims', l)}**")
    c1, c2, c3 = st.columns(3)
    with c1: h = st.number_input(t('h', l), 0.0, value=2.4, step=0.1, key="h2")
    with c2: l1 = st.number_input("Wall 1 (m)", 0.0, value=3.0, step=0.1, key="l2a")
    with c3: l2 = st.number_input("Wall 2 (m)", 0.0, value=2.5, step=0.1, key="l2b")
    st.markdown(f"**{t('app', l)}**")
    c1, c2 = st.columns(2)
    with c1:
        fr = st.checkbox(t('fridge', l), key="fr2")
        fw = st.number_input(t('w', l), 0.0, value=0.8, step=0.1, key="fw2") if fr else 0
    with c2: di = st.checkbox(t('dish', l), key="di2")
    c1, c2 = st.columns(2)
    with c1:
        ca = st.checkbox(t('cab', l), key="ca2")
        cw = st.number_input(t('w', l), 0.0, value=0.6, step=0.1, key="cw2") if ca else 0
    with c2:
        st_ = st.checkbox(t('stove', l), key="st2")
        sw, ov = (st.number_input(t('w', l), 0.0, value=0.6, step=0.1, key="sw2"), st.checkbox(t('oven', l), key="ov2")) if st_ else (0, False)
    vi = st.checkbox(t('vit', l), key="vi2")
    vw = st.number_input(t('w', l), 0.0, value=0.6, step=0.1, key="vw2") if vi else 0
    if h > 0 and l1 > 0 and l2 > 0:
        ba, fa, caa, da, oa, va = (l1+l2)*h, fw*FRIDGE_DEPTH if fr else 0, cw*CABINET_DEPTH if ca else 0, DISHWASHER_AREA if di else 0, sw*OVEN_HEIGHT if (st_ and ov) else 0, vw*(h-VITRINE_BASE_HEIGHT) if vi else 0
        ta, final = ba+fa+caa-da-oa-va, (ba+fa+caa-da-oa-va)*WASTE_FACTOR
        pr = final * MATERIAL_PRICES[st.session_state.material]
        st.session_state.calculation_details = {"Height": h, "Wall1": l1, "Wall2": l2, "Fridge": fr, "Fridge W": fw, "Dish": di, "Cabinet": ca, "Cab W": cw, "Stove": st_, "Stove W": sw, "Oven": ov, "Vitrine": vi, "Vit W": vw, "total_price": pr}
        breakdown({"Base": ba, "Fridge": fa, "Cabinet": caa, "Dish (-)": -da, "Oven (-)": -oa, "Vitrine (-)": -va, "Subtotal": ta, "Waste 10%": final-ta, "Total Area": final}, pr, l=l)

def calcU(l):
    st.markdown(f"**{t('dims', l)}**")
    c1, c2, c3, c4 = st.columns(4)
    with c1: h = st.number_input(t('h', l), 0.0, value=2.4, step=0.1, key="h3")
    with c2: l1 = st.number_input("W1 (m)", 0.0, value=3.0, step=0.1, key="l3a")
    with c3: l2 = st.number_input("W2 (m)", 0.0, value=2.0, step=0.1, key="l3b")
    with c4: l3 = st.number_input("W3 (m)", 0.0, value=3.0, step=0.1, key="l3c")
    st.markdown(f"**{t('app', l)}**")
    c1, c2 = st.columns(2)
    with c1:
        fr = st.checkbox(t('fridge', l), key="fr3")
        fw = st.number_input(t('w', l), 0.0, value=0.8, step=0.1, key="fw3") if fr else 0
    with c2: di = st.checkbox(t('dish', l), key="di3")
    c1, c2 = st.columns(2)
    with c1:
        ca = st.checkbox(t('cab', l), key="ca3")
        cw = st.number_input(t('w', l), 0.0, value=0.6, step=0.1, key="cw3") if ca else 0
    with c2:
        st_ = st.checkbox(t('stove', l), key="st3")
        sw, ov = (st.number_input(t('w', l), 0.0, value=0.6, step=0.1, key="sw3"), st.checkbox(t('oven', l), key="ov3")) if st_ else (0, False)
    vi = st.checkbox(t('vit', l), key="vi3")
    vw = st.number_input(t('w', l), 0.0, value=0.6, step=0.1, key="vw3") if vi else 0
    if h > 0 and l1 > 0 and l2 > 0 and l3 > 0:
        ba, fa, caa, da, oa, va = (l1+l2+l3)*h, fw*FRIDGE_DEPTH if fr else 0, cw*CABINET_DEPTH if ca else 0, DISHWASHER_AREA if di else 0, sw*OVEN_HEIGHT if (st_ and ov) else 0, vw*(h-VITRINE_BASE_HEIGHT) if vi else 0
        ta, final = ba+fa+caa-da-oa-va, (ba+fa+caa-da-oa-va)*WASTE_FACTOR
        pr = final * MATERIAL_PRICES[st.session_state.material]
        st.session_state.calculation_details = {"Height": h, "W1": l1, "W2": l2, "W3": l3, "Fridge": fr, "Fridge W": fw, "Dish": di, "Cabinet": ca, "Cab W": cw, "Stove": st_, "Stove W": sw, "Oven": ov, "Vitrine": vi, "Vit W": vw, "total_price": pr}
        breakdown({"Base": ba, "Fridge": fa, "Cabinet": caa, "Dish (-)": -da, "Oven (-)": -oa, "Vitrine (-)": -va, "Subtotal": ta, "Waste 10%": final-ta, "Total Area": final}, pr, l=l)

def calcG(l):
    st.markdown(f"**{t('dims', l)}**")
    c1, c2, c3 = st.columns(3)
    with c1: h = st.number_input(t('h', l), 0.0, value=2.4, step=0.1, key="h4")
    with c2: l1 = st.number_input("Wall 1 (m)", 0.0, value=3.0, step=0.1, key="l4a")
    with c3: l2 = st.number_input("Wall 2 (m)", 0.0, value=3.0, step=0.1, key="l4b")
    st.markdown(f"**{t('app', l)}**")
    c1, c2 = st.columns(2)
    with c1:
        fr = st.checkbox(t('fridge', l), key="fr4")
        fw = st.number_input(t('w', l), 0.0, value=0.8, step=0.1, key="fw4") if fr else 0
    with c2: di = st.checkbox(t('dish', l), key="di4")
    c1, c2 = st.columns(2)
    with c1:
        ca = st.checkbox(t('cab', l), key="ca4")
        cw = st.number_input(t('w', l), 0.0, value=0.6, step=0.1, key="cw4") if ca else 0
    with c2:
        st_ = st.checkbox(t('stove', l), key="st4")
        sw, ov = (st.number_input(t('w', l), 0.0, value=0.6, step=0.1, key="sw4"), st.checkbox(t('oven', l), key="ov4")) if st_ else (0, False)
    vi = st.checkbox(t('vit', l), key="vi4")
    vw = st.number_input(t('w', l), 0.0, value=0.6, step=0.1, key="vw4") if vi else 0
    if h > 0 and l1 > 0 and l2 > 0:
        ba, fa, caa, da, oa, va = (l1+l2)*h, fw*FRIDGE_DEPTH if fr else 0, cw*CABINET_DEPTH if ca else 0, DISHWASHER_AREA if di else 0, sw*OVEN_HEIGHT if (st_ and ov) else 0, vw*(h-VITRINE_BASE_HEIGHT) if vi else 0
        ta, final = ba+fa+caa-da-oa-va, (ba+fa+caa-da-oa-va)*WASTE_FACTOR
        pr = final * MATERIAL_PRICES[st.session_state.material]
        st.session_state.calculation_details = {"Height": h, "Wall1": l1, "Wall2": l2, "Fridge": fr, "Fridge W": fw, "Dish": di, "Cabinet": ca, "Cab W": cw, "Stove": st_, "Stove W": sw, "Oven": ov, "Vitrine": vi, "Vit W": vw, "total_price": pr}
        breakdown({"Base": ba, "Fridge": fa, "Cabinet": caa, "Dish (-)": -da, "Oven (-)": -oa, "Vitrine (-)": -va, "Subtotal": ta, "Waste 10%": final-ta, "Total Area": final}, pr, l=l)

def kitchen(l):
    st.markdown(f"<div class='step-header'>🔲 {t('s3k', l)}</div>", unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.image("images/layouts/one_wall.png", width=120)
        if st.button(t('1wall', l), use_container_width=True, key="lay1"):
            st.session_state.layout = "One-Wall"
            st.rerun()
    with c2:
        st.image("images/layouts/l_shaped.png", width=120)
        if st.button(t('lshape', l), use_container_width=True, key="lay2"):
            st.session_state.layout = "L-Shaped"
            st.rerun()
    with c3:
        st.image("images/layouts/u_shaped.png", width=120)
        if st.button(t('ushape', l), use_container_width=True, key="lay3"):
            st.session_state.layout = "U-Shaped"
            st.rerun()
    with c4:
        st.image("images/layouts/galley.png", width=120)
        if st.button(t('galley', l), use_container_width=True, key="lay4"):
            st.session_state.layout = "Galley"
            st.rerun()
    if st.session_state.layout is None:
        st.info(f"👆 {t('sel', l)}")
        return
    st.markdown(f"<div class='success-badge'>✓ {st.session_state.layout}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='step-header'>📏 {t('s4', l)}</div>", unsafe_allow_html=True)
    {"One-Wall": calc1w, "L-Shaped": calcL, "U-Shaped": calcU, "Galley": calcG}[st.session_state.layout](l)

def wardrobe(l):
    st.markdown(f"<div class='step-header'>📏 {t('s3w', l)}</div>", unsafe_allow_html=True)
    st.markdown(f"**{t('basic', l)}**")
    c1, c2 = st.columns(2)
    with c1: h = st.number_input(t('h', l), 0.0, value=2.4, step=0.1, key="wh")
    with c2: w = st.number_input(t('w', l), 0.0, value=2.0, step=0.1, key="ww")
    st.markdown(f"**{t('feat', l)}**")
    c1, c2 = st.columns(2)
    with c1:
        sh = st.checkbox(t('shelf', l), key="sh")
        ns = st.number_input(t('nshelf', l), 0, 20, value=5, step=1, key="ns") if sh else 0
    with c2: dt = st.radio(t('door', l), [t('hinge', l), t('slide', l)], key="dt")
    mi = st.checkbox(t('mirror', l), key="mi")
    ga = 0
    if mi:
        c1, c2 = st.columns(2)
        with c1: gh = st.number_input(t('gh', l), 0.0, value=2.0, step=0.1, key="gh")
        with c2: gw = st.number_input(t('gw', l), 0.0, value=1.0, step=0.1, key="gw")
        ga = gh * gw
    if h > 0 and w > 0:
        ba, sa = h*w, w*CABINET_DEPTH*ns if sh else 0
        ta = (ba+sa+ga)*WASTE_FACTOR
        mp, gc, sc = ta*MATERIAL_PRICES[st.session_state.material], ga*50 if mi else 0, 200 if dt == t('slide', l) else 0
        tp = mp+gc+sc
        st.session_state.calculation_details = {"Height": h, "Width": w, "Shelves": sh, "Num": ns, "Door": dt, "Mirror": mi, "Glass H": gh if mi else 0, "Glass W": gw if mi else 0, "glass_cost": gc, "sliding_cost": sc, "total_price": tp}
        breakdown({"Base": ba, "Shelves": sa, "Glass": ga, "Subtotal": ba+sa+ga, "Waste 10%": ta-(ba+sa+ga), "Total Area": ta}, mp, gc, sc, tp, l)

def show_price_calculator():
    css()
    if "lang" not in st.session_state: st.session_state.lang = "en"
    c1, c2, c3, c4 = st.columns([1,1,1,6])
    with c1:
        if st.button("EN", use_container_width=True, key="len"):
            st.session_state.lang = "en"
            st.rerun()
    with c2:
        if st.button("کوردی", use_container_width=True, key="lku"):
            st.session_state.lang = "ku"
            st.rerun()
    with c3:
        if st.button("العربية", use_container_width=True, key="lar"):
            st.session_state.lang = "ar"
            st.rerun()
    l = st.session_state.lang
    st.markdown(f"<h1 style='text-align: center; color: #1f2937; font-weight: 600; margin-top: 20px;'>🧮 {t('calc', l)}</h1>", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align: center; color: #6b7280; margin-bottom: 10px;'>{t('sub', l)}</p>", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align: center; color: #10b981; font-weight: 600; font-size: 18px; margin-bottom: 30px;'>{t('company', l)}</p>", unsafe_allow_html=True)
    for k in ["material", "product", "layout", "calculation_details"]:
        if k not in st.session_state: st.session_state[k] = None if k != "calculation_details" else {}
    st.markdown(f"<div class='step-header'>📦 {t('s1', l)}</div>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1:
        st.image("images/materials/mdf.png", width=150)
        if st.button("MDF\n$120/m²", use_container_width=True, key="m1"):
            st.session_state.material = "MDF"
            st.rerun()
    with c2:
        st.image("images/materials/balloon_press.png", width=150)
        if st.button("Balloon Press\n$160/m²", use_container_width=True, key="m2"):
            st.session_state.material = "Balloon Press"
            st.rerun()
    with c3:
        st.image("images/materials/glass.png", width=150)
        if st.button("Glass\n$170/m²", use_container_width=True, key="m3"):
            st.session_state.material = "Glass"
            st.rerun()
    if st.session_state.material is None:
        st.info(f"👆 {t('sel', l)}")
        return
    st.markdown(f"<div class='success-badge'>✓ {st.session_state.material} - ${MATERIAL_PRICES[st.session_state.material]}/m²</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='step-header'>🏠 {t('s2', l)}</div>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1,2,1])
    with c2:
        sc1, sc2 = st.columns(2)
        with sc1:
            st.image("images/products/kitchen.png", width=180)
            if st.button(t('kitchen', l), use_container_width=True, key="p1"):
                st.session_state.product = "Kitchen"
                st.session_state.layout = None
                st.rerun()
        with sc2:
            st.image("images/products/wardrobe.png", width=180)
            if st.button(t('wardrobe', l), use_container_width=True, key="p2"):
                st.session_state.product = "Wardrobe"
                st.session_state.layout = None
                st.rerun()
    if st.session_state.product is None:
        st.info(f"👆 {t('sel', l)}")
        return
    pd = t('kitchen', l) if st.session_state.product == "Kitchen" else t('wardrobe', l)
    st.markdown(f"<div class='success-badge'>✓ {pd}</div>", unsafe_allow_html=True)
    (kitchen if st.session_state.product == "Kitchen" else wardrobe)(l)
