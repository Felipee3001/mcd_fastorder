from django.urls import path
from .views import (
    procesar_pedido_express, 
    pantalla_cocina_view, 
    api_listar_pedidos, 
    cambiar_estado_pedido, 
    menu_cliente_view
)

urlpatterns = [
    path('cliente/<int:id_cliente>/', menu_cliente_view, name='menu_express'),
    path('fastOrder/', procesar_pedido_express, name='fast_order'),
    path('fastOrder', procesar_pedido_express), 
    path('cocina/', pantalla_cocina_view, name='pantalla_cocina'),
    path('cocina', pantalla_cocina_view),
    path('api/pedidos-cocina/', api_listar_pedidos, name='api_pedidos_cocina'),
    path('api/pedidos-cocina', api_listar_pedidos),
    path('api/despachar/<str:id_pedido>/', cambiar_estado_pedido, name='cambiar_estado_pedido'),
    path('api/despachar/<str:id_pedido>', cambiar_estado_pedido),
]
