import urllib.parse

def build_whatsapp_link(phone, product_name):
    message = f"Hello, I am interested in {product_name}"
    encoded = urllib.parse.quote(message)
    return f"https://wa.me/{phone}?text={encoded}"
