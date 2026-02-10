import urllib.parse

def build_whatsapp_link(phone, product_name):
    message = f"السلام علیکم، دەمەوێت زیاتر بزانم لەسەر ئەم بەرهەمە {product_name}"
    encoded = urllib.parse.quote(message)
    return f"https://wa.me/{phone}?text={encoded}"
