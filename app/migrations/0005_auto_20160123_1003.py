# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_auto_20151222_0710'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='activated',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='activationKey',
            field=models.CharField(max_length=5, blank=True),
        ),
    ]
