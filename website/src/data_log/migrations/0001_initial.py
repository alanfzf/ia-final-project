# Generated by Django 4.2.1 on 2023-06-04 02:05

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Tarjeta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_tarjeta', models.CharField(max_length=255, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Registro',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('persona_predecida', models.CharField(max_length=255)),
                ('confianza', models.DecimalField(decimal_places=4, default=0.0, max_digits=4, verbose_name='Nivel de confianza')),
                ('captura', models.ImageField(blank=True, null=True, upload_to='uploads/')),
                ('fecha', models.DateField(default=datetime.datetime.now)),
                ('tarjeta', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='data_log.tarjeta')),
            ],
        ),
    ]