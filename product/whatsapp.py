import urllib.parse

def build_whatsapp_link(phone: str, product_url: str) -> str:
    """
    Build a WhatsApp link with pre-filled message including the product URL.
    
    Example:
        https://wa.me/+9647501003839?text=message
    """
    message = f"السلام علیکم، دەمەوێت زیاتر بزانم لەسەر ئەم بەرهەمە: {product_url}"
    encoded_message = urllib.parse.quote(message)
    return f"https://wa.me/{phone}?text={encoded_message}"
