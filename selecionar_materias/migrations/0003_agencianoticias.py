# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-06-10 23:33
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('selecionar_materias', '0002_materia_conteudo'),
    ]

    operations = [
        migrations.CreateModel(
            name='AgenciaNoticias',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=90)),
                ('conteudo', models.CharField(blank=True, max_length=500, null=True)),
            ],
        ),
    ]