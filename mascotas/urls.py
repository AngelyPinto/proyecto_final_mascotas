from django.urls import path
from . import views

app_name = 'mascotas'

urlpatterns = [
    path('', views.lista_mascotas, name='lista_mascotas'),
    path('mascotas/<int:mascota_id>/', views.detalle_mascota, name='detalle_mascota'),
    path('mascotas/estado/<str:estado>/', views.mascotas_por_estado, name='mascotas_por_estado'),
    path('consejos/', views.consejos_mascotas, name='consejos_mascotas'),
    path('preguntar-ia/', views.preguntar_ia, name='preguntar_ia'),
    path('crear/', views.crear_mascota, name='crear_mascota'),
    path('editar/<int:mascota_id>/', views.editar_mascota, name='editar_mascota'),
    path('eliminar/<int:mascota_id>/', views.eliminar_mascota, name='eliminar_mascota'),
]
