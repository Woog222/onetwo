from django.urls import path
from . import views

urlpatterns = [
    path('hello/', views.hello, name='hello'),
    # path('which-day/', views.which_day, name='which-day'),
    path('weather/', views.weather, name='weather'),
]