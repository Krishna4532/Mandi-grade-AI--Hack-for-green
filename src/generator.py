import qrcode
from PIL import Image, ImageDraw, ImageFont

def generate_mandi_pass(farmer_name, commodity, grade, price, score):
    # 1. Create the QR Code containing the 'Verified Data'
    # This prevents the trader from saying the app is "fake"
    qr_data = f"Farmer: {farmer_name} | Crop: {commodity} | Grade: {grade} | Score: {score}/100"
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(qr_data)
    qr.make(fit=True)
    qr_img = qr.make_image(fill_color="black", back_color="white")

    # 2. Create a High-Contrast Certificate (Farmer-Friendly)
    # Using 'Green-Bharat' theme colors
    canvas = Image.new('RGB', (600, 400), color=(255, 255, 255))
    draw = ImageDraw.Draw(canvas)
    
    # Add Text (Use large, bold fonts for low-literacy accessibility)
    draw.rectangle([0, 0, 600, 80], fill=(34, 139, 34)) # Green Header
    draw.text((20, 20), "MANDI GRADE: VERIFIED PASS", fill=(255, 255, 255))
    
    draw.text((20, 100), f"COMMODITY: {commodity.upper()}", fill=(0, 0, 0))
    draw.text((20, 140), f"OFFICIAL GRADE: {grade}", fill=(0, 0, 0))
    draw.text((20, 180), f"FAIR PRICE: Rs. {price}/kg", fill=(0, 0, 0))
    draw.text((20, 220), f"QUALITY SCORE: {score}%", fill=(34, 139, 34))

    # 3. Paste the QR Code onto the Certificate
    canvas.paste(qr_img, (350, 100))
    
    # Save the output
    cert_path = f"data/certificates/{farmer_name}_pass.png"
    canvas.save(cert_path)
    return cert_path

# Example Trigger (This would be called by your Pathway Sink)
# generate_mandi_pass("Krishna", "Wheat", "FAQ", 24.50, 92)