# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-07-12 16:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home_application', '0003_auto_20190710_1628'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='code_name',
            field=models.CharField(default='', max_length=200),
            preserve_default=False,
        ),
    ]
