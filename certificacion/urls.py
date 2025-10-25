from django.urls import path
from . import views

urlpatterns = [
    path('nueva/', views.crear_orden, name='crear_orden'),
    path('<int:orden_id>/item/nuevo/', views.crear_item, name='crear_item'),
]
