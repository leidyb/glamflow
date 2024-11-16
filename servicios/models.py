from django.db import models
from django.utils.translation import gettext_lazy as _

class Servicio(models.Model):
    emprendedora = models.ForeignKey(
        'usuarios.Usuario', 
        on_delete=models.CASCADE, 
        related_name='servicios',
        limit_choices_to={'tipo_usuario': 'Emprendedora'},
        verbose_name="Emprendedora"
    )
    nombre_servicio = models.CharField(max_length=100, verbose_name="Nombre del Servicio")
    descripcion = models.TextField(verbose_name="Descripción del Servicio", blank=True, null=True)
    duracion = models.PositiveIntegerField(verbose_name="Duración (minutos)", help_text="Duración aproximada en minutos.")
    precio = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Precio")
    disponible = models.BooleanField(default=True, verbose_name="Disponible")
    fecha_creacion = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Creación")
    fecha_actualizacion = models.DateTimeField(auto_now=True, verbose_name="Última Actualización")

    class Meta:
        verbose_name_plural = "Servicios"
        ordering = ['nombre_servicio']

    def __str__(self):
        return f"{self.nombre_servicio} - {self.emprendedora.full_name}"

    def desactivar(self):
        """Desactiva el servicio, marcándolo como no disponible."""
        self.disponible = False
        self.save()

    def activar(self):
        """Activa el servicio, marcándolo como disponible."""
        self.disponible = True
        self.save()

    @property
    def es_disponible(self):
        return self.disponible
