from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
import juego

urlpatterns = [
    path('admin/', admin.site.urls),
    path('juego/',include('juego.urls')),
    path('', lambda request: redirect('juego/', permanent=False)),
]
