import subprocess

PRINTER_NAME = "XP410B"


def imprimir_zpl(zpl_code):

    process = subprocess.Popen(
        ["lpr", "-P", PRINTER_NAME, "-o", "raw"], stdin=subprocess.PIPE
    )

    process.communicate(zpl_code.encode())

    print("ZPL enviado a impresora")
