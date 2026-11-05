import os
import django

# Configurar el entorno de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mcd_fastorder_backend.settings')
django.setup()

from mcd_v1.models import Producto, Cliente

def poblar():
    print("Poblando base de datos de McD-FastOrder...")

    # 1. Insertar Productos Base
    productos = [
        {"nombre": "Big Mac", "precio": 4990},
        {"nombre": "Cuarto de Libra con Queso", "precio": 5290},
        {"nombre": "McNuggets 10 pzs", "precio": 3990},
        {"nombre": "Papas Fritas Medianas", "precio": 1890},
        {"nombre": "Bebida Mediana", "precio": 1500},
    ]

    for p in productos:
        obj, created = Producto.objects.get_or_create(
            nombreProducto=p["nombre"],
            defaults={"precioBase": p["precio"], "disponibleStock": True}
        )
        if created:
            print(f"✔️ Producto creado: {p['nombre']}")

    # 2. Insertar un Cliente de Prueba (necesario para el carrito express)
    cliente, created = Cliente.objects.get_or_create(
        idCliente=1,
        defaults={"tokenDispositivo": "token_felipe_celular", "preferenciaId": 1}
    )
    if created:
        print("✔️ Cliente de prueba ID: 1 creado con éxito.")

    print("¡Proceso de poblamiento finalizado con éxito!")

if __name__ == '__main__':
    poblar()
