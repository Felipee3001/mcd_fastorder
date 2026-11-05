import os
import qrcode

# 1. Definimos la URL de tu producción en Render
url_producción = "https://mcd-fastorder.onrender.com/"

# 2. Configuramos los parámetros estéticos del código QR
qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_L,
    box_size=10,
    border=4,
)

qr.add_data(url_producción)
qr.make(fit=True)

# 3. Definimos la ruta de guardado apuntando de forma nativa a tus archivos estáticos
# Reemplaza 'mcd_v1' por el nombre exacto de tu carpeta de aplicación si es diferente
ruta_estaticos = os.path.join('mcd_v1', 'static')

# Aseguramos que la carpeta static exista antes de guardar
os.makedirs(ruta_estaticos, exist_ok=True)

# 4. Creamos y exportamos la imagen PNG
ruta_final_imagen = os.path.join(ruta_estaticos, 'qr_mcd_fastorder.png')
imagen_qr = qr.make_image(fill_color="black", back_color="white")
imagen_qr.save(ruta_final_imagen)

print(f"✅ ¡Código QR generado con éxito en: {ruta_final_imagen}!")
