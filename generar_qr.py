import os
import qrcode

def crear_codigo_qr():
    print("Generando código QR para McD-FastOrder...")
    
    # OPCIÓN A: Para pruebas en el mismo computador (Simulador del navegador)
    url_proyecto = "http://127.0.0.1:8000"
    
    # OPCIÓN B: Para escanear con un celular real en la misma red Wi-Fi
    # Reemplaza '192.168.1.X' por la IP local de tu computador (puedes verla con 'ipconfig' en el CMD)
    # url_proyecto = "http://192.168.1.X:8000/api/"

    # Configurar los parámetros del código QR
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    
    # Inyectar la URL del sistema web
    qr.add_data(url_proyecto)
    qr.make(fit=True)

    # Crear la imagen con los colores institucionales (Fondo blanco, código negro)
    imagen_qr = qr.make_image(fill_color="black", back_color="white")
    
    # Guardar el archivo PNG en la carpeta del proyecto
    nombre_archivo = "qr_mcd_fastorder.png"
    imagen_qr.save(nombre_archivo)
    
    print(f"✔️ ¡Código QR generado con éxito! Archivo guardado como: {nombre_archivo}")
    print(f"🔗 El QR apunta a: {url_proyecto}")

if __name__ == '__main__':
    crear_codigo_qr()