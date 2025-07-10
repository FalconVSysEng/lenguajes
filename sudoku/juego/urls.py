from django.contrib import admin
from django.urls import path, include
from juego import views

urlpatterns = [
    path('',views.menu, name='menu'),
    path('resolver/',views.sudoku, name='sudoku')
]