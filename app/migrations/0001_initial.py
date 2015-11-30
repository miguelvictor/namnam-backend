# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='FacebookProfile',
            fields=[
                ('id', models.BigIntegerField(serialize=False, primary_key=True)),
                ('email', models.EmailField(max_length=254)),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='GoogleProfile',
            fields=[
                ('id', models.BigIntegerField(serialize=False, primary_key=True)),
                ('email', models.EmailField(max_length=254)),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('state', models.CharField(default=b'clean', max_length=255, choices=[(b'fb', b'From Facebook'), (b'google', b'From Google'), (b'clean', b'Native')])),
                ('user', models.OneToOneField(related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='googleprofile',
            name='profile',
            field=models.OneToOneField(related_name='google', to='app.UserProfile'),
        ),
        migrations.AddField(
            model_name='facebookprofile',
            name='profile',
            field=models.OneToOneField(related_name='facebook', to='app.UserProfile'),
        ),
    ]
