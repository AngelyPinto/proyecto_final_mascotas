from django.urls import path
from . import views

app_name = 'avistamientos'

urlpatterns = [
    path('', views.lista_avistamientos, name='lista_avistamientos'),
    path('reportar/<int:mascota_id>/', views.reportar_avistamiento, name='reportar_avistamiento'),
    path('eliminar/<int:avistamiento_id>/', views.eliminar_avistamiento, name='eliminar_avistamiento'),
]
