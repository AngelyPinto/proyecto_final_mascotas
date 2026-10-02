import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('mascotas', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Avistamiento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre_persona', models.CharField(max_length=100)),
                ('lugar', models.CharField(max_length=150)),
                ('fecha_avistamiento', models.DateField(auto_now_add=True)),
                ('mascota', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mascotas.mascota')),
            ],
        ),
    ]
