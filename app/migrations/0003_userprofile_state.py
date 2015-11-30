# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_auto_20151129_1319'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='state',
            field=models.CharField(default=b'clean', max_length=255, choices=[(b'fb', b'From Facebook'), (b'google', b'From Google'), (b'clean', b'Native')]),
        ),
    ]
