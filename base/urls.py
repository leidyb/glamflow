"""
URL configuration for base project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path

from base import settings
from base.views import *
from django.conf.urls.static import static

from django.contrib.auth import views as auth_views

urlpatterns = [
    
    path('login/',auth_views.LoginView.as_view(),name='login'),
    path('logout/',logout_user,name="logout"),
    
    path('admin/', admin.site.urls),
    path('',principal,name="index"),
    # The line `path('adm/', principal_admin, name="index-admin")` in the URL configuration is
    # defining a URL pattern that maps requests with the path 'adm/' to a view function named
    # `principal_admin`. The `name="index-admin"` is assigning a unique name to this URL pattern which
    # can be used to refer to it in the Django templates or code to generate URLs.
    path('adm/',principal_admin,name="index-admin"),
    path('agenda/',include('agenda.urls')),
    path('opiniones/',include('opiniones.urls')),
    path('servicios/',include('servicios.urls')),
    path('usuarios/',include('usuarios.urls')), 
    
    path('reiniciar/',auth_views.PasswordResetView.as_view(),name='pass_reset'),
    path('reiniciar/enviar',auth_views.PasswordResetDoneView.as_view(),name='pass_reset_done'),
    path('reiniciar/<uid64>/<token>',auth_views.PasswordResetConfirmView.as_view(),name='pass_reset_confirm'),
    path('reiniciar/completo',auth_views.PasswordResetCompleteView.as_view(),name='pass_reset_reset_complete'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
