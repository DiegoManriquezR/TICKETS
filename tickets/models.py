from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Cliente(models.Model):
    nombre = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    empresa = models.CharField(max_length=100, blank=True, null=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    activo = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'
        ordering = ['nombre']

    def __str__(self):
        return f"{self.nombre} - {self.empresa if self.empresa else 'Sin empresa'}"


class Ticket(models.Model):
    PRIORIDAD_CHOICES = [
        ('baja', 'Baja'),
        ('media', 'Media'),
        ('alta', 'Alta'),
        ('critica', 'Crítica'),
    ]

    ESTADO_CHOICES = [
        ('abierto', 'Abierto'),
        ('en_proceso', 'En Proceso'),
        ('resuelto', 'Resuelto'),
        ('cerrado', 'Cerrado'),
    ]

    titulo = models.CharField(max_length=200)
    descripcion = models.TextField()
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='tickets')
    prioridad = models.CharField(max_length=10, choices=PRIORIDAD_CHOICES, default='media')
    estado = models.CharField(max_length=15, choices=ESTADO_CHOICES, default='abierto')
    
    # Asignación y fechas
    tecnico_asignado = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='tickets_asignados',
        limit_choices_to={'is_staff': True}
    )
    creado_por = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        related_name='tickets_creados'
    )
    
    # Seguimiento de tiempos
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_asignacion = models.DateTimeField(null=True, blank=True)
    fecha_resolucion = models.DateTimeField(null=True, blank=True)
    fecha_cierre = models.DateTimeField(null=True, blank=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Ticket'
        verbose_name_plural = 'Tickets'
        ordering = ['-fecha_creacion']

    def __str__(self):
        return f"#{self.id} - {self.titulo} [{self.get_estado_display()}]"

    def save(self, *args, **kwargs):
        # Registrar fecha de asignación cuando se asigna un técnico
        if self.tecnico_asignado and not self.fecha_asignacion:
            self.fecha_asignacion = timezone.now()
            if self.estado == 'abierto':
                self.estado = 'en_proceso'
        
        # Registrar fecha de resolución
        if self.estado == 'resuelto' and not self.fecha_resolucion:
            self.fecha_resolucion = timezone.now()
        
        # Registrar fecha de cierre
        if self.estado == 'cerrado' and not self.fecha_cierre:
            self.fecha_cierre = timezone.now()
        
        super().save(*args, **kwargs)

    def tiempo_respuesta(self):
        """Calcula el tiempo de respuesta en horas"""
        if self.fecha_asignacion:
            delta = self.fecha_asignacion - self.fecha_creacion
            return round(delta.total_seconds() / 3600, 2)
        return None

    def tiempo_resolucion(self):
        """Calcula el tiempo de resolución en horas"""
        if self.fecha_resolucion:
            delta = self.fecha_resolucion - self.fecha_creacion
            return round(delta.total_seconds() / 3600, 2)
        return None


class Comentario(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name='comentarios')
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    contenido = models.TextField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    es_interno = models.BooleanField(default=False, help_text="Comentario solo visible para técnicos")

    class Meta:
        verbose_name = 'Comentario'
        verbose_name_plural = 'Comentarios'
        ordering = ['fecha_creacion']

    def __str__(self):
        return f"Comentario de {self.usuario.username} en Ticket #{self.ticket.id}"