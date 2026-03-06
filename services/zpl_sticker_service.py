import segno

BASE_URL = "https://render-ml-automation.onrender.com"


def generar_qr_ascii(order_id):

    url = f"{BASE_URL}/form?order={order_id}"

    qr = segno.make(url)

    matrix = qr.matrix

    zpl = "^XA\n"

    y = 20

    for row in matrix:

        x = 20

        for col in row:

            if col:
                zpl += f"^FO{x},{y}^GB6,6,6^FS\n"

            x += 6

        y += 6

    zpl += "^XZ"

    return zpl


def generar_sticker(order_id):

    qr = generar_qr_ascii(order_id)

    zpl = f"""
^XA
^FO50,30^A0N,30,30^FDSoporte pedido ML^FS
{qr}
^FO50,250^A0N,25,25^FDEscanea si hay problema^FS
^XZ
"""

    return zpl


def combinar_etiqueta(label_zpl, qr_zpl):

    label_zpl = label_zpl.replace("^XZ", "")

    zpl = f"""
{label_zpl}

^FO50,700
^A0N,30,30
^FDSoporte post venta^FS

{qr_zpl}

^XZ
"""

    return zpl
