from django.contrib import admin
from django.urls import path
from certificacion.views import crear_orden

urlpatterns = [
    path('admin/', admin.site.urls),
    path('orden/nueva/', crear_orden, name='crear_orden'),
]
