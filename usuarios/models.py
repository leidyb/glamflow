from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User

def get_image_filename(instance, filename):
    ext = filename.split('.')[-1]
    filename = f"{instance.documento}.{ext}"
    return f"comunidad/usuarios/{filename}"
# Create your models here.
class Usuario(models.Model):
    primer_nombre = models.CharField(max_length=45, verbose_name="Primer Nombre")
    segundo_nombre = models.CharField(max_length=45, verbose_name="Segundo Nombre", blank=True, null=True)
    primer_apellido = models.CharField(max_length=45, verbose_name="Primer Apellido")
    segundo_apellido = models.CharField(max_length=45, verbose_name="Segundo Apellido")
    fecha_nacimiento = models.DateField(verbose_name="Fecha de Nacimiento")
    imagen = models.ImageField(upload_to=get_image_filename, blank=True, null=True, default="comunidad/default-user.jpeg")
    correo = models.EmailField(max_length=50, verbose_name="Correo", unique=True)
    
    class TipoDocumento(models.TextChoices):
        CEDULA = 'CC', _("Cédula")
        TARJETA = 'TI', _("Tarjeta de Identidad")
        CEDULA_EXTRANJERIA = 'CE', _("Cédula de Extranjería")
    tipo_documento = models.CharField(max_length=2, choices=TipoDocumento.choices, verbose_name="Tipo de Documento")
    documento = models.PositiveIntegerField(verbose_name="Documento", unique=True)
    
    class TipoUsuario(models.TextChoices):
        CLIENTE = 'Cliente', _("Cliente")
        EMPRENDEDORA = 'Emprendedora', _("Emprendedora")
        ADMINISTRADOR = 'Administrador', _("Administrador")
    tipo_usuario = models.CharField(max_length=15, choices=TipoUsuario.choices, verbose_name="Tipo de Usuario", default=TipoUsuario.CLIENTE)
    
    telefono = models.CharField(max_length=15, verbose_name="Teléfono", blank=True, null=True)
    direccion = models.CharField(max_length=255, verbose_name="Dirección", blank=True, null=True)
    fecha_registro = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Registro")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    estado = models.BooleanField(default=True)

    def clean(self):
        self.primer_nombre = self.primer_nombre.title()

    def __str__(self):
        return f"{self.primer_nombre} {self.primer_apellido}"

    @property
    def full_name(self):
        if self.segundo_nombre:
            return f"{self.primer_nombre} {self.segundo_nombre} {self.primer_apellido} {self.segundo_apellido}"
        else:
            return f"{self.primer_nombre} {self.primer_apellido} {self.segundo_apellido}"

    def usuario_activo(self):
        return self.estado

    def desactivar_usuario(self):
        self.estado = False
        self.save()

    class Meta:
        verbose_name_plural = "Usuarios"
