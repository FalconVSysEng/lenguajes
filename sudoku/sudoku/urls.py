from django.contrib import admin
from django.urls import path, include
import juego

urlpatterns = [
    path('admin/', admin.site.urls),
    path('juego/',include('juego.urls'))
]
