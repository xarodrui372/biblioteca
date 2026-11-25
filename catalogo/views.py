from django.shortcuts import render, get_object_or_404
from .models import Autor, ModeloEditorial, ModeloLibro, Prestamo
from django.db.models import Avg, Count, Max, Min, Sum, Q, Prefetch
from django.db import transaction
from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.utils import timezone
# Create your views here.

def principal(request):
    consulta = ModeloLibro.objects.filter(Q(titulo__startswith="Django", paginas__lt=4) | Q(titulo__icontains="Python"))
    for libro in consulta:
        print(libro.titulo)
    print(f'Total libros: {ModeloLibro.objects.count()}')
    # print(f'Precio Medio: {ModeloLibro.objects.aggregate(precio_medio=Avg("precio"))}')
    # print(f'Precio Máximo: {ModeloLibro.objects.aggregate(precio_maximo=Max("precio"))}')
    # print(f'Precio Mínimo: {ModeloLibro.objects.aggregate(precio_minimo=Min("precio"))}')
    # print(f'Suma Precios: {ModeloLibro.objects.aggregate(suma_precios=Sum("precio"))}')
    resumen = ModeloLibro.objects.aggregate(
        precio_medio=Avg("precio"),
        precio_maximo=Max("precio"),
        precio_minimo=Min("precio"),
        suma_precios=Sum("precio"),
    )
    print(resumen)

    estadistica = ModeloLibro.objects.values("disponible").annotate(
        total=Count("id"),
        precio_medio=Avg("precio"),
    ).order_by("-disponible")

    for l in estadistica:
        print(l)
    return render(request, 'catalogo/principal.html')

def lista_editoriales(request):
    editoriales = ModeloEditorial.objects.annotate(total_libros=Count("libros"))
    return render(request, 'catalogo/editoriales.html', {'editoriales': editoriales})

def editorial(request, pk):
    editoriales = ModeloEditorial.objects.prefetch_related(
        Prefetch("libros", queryset=ModeloLibro.objects.filter(disponible=True), to_attr= "libros_disponibles")
    )
    editorial = get_object_or_404(editoriales, pk = pk)
    return render(request, 'catalogo/editorial.html', {'editorial': editorial})

def detalle_libro(request, pk):
    libro = get_object_or_404(ModeloLibro, pk = pk)
    libros = ModeloLibro.objects.select_related("editorial")
    for libro in libros:
        print(libro.titulo, libro.editorial.nombre if libro.editorial else "Sin Editorial")
    return render(request, 'catalogo/detalle_libro.html', {'libro': libro})

def autores(request, pk):
    autor = get_object_or_404(Autor, pk = pk)
    return render(request, 'catalogo/autores.html', {'autor': autor})

def libros(request):
    libros = ModeloLibro.objects.select_related("editorial").prefetch_related("autores")
    for libro in libros:
        libro.nom_editorial = libro.editorial.nombre if libro.editorial else "Sin editorial"
    return render(request, 'catalogo/libros.html' ,{'libros': libros})

def prestar_libro(request, pk_libro, pk_usuario):
    with transaction.atomic():
        libro = ModeloLibro.objects.select_for_update().get(pk=pk_libro)
        if not libro.disponible:
            raise ValueError("El libro no está disponible")

        usuario = get_user_model().objects.get(pk=pk_usuario)
        prestamo = Prestamo.objects.create(
            libro = libro,
            usuario = usuario,
        )
        libro.disponible = False
        libro.save(update_fields=["disponible"])
        return render(request, 'catalogo/prestamo_realizado.html', {'prestamo': prestamo})
    # HttpResponse("Préstamo realizado correctamente")

def devolver_libro(request, pk_prestamo):
    with transaction.atomic():
        prestamo = Prestamo.objects.select_for_update().get(pk=pk_prestamo)
        if prestamo.fecha_devolucion is not None:
            raise ValueError("El préstamo ya fué devuelto")

        prestamo.fecha_devolucion = timezone.now()
        prestamo.save(update_fields=["fecha_devolucion"])
        raise RuntimeError("Error simulado")
        prestamo.libro.disponible = True
        prestamo.libro.save(update_fields=["disponible"])
        return render(request, 'catalogo/libro_devuelto.html', {'prestamo': prestamo})