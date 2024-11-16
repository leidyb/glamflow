from django.db import models
from django.utils.translation import gettext_lazy as _

class Opinion(models.Model):
    cliente = models.ForeignKey(
        'usuarios.Usuario', 
        on_delete=models.CASCADE,
        related_name='opiniones',
        limit_choices_to={'tipo_usuario': 'Cliente'},
        verbose_name="Cliente"
    )
    servicio = models.ForeignKey(
        'servicios.Servicio',
        on_delete=models.CASCADE,
        related_name='opiniones',
        verbose_name="Servicio"
    )
    calificacion = models.PositiveSmallIntegerField(
        verbose_name="Calificación",
        help_text="Calificación de 1 a 5 estrellas",
        choices=[(1, '1 Estrella'), (2, '2 Estrellas'), (3, '3 Estrellas'), (4, '4 Estrellas'), (5, '5 Estrellas')]
    )
    comentario = models.TextField(verbose_name="Comentario", blank=True, null=True)
    fecha_opinion = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Opinión")
    estado = models.BooleanField(default=True, verbose_name="Visible")

    class Meta:
        verbose_name_plural = "Opiniones"
        ordering = ['-fecha_opinion']

    def __str__(self):
        return f"Opinión de {self.cliente.full_name} sobre {self.servicio.nombre_servicio}"

    def ocultar(self):
        """Oculta la opinión para que no sea visible en el sistema."""
        self.estado = False
        self.save()

    def activar(self):
        """Activa la opinión para que sea visible en el sistema."""
        self.estado = True
        self.save()

    @property
    def es_visible(self):
        return self.estado
