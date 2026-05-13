# sistema/urls.py
from django.contrib import admin
from django.urls import path, include
from usuarios.views import login_view, logout_view  # nombres correctos
from tickets import views as ticket_views
from django.urls import path
from . import views


urlpatterns = [
    path('admin/', admin.site.urls),

    # Login / Logout
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),

    # Dashboard y tickets
    path('', ticket_views.dashboard, name='dashboard'),
    path('tickets/', ticket_views.lista_tickets, name='lista_tickets'),
    path('tickets/crear/', ticket_views.crear_ticket, name='crear_ticket'),
    path('tickets/<int:ticket_id>/', ticket_views.detalle_ticket, name='detalle_ticket'),
    path('tickets/<int:ticket_id>/editar/', ticket_views.editar_ticket, name='editar_ticket'),
    path('tickets/<int:id>/eliminar/', views.eliminar_ticket, name='eliminar_ticket'),

    # Clientes
    path('clientes/', ticket_views.lista_clientes, name='lista_clientes'),
    path('clientes/crear/', ticket_views.crear_cliente, name='crear_cliente'),
    path('clientes/<int:cliente_id>/editar/', ticket_views.editar_cliente, name='editar_cliente'),
    path('clientes/<int:cliente_id>/eliminar/', ticket_views.eliminar_cliente, name='eliminar_cliente'),

    # Informes
    path('informes/', ticket_views.informes, name='informes'),
]
