# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import app.models


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
            name='activation_key',
            field=models.CharField(default=app.models.generate_slug_profile, max_length=5, blank=True),
        ),
    ]
