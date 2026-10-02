from django.shortcuts import render, redirect, get_object_or_404
from mascotas.models import Mascota
from .models import Avistamiento


def lista_avistamientos(request):
    avistamientos = Avistamiento.objects.all()
    return render(request, 'avistamientos/lista.html', {'avistamientos': avistamientos})


def reportar_avistamiento(request, mascota_id):
    mascota = get_object_or_404(Mascota, id=mascota_id)

    if request.method == 'POST':
        nombre_persona = request.POST.get('nombre_persona')
        lugar = request.POST.get('lugar')
        Avistamiento.objects.create(mascota=mascota, nombre_persona=nombre_persona, lugar=lugar)
        mascota.estado = 'encontrada'
        mascota.save()
        return redirect('avistamientos:lista_avistamientos')

    return render(request, 'avistamientos/reportar.html', {'mascota': mascota})


def eliminar_avistamiento(request, avistamiento_id):
    avistamiento = get_object_or_404(Avistamiento, id=avistamiento_id)
    mascota = avistamiento.mascota
    mascota.estado = 'perdida'
    mascota.save()
    avistamiento.delete()
    return redirect('avistamientos:lista_avistamientos')
