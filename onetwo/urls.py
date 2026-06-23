from django.urls import path
from . import views

urlpatterns = [
    path('hello/', views.hello, name='hello'),
    path('enchant-team/', views.enchant_team, name='enchant-team'),
    path('which-day/', views.which_day, name='which-day'),
    path('weather/', views.weather, name='weather'),
    path('calculate/', views.calculate, name='calculate'),
    path('seat-arrangement/', views.seat_arrangement, name='seat-arrangement'),
]