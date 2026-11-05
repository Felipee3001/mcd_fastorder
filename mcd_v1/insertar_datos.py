import os
import django

# Configuramos el entorno de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mcd_fastorder_backend.settings')
django.setup()

from mcd_v1.models import Producto

print("Iniciando inyección de menú...")

# Insertamos tus productos con las columnas reales de tu base de datos
p1, c1 = Producto.objects.get_or_create(idProducto="1", nombreProducto="🍔 Big Mac Magnífica", precioBase=5500, disponibleStock=True)
p2, c2 = Producto.objects.get_or_create(idProducto="2", nombreProducto="🍟 Papas Fritas Grandes", precioBase=2800, disponibleStock=True)
p3, c3 = Producto.objects.get_or_create(idProducto="3", nombreProducto="🥤 Bebida Express", precioBase=1900, disponibleStock=True)

print("¡MENÚ INYECTADO CORRECTAMENTE EN POSTGRESQL!")
