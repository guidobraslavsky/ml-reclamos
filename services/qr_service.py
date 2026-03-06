import qrcode
import os

BASE_URL = "https://render-ml-automation.onrender.com"


def generar_qr(order_id):

    url = f"{BASE_URL}/form?order={order_id}"

    qr = qrcode.QRCode(
        version=None,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=12,
        border=4,
    )

    qr.add_data(url)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")

    os.makedirs("qrs", exist_ok=True)

    filename = f"qr_{order_id}.png"

    path = f"qrs/{filename}"

    img.save(path)

    return path
