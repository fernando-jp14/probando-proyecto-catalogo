from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Curso
from .forms import CursoForm

def lista_cursos(request):
    cursos = Curso.objects.all()
    return render(request, 'catalogo/lista_cursos.html', {'cursos': cursos})

def crear_curso(request):
    if request.method == 'POST':
        form = CursoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, '✅ Curso creado correctamente.')
            return redirect('lista_cursos')
        else:
            messages.error(request, '❌ Corrige los errores del formulario.')
    else:
        form = CursoForm()
    return render(request, 'catalogo/crear_curso.html', {'form': form})

def editar_curso(request, id):
    curso = get_object_or_404(Curso, id=id)
    if request.method == 'POST':
        form = CursoForm(request.POST, instance=curso)  # <- AQUÍ ES CLAVE
        if form.is_valid():
            form.save()
            messages.success(request, '✅ Curso actualizado correctamente.')
            return redirect('lista_cursos')
        else:
            messages.error(request, '❌ Corrige los errores del formulario.')
    else:
        form = CursoForm(instance=curso)  # <- TAMBIÉN AQUÍ
    return render(request, 'catalogo/editar_curso.html', {'form': form})

def eliminar_curso(request, id):
    curso = get_object_or_404(Curso, id=id)
    curso.delete()
    messages.warning(request, f'🗑️ Curso eliminado: {curso.curso}')
    return redirect('lista_cursos')
