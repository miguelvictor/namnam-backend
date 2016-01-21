from django.contrib import admin

from app import models


class FacebookProfileInline(admin.StackedInline):
    verbose_name_plural = 'Facebook Profile'
    model = models.FacebookProfile
    extra = 0


class GoogleProfileInline(admin.StackedInline):
    verbose_name_plural = 'Google Profile'
    model = models.GoogleProfile
    extra = 0


class UserProfileAdmin(admin.ModelAdmin):
    inlines = (FacebookProfileInline, GoogleProfileInline)


class StepInline(admin.TabularInline):
    model = models.Step
    extra = 0


class RecipeInline(admin.TabularInline):
    model = models.RecipeComponent


class RecipeAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': [
            'name', 'categories', 'description',
            'default_serving_size', 'time_to_complete',
        ]}),
        ('More Information', {'fields': ['banner', 'icon']}),
    ]

    inlines = (RecipeInline, StepInline)
    search_fields = 'name', 'description'
    list_filter = 'categories',
    list_per_page = 10


class IngredientAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['name', 'type', 'description']}),
        ('More Information', {'fields': ['banner', 'icon']}),
    ]

    search_fields = 'name', 'description'
    list_filter = 'type',
    list_per_page = 10


class RatingAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['recipe', 'rating', 'who']})
    ]

    search_fields = 'recipe', 'rating', 'who'
    list_filter = 'recipe', 'rating', 'who'
    list_display = ('recipe', 'rating', 'who')
    list_per_page = 10


class RecipeTypeAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['name', 'picture']})
    ]

    list_display = ('name',)
    list_per_page = 10


class IngredientTypeAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['name', 'picture']})
    ]

    list_display = ('name',)
    list_per_page = 10

admin.site.register(models.RecipeComponent)
admin.site.register(models.UnitOfMeasure)
admin.site.register(models.Recipe, RecipeAdmin)
admin.site.register(models.RecipeType, RecipeTypeAdmin)
admin.site.register(models.Ingredient, IngredientAdmin)
admin.site.register(models.IngredientType, IngredientTypeAdmin)
admin.site.register(models.Rating, RatingAdmin)
admin.site.register(models.UserProfile, UserProfileAdmin)
