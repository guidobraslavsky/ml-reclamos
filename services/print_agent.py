import requests
import time

from services.zpl_sticker_service import generar_sticker
from services.print_service import imprimir_zpl

SERVER_URL = "https://render-ml-automation.onrender.com"


print("🚀 Print Agent iniciado")


def check_print_queue():

    try:

        print("Consultando servidor...")

        r = requests.get(f"{SERVER_URL}/print_queue")

        if r.status_code != 200:
            print("Error servidor:", r.status_code)
            return

        data = r.json()

        print("Respuesta servidor:", data)

        orders = data.get("orders", [])

        if not orders:
            print("No hay órdenes para imprimir")
            return

        for order in orders:

            order_id = order["order_id"]

            print("🖨 Imprimiendo orden:", order_id)

            zpl = generar_sticker(order_id)

            imprimir_zpl(zpl)

            # avisar al servidor que ya se imprimió
            requests.post(f"{SERVER_URL}/mark_printed", json={"order_id": order_id})

            print("Orden marcada como impresa")

    except Exception as e:

        print("Error en print agent:", e)


while True:

    check_print_queue()

    time.sleep(5)
