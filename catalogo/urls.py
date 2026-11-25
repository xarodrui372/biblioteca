from django.urls import path
from . import views

urlpatterns = [
    path('', views.principal, name='principal'),
    path('editoriales', views.lista_editoriales, name='editoriales'),
    path('editorial/<int:pk>', views.editorial, name='editorial'),
    path('detalle_libro/<int:pk>', views.detalle_libro, name='detalle_libro'),
    path('autores/<int:pk>', views.autores, name='autores'),
    path('libros', views.libros, name='libros'),
    path('prestamo/<int:pk_libro>/<int:pk_usuario>', views.prestar_libro, name='prestamo'),
    path('devolverLibro/<int:pk_prestamo>', views.devolver_libro, name="devolver_libro"),
]
