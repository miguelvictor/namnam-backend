from django.conf.urls import include, url
from django.contrib import admin

from app import viewsets

from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'recipes', viewsets.RecipeViewSet)
router.register(r'recipe-types', viewsets.RecipeTypeViewSet)
router.register(r'ingredients', viewsets.IngredientViewSet)
router.register(r'ingredient-types', viewsets.IngredientTypeViewSet)

urlpatterns = [
    url(r'^api/', include(router.urls)),
    url(r'^api-auth/', include('app.urls', namespace='app')),
    url(r'^api/auth/', include('rest_framework.urls',
        namespace='rest_framework')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^oauth/', include('oauth2_provider.urls',
        namespace='oauth2_provider')),
]
