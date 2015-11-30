# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_auto_20151129_1331'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='facebook',
            field=models.OneToOneField(null=True, to='app.FacebookProfile'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='google',
            field=models.OneToOneField(null=True, to='app.GoogleProfile'),
        ),
    ]
