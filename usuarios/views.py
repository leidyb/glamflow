from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import Group
from usuarios.forms import *
from usuarios.models import Usuario
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from PIL import Image
from django.contrib.auth.models import User
from django.contrib.auth.decorators import permission_required
# Create your views here.
def usuario_crear(request):
    titulo = "Usuario"
    accion = "Agregar"
    usuarios = Usuario.objects.all()

    if request.method == "POST":
        form = UsuarioForm(request.POST, request.FILES)
        if form.is_valid():
            documento = request.POST['documento']
            primer_nombre = request.POST['primer_nombre']
            primer_apellido = request.POST['primer_apellido']

            # Crear o recuperar el usuario en el modelo User
            user, created = User.objects.get_or_create(username=documento, defaults={
                'first_name': primer_nombre,
                'last_name': primer_apellido,
                'email': request.POST['correo'],
                'password': make_password(f"@{primer_nombre[0]}{primer_apellido[0]}{documento[-4:]}")
            })

            if not created:  # Si el usuario ya existe
                user.first_name = primer_nombre
                user.last_name = primer_apellido
                user.email = request.POST['correo']
                user.save()

            # Asociar rol
            rol_id = request.POST.get('rol')
            if rol_id:
                rol = Group.objects.get(id=rol_id)
                user.groups.add(rol)

            # Crear el registro en el modelo Usuario
            usuario = Usuario.objects.create(
                primer_nombre=primer_nombre,
                segundo_nombre=request.POST.get('segundo_nombre', ''),
                primer_apellido=primer_apellido,
                segundo_apellido=request.POST['segundo_apellido'],
                fecha_nacimiento=request.POST['fecha_nacimiento'],
                imagen=request.FILES.get('imagen'),
                correo=request.POST['correo'],
                tipo_documento=request.POST['tipo_documento'],
                documento=documento,
                user=user,
            )

            # Redimensionar imagen
            if usuario.imagen:
                try:
                    img = Image.open(usuario.imagen.path)
                    img = img.resize((500, 500))
                    img.save(usuario.imagen.path)
                except Exception as e:
                    messages.error(request, f"Error al procesar la imagen: {str(e)}")

            messages.success(request, "¡El Usuario se agregó de forma exitosa!")
            return redirect('usuarios')
        else:
            messages.error(request, "¡Error al agregar al Usuario!")
    else:
        form = UsuarioForm()

    context = {
        "titulo": titulo,
        "usuarios": usuarios,
        "form": form,
        "accion": accion
    }
    return render(request, "usuarios/usuario.html", context)


def usuario_editar(request, pk):
    usuario = Usuario.objects.get(id=pk)
    usuarios = Usuario.objects.all()
    accion = "Editar"
    nombre = f"{usuario.primer_nombre} {usuario.primer_apellido}"
    titulo = f"Usuario {nombre}"

    if request.method == "POST":
        form = UsuarioEditarForm(request.POST, request.FILES, instance=usuario)
        if form.is_valid():
            usuario = form.save()

            # Actualizar grupo del usuario en el modelo User
            rol_id = request.POST.get('rol')
            if rol_id:
                rol = Group.objects.get(id=rol_id)
                usuario.user.groups.set([rol])

            # Redimensionar imagen
            if usuario.imagen:
                try:
                    img = Image.open(usuario.imagen.path)
                    img = img.resize((500, 500))
                    img.save(usuario.imagen.path)
                except Exception as e:
                    messages.error(request, f"Error al procesar la imagen: {str(e)}")

            messages.success(request, f"¡{nombre} se editó de forma exitosa!")
            return redirect("usuarios")
        else:
            messages.error(request, f"¡Error al editar a {nombre}!")
    else:
        form = UsuarioEditarForm(instance=usuario)

    context = {
        "titulo": titulo,
        "usuarios": usuarios,
        "form": form,
        "accion": accion
    }
    return render(request, "usuarios/usuario.html", context)


def usuario_eliminar(request, pk):
    usuario = Usuario.objects.filter(id=pk)
    if usuario.exists():
        usuario.update(estado=False)  # Cambiar el estado a inactivo
        messages.success(request, "¡El usuario se eliminó correctamente!")
    else:
        messages.error(request, "¡El usuario no existe o ya fue eliminado!")
    return redirect('usuarios')

def edit_group(request, group_id=None):
    groups = Group.objects.all()
    if group_id:
        group = get_object_or_404(Group, id=group_id)
    else:
        group = None

    if request.method == 'POST':
        form = GroupForm(request.POST, instance=group)
        if form.is_valid():
            form.save()
            return redirect('edit_group',group_id)  # Cambia 'list_groups' por el nombre de la URL donde se listan los grupos
    else:
        form = GroupForm(instance=group)
    context={
    'groups':groups,
    'group': group,
    'form': form
    }
    return render(request, 'usuarios/grupos.html', context)