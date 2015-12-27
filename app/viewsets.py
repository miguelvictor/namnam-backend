from django.db.models import Avg
from django.http import JsonResponse

from app import models, serializers
from app.core import HeaderBasedPagination
from app.serializers import RecipeSerializer
from app.utils import normalize_recipe_params

from rest_framework import viewsets, filters
from rest_framework.decorators import (detail_route,
                                       list_route, permission_classes)
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

import json


class RecipeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.Recipe.objects.all()
    serializer_class = serializers.RecipeSerializer
    pagination_class = HeaderBasedPagination
    filter_backends = filters.SearchFilter, filters.OrderingFilter
    search_fields = 'name',
    ordering = 'name',

    @detail_route(methods=['post'])
    @permission_classes((IsAuthenticated, ))
    def rate(self, request, pk=None):
        rating = request.data.get('rating', None)

        try:
            rating = int(rating)

            try:
                recipe = models.Recipe.objects.get(pk=pk)
                models.Rating.objects.update_or_create(
                    recipe=recipe, who=request.user,
                    defaults={'rating': rating})

                recipe_ratings = models.Rating.objects.filter(recipe=recipe)
                recipe_avg_rating = recipe_ratings.aggregate(
                    Avg('rating'))['rating__avg']
                recipe_rating_num = len(recipe_ratings)

                return JsonResponse({
                        'average_rating': recipe_avg_rating,
                        'number_of_ratings': recipe_rating_num,
                    })
            except models.Recipe.DoesNotExist:
                return Response('Recipe not found', status=404)
        except ValueError:
            return Response('Rating must be an integer', status=400)

    @list_route()
    def recommend_old(self, request):
        params = set(normalize_recipe_params(request.GET.get('q', None)))

        exact_recipes = []
        nearly_there_recipes = []

        for recipe in models.Recipe.objects.all():
            ingredients = set([x.ingredient.id
                               for x in recipe.recipe_components.all()])

            intersection = params & ingredients

            if len(intersection) > 0:

                difference = ingredients - intersection
                difference_length = len(difference)

                if difference_length is 0:
                    exact_recipes.append(recipe)
                else:
                    nearly_there_recipes.append({
                        'recipe': RecipeSerializer(recipe, many=False).data,
                        'missing_count': difference_length,
                    })

        nearly_there_recipes.sort(key=lambda x: x['missing_count'])

        return JsonResponse({
            'recipes': RecipeSerializer(exact_recipes, many=True).data,
            'nearly_there': json.JSONDecoder().decode(
                json.dumps(nearly_there_recipes)),
        })

    @list_route()
    def recommend(self, request):
        params = set(normalize_recipe_params(request.GET.get('q', None)))

        exact_recipes = []
        nearly_there_recipes = []

        for recipe in models.Recipe.objects.all():
            ingredients = set([x.ingredient.id
                               for x in recipe.recipe_components.all()])

            intersection = params & ingredients

            if len(intersection) > 0:

                difference = ingredients - intersection

                if len(difference) is 0:
                    exact_recipes.append(recipe)
                else:
                    nearly_there_recipes.append({
                        'recipe': recipe.pk,
                        'missing': difference,
                    })

        nearly_there_recipes.sort(key=lambda x: len(x['missing']))

        return JsonResponse({
            'recipes': [recipe.pk for recipe in exact_recipes],
            'nearly_there': nearly_there_recipes
        })


class RecipeTypeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.RecipeType.objects.all()
    serializer_class = serializers.RecipeTypeSerializer
    pagination_class = HeaderBasedPagination
    ordering = 'name',


class IngredientTypeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.IngredientType.objects.all()
    serializer_class = serializers.IngredientTypeSerializer
    pagination_class = HeaderBasedPagination
    ordering = 'name',


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.Ingredient.objects.all()
    serializer_class = serializers.IngredientSerializer
    pagination_class = HeaderBasedPagination
    filter_backends = filters.SearchFilter, filters.OrderingFilter
    search_fields = 'name',
    ordering = 'name',
