# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-15 04:09
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('archive', '0003_auto_20171115_0353'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clip',
            name='memento',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='old_memento', to='archive.Memento'),
        ),
    ]
