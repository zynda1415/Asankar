import streamlit as st
import pandas as pd
from datetime import datetime
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER, TA_RIGHT, TA_LEFT
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import io

# Config
MATERIAL_PRICES = {"MDF": 120, "Balloon Press": 160, "Glass": 170}
WASTE_FACTOR, DISHWASHER_AREA, FRIDGE_DEPTH, CABINET_DEPTH, OVEN_HEIGHT, VITRINE_BASE_HEIGHT = 1.10, 0.51, 0.6, 0.6, 0.85, 0.6

# Translations
T = {
    "en": {
        "company": "Asankar Company", "company_ar": "کۆمپانیای ئاسانکار", 
        "calc": "Price Calculator", "sub": "Configure your dream kitchen or wardrobe", 
        "s1": "Step 1: Select Material", "s2": "Step 2: Select Product", 
        "s3k": "Step 3: Kitchen Layout", "s3w": "Step 3: Wardrobe Config", 
        "s4": "Step 4: Dimensions & Appliances", "kitchen": "Kitchen", "wardrobe": "Wardrobe", 
        "1wall": "One-Wall", "lshape": "L-Shaped", "ushape": "U-Shaped", "galley": "Galley", 
        "dims": "Wall Dimensions", "h": "Height (m)", "l": "Length (m)", "w": "Width (m)", 
        "app": "Appliances", "fridge": "🧊 Refrigerator", "dish": "🍽️ Dishwasher", 
        "cab": "🗄️ Cabinet", "stove": "🔥 Stove", "oven": "With oven", "vit": "🪟 Vitrine", 
        "shelf": "📚 Shelves", "nshelf": "Number of shelves", "door": "🚪 Door type", 
        "hinge": "Hinged", "slide": "Sliding", "mirror": "🪞 Mirror/Glass", 
        "gh": "Glass height (m)", "gw": "Glass width (m)", "break": "Price Breakdown", 
        "comp": "Component", "area": "Area (m²)", "mat": "Material", "perm2": "Price/m²", 
        "matcost": "Material Cost", "glasscost": "Glass Cost", "slidecost": "Sliding System", 
        "total": "TOTAL PRICE", "new": "🔄 New Calc", "down": "📄 Download", 
        "share": "💬 WhatsApp", "sel": "Please select to continue", 
        "basic": "Basic Dimensions", "feat": "Additional Features",
        "quote": "PRICE QUOTATION", "quote_num": "Quote Number", "date": "Date",
        "material": "Material", "product": "Product Type", "layout": "Layout",
        "details": "PROJECT DETAILS", "desc": "Description", "spec": "Specification",
        "yes": "Yes", "no": "No", "breakdown_title": "AREA CALCULATION BREAKDOWN",
        "item": "Item", "notes": "Notes", "subtracted": "Subtracted", "added": "Added (10%)",
        "calculated": "Calculated", "price_summary": "PRICE SUMMARY", 
        "quantity": "Quantity", "rate": "Rate", "amount": "Amount",
        "subtotal": "SUBTOTAL", "tax": "TAX (if applicable)", "terms": "TERMS & CONDITIONS",
        "term1": "This quotation is valid for 30 days from the date of issue.",
        "term2": "Prices include materials and installation labor.",
        "term3": "A 50% deposit is required to commence work.",
        "term4": "Final dimensions will be confirmed on-site before production.",
        "term5": "Installation timeline: 2-4 weeks from deposit confirmation.",
        "term6": "Warranty: 2 years on materials and workmanship.",
        "thank": "Thank you for choosing Asankar Company",
        "contact": "Contact: info@asankar.com | Phone: +964-xxx-xxxx"
    },
    "ku": {
        "company": "کۆمپانیای ئاسانکار", "company_ar": "کۆمپانیای ئاسانکار",
        "calc": "حیسابکەری نرخ", "sub": "چێشتخانە یان جلخانە ڕێکبخە", 
        "s1": "هەنگاو ١: ماددە هەڵبژێرە", "s2": "هەنگاو ٢: بەرهەم هەڵبژێرە", 
        "s3k": "هەنگاو ٣: شێوەی چێشتخانە", "s3w": "هەنگاو ٣: ڕێکخستنی جلخانە", 
        "s4": "هەنگاو ٤: پێوانە و ئامێر", "kitchen": "چێشتخانە", "wardrobe": "جلخانە", 
        "1wall": "یەک-دیوار", "lshape": "L شێوەی", "ushape": "U شێوەی", "galley": "هاوتەریب", 
        "dims": "پێوانەی دیوار", "h": "بەرزی (م)", "l": "درێژی (م)", "w": "پانی (م)", 
        "app": "ئامێرەکان", "fridge": "🧊 سارکەرەوە", "dish": "🍽️ قاپشۆر", 
        "cab": "🗄️ کابینێت", "stove": "🔥 هێڵان", "oven": "لەگەڵ تەنوور", 
        "vit": "🪟 ڤیترین", "shelf": "📚 تەختە", "nshelf": "ژمارەی تەختە", 
        "door": "🚪 دەرگا", "hinge": "پاشۆڵە", "slide": "خلیسکان", "mirror": "🪞 ئاوێنە", 
        "gh": "بەرزی شووشە (م)", "gw": "پانی شووشە (م)", "break": "وردەکاری نرخ", 
        "comp": "پێکهاتە", "area": "ڕووبەر (م²)", "mat": "ماددە", "perm2": "نرخ/م²", 
        "matcost": "تێچووی ماددە", "glasscost": "تێچووی شووشە", 
        "slidecost": "سیستەمی خلیسکان", "total": "کۆی گشتی", "new": "🔄 نوێ", 
        "down": "📄 داگرتن", "share": "💬 واتساپ", "sel": "تکایە هەڵبژێرە", 
        "basic": "پێوانە بنەڕەتی", "feat": "تایبەتمەندی زیادە",
        "quote": "پسوڵەی نرخ", "quote_num": "ژمارەی پسوڵە", "date": "بەروار",
        "material": "ماددە", "product": "جۆری بەرهەم", "layout": "شێواز",
        "details": "وردەکاریی پڕۆژە", "desc": "وەسف", "spec": "تایبەتمەندی",
        "yes": "بەڵێ", "no": "نەخێر", "breakdown_title": "وردەکاریی حیسابکردنی ڕووبەر",
        "item": "بابەت", "notes": "تێبینی", "subtracted": "لابراو", "added": "زیادکراو (١٠٪)",
        "calculated": "حیسابکراو", "price_summary": "کورتەی نرخ",
        "quantity": "بڕ", "rate": "ڕێژە", "amount": "بڕی پارە",
        "subtotal": "کۆی لاوەکی", "tax": "باج (ئەگەر هەبێت)", "terms": "مەرج و ڕێسا",
        "term1": "ئەم پسوڵەیە بەکارە بۆ ماوەی ٣٠ ڕۆژ لە بەرواری دەرچوون.",
        "term2": "نرخەکان ماددە و دامەزراندن لەخۆدەگرن.",
        "term3": "پێویستە ٥٠٪ پێشەکی بۆ دەستپێکردنی کار.",
        "term4": "پێوانە کۆتاییەکان لەسەر شوێن پشتڕاست دەکرێنەوە.",
        "term5": "کاتی دامەزراندن: ٢-٤ هەفتە لە دوای پشتڕاستکردنەوەی پێشەکی.",
        "term6": "گەرەنتی: ٢ ساڵ بۆ ماددە و کارکردن.",
        "thank": "سوپاس بۆ هەڵبژاردنی کۆمپانیای ئاسانکار",
        "contact": "پەیوەندی: info@asankar.com | ژمارە: +964-xxx-xxxx"
    },
    "ar": {
        "company": "شركة أسانكار", "company_ar": "کۆمپانیای ئاسانکار",
        "calc": "حاسبة الأسعار", "sub": "قم بتكوين مطبخ أو خزانة", 
        "s1": "الخطوة ١: اختر المادة", "s2": "الخطوة ٢: اختر المنتج", 
        "s3k": "الخطوة ٣: تصميم المطبخ", "s3w": "الخطوة ٣: تكوين الخزانة", 
        "s4": "الخطوة ٤: الأبعاد والأجهزة", "kitchen": "مطبخ", "wardrobe": "خزانة", 
        "1wall": "جدار واحد", "lshape": "شكل L", "ushape": "شكل U", "galley": "متوازي", 
        "dims": "أبعاد الجدار", "h": "الارتفاع (م)", "l": "الطول (م)", "w": "العرض (م)", 
        "app": "الأجهزة", "fridge": "🧊 ثلاجة", "dish": "🍽️ غسالة صحون", 
        "cab": "🗄️ خزانة", "stove": "🔥 موقد", "oven": "مع فرن", "vit": "🪟 فاترينا", 
        "shelf": "📚 رفوف", "nshelf": "عدد الرفوف", "door": "🚪 الباب", 
        "hinge": "مفصلي", "slide": "منزلق", "mirror": "🪞 مرآة", 
        "gh": "ارتفاع الزجاج (م)", "gw": "عرض الزجاج (م)", "break": "تفاصيل السعر", 
        "comp": "المكون", "area": "المساحة (م²)", "mat": "المادة", "perm2": "السعر/م²", 
        "matcost": "تكلفة المواد", "glasscost": "تكلفة الزجاج", 
        "slidecost": "نظام الانزلاق", "total": "السعر الإجمالي", "new": "🔄 جديد", 
        "down": "📄 تحميل", "share": "💬 واتساب", "sel": "الرجاء الاختيار", 
        "basic": "الأبعاد الأساسية", "feat": "ميزات إضافية",
        "quote": "عرض السعر", "quote_num": "رقم العرض", "date": "التاريخ",
        "material": "المادة", "product": "نوع المنتج", "layout": "التصميم",
        "details": "تفاصيل المشروع", "desc": "الوصف", "spec": "المواصفات",
        "yes": "نعم", "no": "لا", "breakdown_title": "تفصيل حساب المساحة",
        "item": "البند", "notes": "ملاحظات", "subtracted": "مطروح", "added": "مضاف (١٠٪)",
        "calculated": "محسوب", "price_summary": "ملخص السعر",
        "quantity": "الكمية", "rate": "السعر", "amount": "المبلغ",
        "subtotal": "المجموع الفرعي", "tax": "الضريبة (إن وجدت)", "terms": "الشروط والأحكام",
        "term1": "هذا العرض صالح لمدة ٣٠ يومًا من تاريخ الإصدار.",
        "term2": "تشمل الأسعار المواد والتركيب.",
        "term3": "مطلوب دفعة مقدمة بنسبة ٥٠٪ لبدء العمل.",
        "term4": "سيتم تأكيد الأبعاد النهائية في الموقع قبل الإنتاج.",
        "term5": "الجدول الزمني للتركيب: ٢-٤ أسابيع من تأكيد الدفعة المقدمة.",
        "term6": "الضمان: سنتان على المواد والتصنيع.",
        "thank": "شكراً لاختياركم شركة أسانكار",
        "contact": "الاتصال: info@asankar.com | الهاتف: +964-xxx-xxxx"
    }
}

