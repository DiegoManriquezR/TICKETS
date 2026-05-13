from django.contrib import admin
from .models import Cliente, Ticket, Comentario


@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'email', 'empresa', 'telefono', 'activo', 'fecha_registro']
    list_filter = ['activo', 'fecha_registro']
    search_fields = ['nombre', 'email', 'empresa']
    list_per_page = 20


class ComentarioInline(admin.TabularInline):
    model = Comentario
    extra = 0
    readonly_fields = ['fecha_creacion']


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = [
        'id', 
        'titulo', 
        'cliente', 
        'prioridad', 
        'estado', 
        'tecnico_asignado', 
        'fecha_creacion'
    ]
    list_filter = ['estado', 'prioridad', 'fecha_creacion', 'tecnico_asignado']
    search_fields = ['titulo', 'descripcion', 'cliente__nombre']
    readonly_fields = [
        'fecha_creacion', 
        'fecha_asignacion', 
        'fecha_resolucion', 
        'fecha_cierre', 
        'fecha_actualizacion'
    ]
    list_per_page = 25
    date_hierarchy = 'fecha_creacion'
    inlines = [ComentarioInline]
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('titulo', 'descripcion', 'cliente')
        }),
        ('Estado y Prioridad', {
            'fields': ('estado', 'prioridad')
        }),
        ('Asignación', {
            'fields': ('tecnico_asignado', 'creado_por')
        }),
        ('Fechas', {
            'fields': (
                'fecha_creacion', 
                'fecha_asignacion', 
                'fecha_resolucion', 
                'fecha_cierre', 
                'fecha_actualizacion'
            ),
            'classes': ('collapse',)
        }),
    )


@admin.register(Comentario)
class ComentarioAdmin(admin.ModelAdmin):
    list_display = ['ticket', 'usuario', 'fecha_creacion', 'es_interno']
    list_filter = ['es_interno', 'fecha_creacion']
    search_fields = ['contenido', 'ticket__titulo', 'usuario__username']
    readonly_fields = ['fecha_creacion']
    list_per_page = 30