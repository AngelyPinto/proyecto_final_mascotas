import requests
from groq import Groq
from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from .models import Mascota

URL_MICROSERVICIO_CONSEJOS = 'https://microservicio-consejos-1.onrender.com/consejos'
URL_RESPALDO_CONSEJOS = settings.URL_RESPALDO_CONSEJOS


def lista_mascotas(request):
    mascotas = Mascota.objects.all()
    return render(request, 'mascotas/lista.html', {'mascotas': mascotas})


def detalle_mascota(request, mascota_id):
    mascota = get_object_or_404(Mascota, id=mascota_id)
    return render(request, 'mascotas/detalle.html', {'mascota': mascota})


def mascotas_por_estado(request, estado):
    mascotas = Mascota.objects.filter(estado__iexact=estado)
    return render(request, 'mascotas/por_estado.html', {
        'mascotas': mascotas,
        'estado': estado,
    })


def consejos_mascotas(request):
    try:
        respuesta = requests.get(URL_MICROSERVICIO_CONSEJOS, timeout=5)
        respuesta.raise_for_status()
        consejos = respuesta.json()
    except requests.exceptions.RequestException:
        try:
            respuesta = requests.get(URL_RESPALDO_CONSEJOS, timeout=5)
            respuesta.raise_for_status()
            consejos = respuesta.json()
        except requests.exceptions.RequestException:
            consejos = []

    return render(request, 'mascotas/consejos.html', {'consejos': consejos})


def preguntar_ia(request):
    respuesta_ia = None

    if request.method == 'POST':
        pregunta = request.POST.get('pregunta')

        mascotas = Mascota.objects.all()
        lista_mascotas_texto = ""
        for m in mascotas:
            lista_mascotas_texto += f"- {m.nombre}, especie: {m.especie}, color: {m.color}, estado: {m.estado}\n"

        if not lista_mascotas_texto:
            lista_mascotas_texto = "No hay mascotas registradas en este momento."

        cliente = Groq(api_key=settings.GROQ_API_KEY)

        prompt = f"""
        Eres un asistente experto en mascotas perdidas y encontradas.
        Responde de forma breve y clara, en texto plano,
        sin usar negrilla, asteriscos, ni ningun otro simbolo de formato.

        Esta es la lista actual de mascotas registradas en el sistema:
        {lista_mascotas_texto}

        Usa esa lista si la pregunta del usuario se refiere a mascotas especificas
        registradas en el sistema. Si la pregunta es general (consejos, cuidados,
        que hacer si se pierde una mascota), respondela normalmente sin necesidad
        de usar la lista.

        Pregunta del usuario:
        {pregunta}
        """

        respuesta = cliente.chat.completions.create(
            model='openai/gpt-oss-120b',
            messages=[{'role': 'user', 'content': prompt}],
        )

        respuesta_ia = respuesta.choices[0].message.content

    return render(request, 'mascotas/preguntar_ia.html', {'respuesta_ia': respuesta_ia})


def crear_mascota(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        especie = request.POST.get('especie')
        color = request.POST.get('color')
        descripcion = request.POST.get('descripcion')
        estado = request.POST.get('estado')

        Mascota.objects.create(
            nombre=nombre,
            especie=especie,
            color=color,
            descripcion=descripcion,
            estado=estado,
        )
        return redirect('mascotas:lista_mascotas')

    return render(request, 'mascotas/crear.html')


def editar_mascota(request, mascota_id):
    mascota = get_object_or_404(Mascota, id=mascota_id)

    if request.method == 'POST':
        mascota.nombre = request.POST.get('nombre')
        mascota.especie = request.POST.get('especie')
        mascota.color = request.POST.get('color')
        mascota.descripcion = request.POST.get('descripcion')
        mascota.estado = request.POST.get('estado')
        mascota.save()
        return redirect('mascotas:detalle_mascota', mascota_id=mascota.id)

    return render(request, 'mascotas/editar.html', {'mascota': mascota})


def eliminar_mascota(request, mascota_id):
    mascota = get_object_or_404(Mascota, id=mascota_id)
    mascota.delete()
    return redirect('mascotas:lista_mascotas')
