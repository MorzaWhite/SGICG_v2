from django.urls import path
from . import views

urlpatterns = [
    path('nueva/', views.crear_orden, name='crear_orden'),
    path('<int:orden_id>/item/nuevo/', views.crear_item, name='crear_item'),

    # API endpoints for items
    path('api/orden/<int:orden_id>/items', views.item_api_view, name='item_api_list_create'),
    path('api/orden/<int:orden_id>/item/<int:item_id>', views.item_api_view, name='item_api_update'),
]
