# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_auto_20151129_1351'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='facebook',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='google',
        ),
        migrations.AddField(
            model_name='facebookprofile',
            name='profile',
            field=models.OneToOneField(related_name='facebook', default=1, to='app.UserProfile'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='googleprofile',
            name='profile',
            field=models.OneToOneField(related_name='google', default=1, to='app.UserProfile'),
            preserve_default=False,
        ),
    ]
