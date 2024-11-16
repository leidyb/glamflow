from django.shortcuts import redirect, render

from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required

from django.db.models import Count,Q
def principal(request):
    titulo="Bienvenido"
 
    context={
        "titulo": titulo,
       
    }
    return render(request, "index.html", context)

def principal_admin(request):
    titulo = "Bienvenido"
    
    # # Obtener las cantidades correctas
    # usuarios = Usuario.objects.all().count()
    # tiendas = Tienda.objects.all().count()  
    # productos = Producto.objects.all().count() 
    # pedidos = Pedido.objects.all().count()  

    # # Obtener nombres de tiendas y cantidad de productos por tienda
    # tiendas_con_productos = Tienda.objects.annotate(cantidad_productos=Count('producto', filter=Q(producto__estado=True))).values('nombre', 'cantidad_productos')
    
    
    # usuarios_obj = Usuario.objects.all()

    context = {
        # "titulo": titulo,
        # "usuarios_cantidad": usuarios,
        # "tiendas_cantidad": tiendas,
        # "productos_cantidad": productos,
        # "pedidos_cantidad": pedidos,
        # "usuarios_obj": usuarios_obj,
        # "tiendas_con_productos": tiendas_con_productos
    }

    return render(request, "index-admin.html", context)


def logout_user(request):
    logout(request)
    return redirect('index')