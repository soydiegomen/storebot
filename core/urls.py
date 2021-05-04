from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from django.urls import path, include, re_path
#from . import views
from .views import UsuarioActualView, CustomAuthToken,AdminsView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('token/', CustomAuthToken.as_view()),
    #User details
    path('me', UsuarioActualView.as_view()),
    #Create admin
    path('usuarios/admin/<str:secret>', AdminsView.as_view()),
]