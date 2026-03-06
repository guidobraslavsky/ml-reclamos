import requests
import time
import subprocess

from services.zpl_sticker_service import generar_sticker

SERVER_URL = "https://render-ml-automation.onrender.com"

PRINTER_NAME = "XP410B"

printed_cache = set()

print("🚀 Print Agent iniciado")


def imprimir_zpl(zpl):

    try:

        subprocess.run(
            ["lpr", "-P", PRINTER_NAME, "-o", "raw"], input=zpl.encode(), check=True
        )

        print("Etiqueta enviada a impresora")

    except Exception as e:

        print("Error imprimiendo:", e)


def check_print_queue():

    try:

        print("Consultando servidor...")

        r = requests.get(f"{SERVER_URL}/print_queue", timeout=5)

        if r.status_code != 200:
            print("Error servidor:", r.status_code)
            return

        data = r.json()

        orders = data.get("orders", [])

        if not orders:
            print("No hay órdenes pendientes")
            return

        for order in orders:

            order_id = order["order_id"]

            if order_id in printed_cache:
                continue

            print("🖨 Imprimiendo orden:", order_id)

            zpl = generar_sticker(order_id)

            imprimir_zpl(zpl)

            printed_cache.add(order_id)

            requests.post(
                f"{SERVER_URL}/mark_printed", json={"order_id": order_id}, timeout=5
            )

            print("Orden marcada como impresa")

    except Exception as e:

        print("Error en agente:", e)


while True:

    check_print_queue()

    time.sleep(5)
