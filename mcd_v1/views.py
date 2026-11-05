from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
from django.db import transaction
import json
import time
from .models import Cliente, Producto, PedidoExpress, DetallePedido

# ==========================================
# 🔑 VISTAS DEL SISTEMA DE LOGIN Y ACCESO
# ==========================================

@ensure_csrf_cookie
def vista_login(request):
    """Maneja el renderizado del login y la validación segura en el servidor"""
    if request.method == 'POST':
        try:
            datos = json.loads(request.body)
            rol = datos.get('rol')
            
            if rol == 'usuario':
                return JsonResponse({'status': 'Ok', 'redirect': '/cliente/1/'})
                
            elif rol == 'admin':
                usuario = datos.get('username', '').strip()
                contrasena = datos.get('password', '')
                
                # 🔒 Validación protegida en el backend (Fuera del alcance de DevTools)
                if usuario == "Felipe Nuñez" and contrasena == "inacap123":
                    return JsonResponse({'status': 'Ok', 'redirect': '/cocina/'})
                else:
                    return JsonResponse({'error': 'Usuario o contraseña incorrectos'}, status=401)
                    
        except json.JSONDecodeError:
            return JsonResponse({'error': 'JSON inválido'}, status=400)
            
    # Si es un método GET, renderiza la página normalmente
    return render(request, 'login.html')

def vista_index(request):
    """Redirige al flujo nativo con el Cliente ID por defecto 1"""
    return redirect('menu_express', id_cliente=1)

def vista_cocina(request):
    """Redirige directamente a la pantalla principal del monitor de cocina"""
    return redirect('pantalla_cocina')

# ==========================================
# 🍔 VISTAS DE MONITORES Y PANTALLAS
# ==========================================

def pantalla_cocina_view(request):
    """Renderiza la vista HTML del monitor de cocina"""
    return render(request, 'cocina.html')

@ensure_csrf_cookie
def menu_cliente_view(request, id_cliente):
    """Busca los productos en la BD y los pasa al HTML con su stock real"""
    productos_db = Producto.objects.all().order_by('idProducto')
    lista_productos = []
    for p in productos_db:
        lista_productos.append({
            'id': p.idProducto,
            'nombre': p.nombreProducto,
            'precio': int(p.precioBase), # ✨ CLAVE: Convertimos a entero para que json.dumps funcione
            'disponible': 1 if p.disponibleStock else 0
        })
        
    return render(request, 'index.html', {
        'id_cliente': id_cliente,
        'productos_json': json.dumps(lista_productos)
    })

# ==========================================
# ⚙️ VISTAS DE API (PROCESAMIENTO ASÍNCRONO)
# ==========================================

@csrf_exempt
def procesar_pedido_express(request):
    """Recibe la orden express en MySQL resolviendo dinámicamente desajustes del Cliente ID"""
    if request.method != 'POST':
        return JsonResponse({'error': 'Método no permitido. Use POST.'}, status=405)
    
    try:
        datos = json.loads(request.body)
        id_cliente = datos.get('idCliente')
        items = datos.get('items', [])
        nombre_cliente = datos.get('nombreLlamado', 'Cliente Express')
        
        if not id_cliente or not items:
            return JsonResponse({'error': 'Datos de orden incompletos'}, status=400)
        
        # Normalizamos el identificador quitando espacios y limitando a 15 caracteres
        id_cliente_str = str(id_cliente).strip()[:15]
        
        try:
            cliente = Cliente.objects.get(pk=id_cliente_str)
        except Cliente.DoesNotExist:
            # 🌟 RESOLUCIÓN DEL ERROR 500: Creamos el objeto instanciando de forma explícita 
            # todos los campos requeridos por tu modelo de base de datos
            cliente = Cliente.objects.create(
                idCliente=id_cliente_str,
                tokenDispositivo=None,
                preferenciaId="1"
            )
        
        total_pago = 0
        detalles_a_crear = []
        
        with transaction.atomic():
            for item in items:
                id_prod = item.get('idProducto')
                cant = item.get('cantidad')
                
                try:
                    producto = Producto.objects.get(pk=id_prod)
                except Producto.DoesNotExist:
                    return JsonResponse({'error': f'Producto ID {id_prod} no existe'}, status=404)
                
                if not producto.disponibleStock:
                    return JsonResponse({'error': f'El producto {producto.nombreProducto} no tiene stock'}, status=400)
                
                sub_t = producto.precioBase * cant
                total_pago += sub_t
                
                detalles_a_crear.append({
                    'producto': producto,
                    'cantidad': cant,
                    'subtotal': sub_t
                })
            
            # Generamos el ID único de 14 caracteres cumpliendo el max_length=15
            cantidad_pedidos = PedidoExpress.objects.count()
            siguiente_numero = cantidad_pedidos + 1
            
            # Lo guardamos como un String simple (Ej: "4", "5", "6")
            # Cumple perfectamente con medir menos de 15 caracteres
            id_ticket_unico = str(siguiente_numero)
            
            # Creación del registro principal en MySQL
            pedido = PedidoExpress.objects.create(
                idPedido=id_ticket_unico,
                idCliente=cliente,
                totalPago=total_pago,
                nombreLlamado=nombre_cliente
            )
            
            for d in detalles_a_crear:
                DetallePedido.objects.create(
                    idPedido=pedido,
                    idProducto=d['producto'],  # 🌟 CORREGIDO: Cambiado de d['idProducto'] a d['producto']
                    cantidad=d['cantidad'],
                    subtotal=d['subtotal']
                )
        
        return JsonResponse({
            'status': 'Ok',
            'idPedido': pedido.idPedido,
            'mensaje': 'Pedido recibido directamente en cocina',
            'totalTransaccion': total_pago
        }, status=201)

    except json.JSONDecodeError:
        return JsonResponse({'error': 'JSON inválido'}, status=400)
    except Exception as e:
        return JsonResponse({'error': 'Falla interna del servidor local', 'detalle': str(e)}, status=500)

def api_listar_pedidos(request):
    """Lista todas las órdenes en preparación para la pantalla de cocina"""
    pedidos = PedidoExpress.objects.filter(estado='Preparando').order_by('-timestampOrden')
    data = []
    for p in pedidos:
        items = [{'producto': d.idProducto.nombreProducto, 'cantidad': d.cantidad} for d in p.detalles.all()]
        data.append({
            'idPedido': p.idPedido,
            'timestamp': p.timestampOrden.strftime('%H:%M:%S'),
            'items': items,
            'nombreLlamado': p.nombreLlamado
        })
    return JsonResponse({'pedidos': data}, safe=False)

@csrf_exempt
def cambiar_estado_pedido(request, id_pedido):
    """Cambia el estado de una orden a 'Entregado' para sacarla del monitor"""
    try:
        pedido = PedidoExpress.objects.get(pk=id_pedido)
        pedido.estado = 'Entregado'
        pedido.save()
        return JsonResponse({'status': 'Ok', 'mensaje': f'Ticket #{id_pedido} actualizado'})
    except PedidoExpress.DoesNotExist:
        return JsonResponse({'error': 'Pedido no encontrado'}, status=404)

