from django.db import migrations


def crear_mascotas_ejemplo(apps, schema_editor):
    Mascota = apps.get_model('mascotas', 'Mascota')
    Mascota.objects.create(
        nombre='Toby', especie='Perro', color='Cafe',
        descripcion='Perro pequeño, orejas caidas, collar rojo.',
        estado='perdida',
    )
    Mascota.objects.create(
        nombre='Michi', especie='Gato', color='Negro',
        descripcion='Gato negro con una mancha blanca en el pecho.',
        estado='perdida',
    )
    Mascota.objects.create(
        nombre='Luna', especie='Perro', color='Blanco',
        descripcion='Perra mediana, muy juguetona, sin collar.',
        estado='encontrada',
    )


def eliminar_mascotas_ejemplo(apps, schema_editor):
    Mascota = apps.get_model('mascotas', 'Mascota')
    Mascota.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ('mascotas', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(crear_mascotas_ejemplo, eliminar_mascotas_ejemplo),
    ]
