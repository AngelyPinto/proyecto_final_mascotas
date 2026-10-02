from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='Mascota',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('especie', models.CharField(max_length=50)),
                ('color', models.CharField(max_length=50)),
                ('descripcion', models.TextField()),
                ('estado', models.CharField(choices=[('perdida', 'Perdida'), ('encontrada', 'Encontrada')], default='perdida', max_length=20)),
            ],
        ),
    ]
