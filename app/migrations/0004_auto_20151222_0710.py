# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_auto_20151215_1251'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='time_to_complete',
            field=models.IntegerField(),
        ),
    ]
