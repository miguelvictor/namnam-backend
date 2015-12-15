# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='facebookprofile',
            name='id',
            field=models.CharField(max_length=255, serialize=False, primary_key=True),
        ),
        migrations.AlterField(
            model_name='googleprofile',
            name='id',
            field=models.CharField(max_length=255, serialize=False, primary_key=True),
        ),
    ]
