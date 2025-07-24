from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_cursos, name='lista_cursos'),
    path('crear/', views.crear_curso, name='crear_curso'),
    path('editar/<int:id>/', views.editar_curso, name='editar_curso'),
    path('eliminar/<int:id>/', views.eliminar_curso, name='eliminar_curso'),
]
