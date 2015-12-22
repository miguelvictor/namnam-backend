from django.contrib.auth.models import User
from django.db.models import Avg

from app import models

from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'email',
                  'first_name', 'last_name')
        read_only_fields = 'id',
        extra_kwargs = {'password': {'write_only': True}}


class UnitOfMeasureSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.UnitOfMeasure
        fields = ('pk', 'name')


class StepSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Step
        fields = ('sequence', 'instruction')


class IngredientSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Ingredient
        fields = ('pk', 'banner', 'icon', 'name', 'description')


class IngredientTypeSerializer(serializers.HyperlinkedModelSerializer):
    ingredients = IngredientSerializer(many=True, read_only=True)

    class Meta:
        model = models.IngredientType
        fields = ('pk', 'name', 'picture', 'ingredients')


class RecipeComponentSerializer(serializers.ModelSerializer):
    ingredient = IngredientSerializer(many=False, read_only=True)
    unit_of_measure = UnitOfMeasureSerializer(many=False, read_only=True)

    class Meta:
        model = models.RecipeComponent
        fields = ('quantity', 'adjective', 'unit_of_measure',
                  'ingredient', 'extra')


class RecipeOverviewSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Recipe
        fields = ('pk', 'url', 'name', 'description', 'banner', 'icon')


class RecipeTypeSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = models.RecipeType
        fields = ('pk', 'name', 'picture')


class RecipeSerializer(serializers.HyperlinkedModelSerializer):
    categories = RecipeTypeSerializer(many=True, read_only=True)
    recipe_components = RecipeComponentSerializer(many=True, read_only=True)
    steps = StepSerializer(many=True, read_only=True)
    rating = serializers.SerializerMethodField()
    reviews = serializers.SerializerMethodField()

    class Meta:
        model = models.Recipe
        fields = ('pk', 'name', 'rating', 'reviews', 'description', 'banner',
                  'icon', 'time_to_complete', 'default_serving_size',
                  'categories', 'recipe_components', 'steps')

    def get_rating(self, obj):
        ratings = models.Rating.objects.filter(recipe=obj)
        return ratings.aggregate(Avg('rating'))['rating__avg']

    def get_reviews(self, obj):
        return len(models.Rating.objects.filter(recipe=obj))