def t(k, l="en"): 
    return T.get(l, T["en"]).get(k, k)

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

def generate_pdf(bd, cd, mat, prod, lay, lang):
    """Generate professional multilingual PDF"""
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, topMargin=0.5*inch, bottomMargin=0.5*inch, 
                           leftMargin=0.75*inch, rightMargin=0.75*inch)
    story = []
    styles = getSampleStyleSheet()
    
    # Determine text alignment based on language
    text_align = TA_RIGHT if lang in ["ku", "ar"] else TA_LEFT
    
    # Custom Styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=22,
        textColor=colors.HexColor('#10b981'),
        spaceAfter=20,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    
    subtitle_style = ParagraphStyle(
        'CustomSubtitle',
        parent=styles['Heading2'],
        fontSize=16,
        textColor=colors.HexColor('#1f2937'),
        spaceAfter=15,
        alignment=text_align,
        fontName='Helvetica-Bold'
    )
    
    normal_style = ParagraphStyle(
        'CustomNormal',
        parent=styles['Normal'],
        fontSize=10,
        alignment=text_align,
        fontName='Helvetica'
    )
    
    # Header - Company Name (bilingual)
    story.append(Paragraph(t('company_ar', lang), title_style))
    story.append(Paragraph(t('company', lang), title_style))
    story.append(Spacer(1, 0.1*inch))
    story.append(Paragraph(t('quote', lang), subtitle_style))
    story.append(Spacer(1, 0.3*inch))
    
    # Quote Info Table
    quote_date = datetime.now().strftime("%B %d, %Y")
    quote_num = datetime.now().strftime("%Y%m%d%H%M%S")
    
    info_data = [
        [t('quote_num', lang), quote_num, t('date', lang), quote_date],
        [t('material', lang), mat, t('product', lang), prod]
    ]
    if lay:
        info_data.append([t('layout', lang), lay, '', ''])
    
    info_table = Table(info_data, colWidths=[1.5*inch, 2*inch, 1.2*inch, 1.8*inch])
    info_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#f9fafb')),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#1f2937')),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ('TOPPADDING', (0, 0), (-1, -1), 10),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#e5e7eb')),
        ('ROUNDEDCORNERS', [5, 5, 5, 5]),
    ]))
    story.append(info_table)
    story.append(Spacer(1, 0.4*inch))
    
    # Project Details
    story.append(Paragraph(t('details', lang), subtitle_style))
    story.append(Spacer(1, 0.15*inch))
    
    details_data = [[t('desc', lang), t('spec', lang)]]
    for key, value in cd.items():
        if key not in ['glass_cost', 'sliding_cost', 'total_price']:
            if isinstance(value, float):
                details_data.append([key, f"{value:.2f} m"])
            elif isinstance(value, bool):
                details_data.append([key, t('yes', lang) if value else t('no', lang)])
            else:
                details_data.append([key, str(value)])
    
    details_table = Table(details_data, colWidths=[3*inch, 3.5*inch])
    details_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#10b981')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 11),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#e5e7eb')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#fafafa')]),
    ]))
    story.append(details_table)
    story.append(Spacer(1, 0.4*inch))
    
    # Area Breakdown
    story.append(Paragraph(t('breakdown_title', lang), subtitle_style))
    story.append(Spacer(1, 0.15*inch))
    
    breakdown_data = [[t('item', lang), t('area', lang), t('notes', lang)]]
    for item, value in bd.items():
        if value != 0:
            note = ""
            if "deduction" in item.lower() or "(-)" in item:
                note = t('subtracted', lang)
            elif "waste" in item.lower():
                note = t('added', lang)
            elif "total" in item.lower() or "subtotal" in item.lower():
                note = t('calculated', lang)
            
            breakdown_data.append([item, f"{abs(value):.2f}", note])
    
    breakdown_table = Table(breakdown_data, colWidths=[2.5*inch, 1.8*inch, 2.2*inch])
    breakdown_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#10b981')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (0, -1), 'LEFT'),
        ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
        ('ALIGN', (2, 0), (2, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 11),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#e5e7eb')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#fafafa')]),
    ]))
    
    # Highlight total row
    for i, row in enumerate(breakdown_data):
        if 'Total Area' in row[0] or t('total', lang) in row[0]:
            breakdown_table.setStyle(TableStyle([
                ('BACKGROUND', (0, i), (-1, i), colors.HexColor('#d1fae5')),
                ('FONTNAME', (0, i), (-1, i), 'Helvetica-Bold'),
                ('TEXTCOLOR', (0, i), (-1, i), colors.HexColor('#065f46')),
            ]))
    
    story.append(breakdown_table)
    story.append(Spacer(1, 0.4*inch))
    
    # Price Summary
    story.append(Paragraph(t('price_summary', lang), subtitle_style))
    story.append(Spacer(1, 0.15*inch))
    
    total_area = bd.get('Total Area', 0)
    material_rate = MATERIAL_PRICES[mat]
    material_cost = total_area * material_rate
    
    price_data = [
        [t('desc', lang), t('quantity', lang), t('rate', lang), t('amount', lang)],
        [f'{mat} {t("material", lang)}', f'{total_area:.2f} m²', f'${material_rate}/m²', f'${material_cost:.2f}']
    ]
    
    # Additional costs
    if cd.get('glass_cost', 0) > 0:
        price_data.append([t('glasscost', lang), '-', '-', f"${cd['glass_cost']:.2f}"])
    
    if cd.get('sliding_cost', 0) > 0:
        price_data.append([t('slidecost', lang), '-', '-', f"${cd['sliding_cost']:.2f}"])
    
    total_price = cd.get('total_price', material_cost)
    
    price_data.append(['', '', t('subtotal', lang), f'${total_price:.2f}'])
    price_data.append(['', '', t('tax', lang), '$0.00'])
    price_data.append(['', '', t('total', lang).upper(), f'${total_price:.2f}'])
    
    price_table = Table(price_data, colWidths=[2.3*inch, 1.5*inch, 1.4*inch, 1.3*inch])
    price_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#10b981')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, 0), 'LEFT'),
        ('ALIGN', (2, 0), (-1, -1), 'RIGHT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 11),
        ('FONTNAME', (0, 1), (-1, -4), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -4), 9),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -4), 0.5, colors.HexColor('#e5e7eb')),
        ('LINEABOVE', (2, -3), (-1, -3), 1.5, colors.HexColor('#9ca3af')),
        ('LINEABOVE', (2, -1), (-1, -1), 2, colors.HexColor('#10b981')),
        ('BACKGROUND', (2, -1), (-1, -1), colors.HexColor('#d1fae5')),
        ('FONTNAME', (2, -1), (-1, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (2, -1), (-1, -1), 12),
        ('TEXTCOLOR', (2, -1), (-1, -1), colors.HexColor('#065f46')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -4), [colors.white, colors.HexColor('#fafafa')]),
    ]))
    story.append(price_table)
    story.append(Spacer(1, 0.4*inch))
    
    # Terms & Conditions
    story.append(Paragraph(t('terms', lang), subtitle_style))
    story.append(Spacer(1, 0.1*inch))
    
    terms_text = f"""
    1. {t('term1', lang)}<br/>
    2. {t('term2', lang)}<br/>
    3. {t('term3', lang)}<br/>
    4. {t('term4', lang)}<br/>
    5. {t('term5', lang)}<br/>
    6. {t('term6', lang)}<br/>
    """
    story.append(Paragraph(terms_text, normal_style))
    story.append(Spacer(1, 0.3*inch))
    
    # Footer
    footer_style = ParagraphStyle(
        'Footer',
        parent=styles['Normal'],
        fontSize=9,
        textColor=colors.HexColor('#6b7280'),
        alignment=TA_CENTER
    )
    story.append(Paragraph(t('thank', lang), footer_style))
    story.append(Spacer(1, 0.05*inch))
    story.append(Paragraph(t('contact', lang), footer_style))
    
    doc.build(story)
    buffer.seek(0)
    return buffer

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
        # Generate PDF
        pdf_buffer = generate_pdf(
            bd, 
            st.session_state.calculation_details, 
            st.session_state.material, 
            st.session_state.product,
            st.session_state.layout if st.session_state.product == "Kitchen" else None,
            l
        )
        st.download_button(
            t('down', l), 
            pdf_buffer, 
            f"quote_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf", 
            "application/pdf", 
            use_container_width=True
        )
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
