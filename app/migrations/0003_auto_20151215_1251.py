# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app', '0002_auto_20151215_0254'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ingredient',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('banner', models.URLField()),
                ('description', models.TextField()),
                ('icon', models.URLField()),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='IngredientType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('picture', models.URLField()),
            ],
        ),
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('rating', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Recipe',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('icon', models.URLField()),
                ('banner', models.URLField()),
                ('default_serving_size', models.IntegerField()),
                ('time_to_complete', models.FloatField()),
            ],
            options={
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='RecipeComponent',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('quantity', models.FloatField()),
                ('adjective', models.CharField(max_length=255, blank=True)),
                ('extra', models.CharField(max_length=255, blank=True)),
                ('ingredient', models.ForeignKey(to='app.Ingredient')),
                ('recipe', models.ForeignKey(related_name='recipe_components', to='app.Recipe')),
            ],
        ),
        migrations.CreateModel(
            name='RecipeType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('picture', models.URLField()),
            ],
        ),
        migrations.CreateModel(
            name='Step',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('sequence', models.IntegerField(default=1)),
                ('instruction', models.TextField()),
                ('recipe', models.ForeignKey(related_name='steps', to='app.Recipe')),
            ],
            options={
                'ordering': ['sequence'],
            },
        ),
        migrations.CreateModel(
            name='UnitOfMeasure',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.AddField(
            model_name='recipecomponent',
            name='unit_of_measure',
            field=models.ForeignKey(to='app.UnitOfMeasure'),
        ),
        migrations.AddField(
            model_name='recipe',
            name='categories',
            field=models.ManyToManyField(related_name='recipes', to='app.RecipeType'),
        ),
        migrations.AddField(
            model_name='rating',
            name='recipe',
            field=models.ForeignKey(related_name='ratings', to='app.Recipe'),
        ),
        migrations.AddField(
            model_name='rating',
            name='who',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='ingredient',
            name='type',
            field=models.ForeignKey(related_name='ingredients', to='app.IngredientType'),
        ),
    ]
