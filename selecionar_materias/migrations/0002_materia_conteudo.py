# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-06-10 23:05
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('selecionar_materias', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='materia',
            name='conteudo',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
    ]
