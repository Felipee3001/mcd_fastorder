from django.contrib import admin
from django.urls import path, include
from mcd_v1.views import menu_cliente_view # Importamos tu vista real

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('mcd_v1.urls')),
    path('', lambda request: menu_cliente_view(request, id_cliente=1), name='home_raiz'),
]
