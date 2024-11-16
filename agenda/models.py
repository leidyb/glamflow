from django.db import models

# Create your models here.
from django.db import models
from django.utils.translation import gettext_lazy as _

class Agenda(models.Model):
    class EstadoCita(models.TextChoices):
        PENDIENTE = 'Pendiente', _("Pendiente")
        CONFIRMADA = 'Confirmada', _("Confirmada")
        CANCELADA = 'Cancelada', _("Cancelada")
        COMPLETADA = 'Completada', _("Completada")
    
    cliente = models.ForeignKey(
        'usuarios.Usuario', 
        on_delete=models.CASCADE, 
        related_name='citas_cliente',
        limit_choices_to={'tipo_usuario': 'Cliente'},
        verbose_name="Cliente"
    )
    emprendedora = models.ForeignKey(
        'usuarios.Usuario', 
        on_delete=models.CASCADE, 
        related_name='citas_emprendedora',
        limit_choices_to={'tipo_usuario': 'Emprendedora'},
        verbose_name="Emprendedora"
    )
    servicio = models.ForeignKey(
        'servicios.Servicio', 
        on_delete=models.CASCADE, 
        related_name='citas_servicio',
        verbose_name="Servicio"
    )
    fecha_hora = models.DateTimeField(verbose_name="Fecha y Hora")
    estado = models.CharField(
        max_length=15, 
        choices=EstadoCita.choices, 
        default=EstadoCita.PENDIENTE,
        verbose_name="Estado de la Cita"
    )
    comentarios_cliente = models.TextField(
        verbose_name="Comentarios del Cliente", 
        blank=True, 
        null=True
    )
    comentarios_emprendedora = models.TextField(
        verbose_name="Comentarios de la Emprendedora", 
        blank=True, 
        null=True
    )
    fecha_creacion = models.DateTimeField(
        auto_now_add=True, 
        verbose_name="Fecha de Creación"
    )

    class Meta:
        verbose_name_plural = "Citas"
        ordering = ['-fecha_hora']

    def __str__(self):
        return f"Cita de {self.cliente} con {self.emprendedora} - {self.servicio.nombre_servicio}"

    @property
    def es_pendiente(self):
        return self.estado == self.EstadoCita.PENDIENTE

    @property
    def es_completada(self):
        return self.estado == self.EstadoCita.COMPLETADA

    def cancelar(self):
        if self.estado in [self.EstadoCita.PENDIENTE, self.EstadoCita.CONFIRMADA]:
            self.estado = self.EstadoCita.CANCELADA
            self.save()

    def confirmar(self):
        if self.estado == self.EstadoCita.PENDIENTE:
            self.estado = self.EstadoCita.CONFIRMADA
            self.save()
