# Generated by Django 2.2.5 on 2020-01-22 15:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_auto_20200121_1827'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='jugador',
            name='lesionado',
        ),
        migrations.RemoveField(
            model_name='jugador',
            name='posicion',
        ),
    ]
