from django.apps import apps
from django.db import models
from django.contrib.auth.models import User
from .utils import generate_slug

from app import inflect


USER_STATES = (
    ('fb', 'From Facebook'),
    ('google', 'From Google'),
    ('clean', 'Native'),
)


def generate_slug_profile():
    model = apps.get_model(app_label='app', model_name='UserProfile')
    return generate_slug(model)


class UserProfile(models.Model):
    user = models.OneToOneField(User, related_name='profile')
    activation_key = models.CharField(
        max_length=5, blank=True)
    activated = models.BooleanField(default=False)
    state = models.CharField(
        max_length=255, choices=USER_STATES, default='clean')

    def __unicode__(self):
        ''' checking user object '''
        if self.user.first_name and self.user.last_name:
            return self.user.first_name + ' ' + self.user.last_name

        ''' checking facebook profile '''
        try:
            return self.facebook.name
        except:
            pass

        ''' checking google profile '''
        try:
            return self.google.name
        except:
            pass

        return self.user.username


class FacebookProfile(models.Model):
    id = models.CharField(primary_key=True, max_length=255)
    profile = models.OneToOneField(UserProfile, related_name='facebook')
    email = models.EmailField()
    name = models.CharField(max_length=255)

    def __unicode__(self):
        return self.name


class GoogleProfile(models.Model):
    id = models.CharField(primary_key=True, max_length=255)
    profile = models.OneToOneField(UserProfile, related_name='google')
    email = models.EmailField()
    name = models.CharField(max_length=255)

    def __unicode__(self):
        return self.name


class RecipeType(models.Model):
    name = models.CharField(max_length=255)
    picture = models.URLField()

    def __unicode__(self):
        return self.name.capitalize()


class IngredientType(models.Model):
    name = models.CharField(max_length=255)
    picture = models.URLField()

    def __unicode__(self):
        return self.name.capitalize()


class Ingredient(models.Model):
    banner = models.URLField()
    description = models.TextField()
    icon = models.URLField()
    name = models.CharField(max_length=255)
    type = models.ForeignKey(IngredientType, related_name='ingredients')

    def __unicode__(self):
        return self.name.capitalize()


class UnitOfMeasure(models.Model):
    name = models.CharField(max_length=255)

    def __unicode__(self):
        return self.name


class Recipe(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    icon = models.URLField()
    banner = models.URLField()
    default_serving_size = models.IntegerField()
    time_to_complete = models.IntegerField()
    categories = models.ManyToManyField(RecipeType, related_name='recipes')

    class Meta:
        ordering = 'name',

    def __unicode__(self):
        return self.name.capitalize()


class RecipeComponent(models.Model):
    recipe = models.ForeignKey(Recipe, related_name='recipe_components')
    quantity = models.FloatField()
    adjective = models.CharField(max_length=255, blank=True)
    unit_of_measure = models.ForeignKey(UnitOfMeasure)
    ingredient = models.ForeignKey(Ingredient)
    extra = models.CharField(max_length=255, blank=True)

    def __unicode__(self):
        p = inflect.engine()

        if (self.quantity).is_integer():
            string = "%s " % str(int(self.quantity))
        else:
            string = "%s " % str(self.quantity)

        if self.unit_of_measure.name != 'generic':
            string += "%s of " % p.plural(
                self.unit_of_measure.name, int(self.quantity))

        if self.adjective:
            string += "%s " % self.adjective

        string += self.ingredient.name.lower()

        return string


class Step(models.Model):
    sequence = models.IntegerField(default=1)
    instruction = models.TextField()
    recipe = models.ForeignKey(Recipe, related_name='steps')

    def __unicode__(self):
        return 'Step %s' % str(self.sequence)

    class Meta:
        ordering = ['sequence']


class Rating(models.Model):
    who = models.ForeignKey(User)
    rating = models.IntegerField(default=0)
    recipe = models.ForeignKey(Recipe, related_name='ratings')

    def __unicode__(self):
        return str(self.recipe) + ' ' + str(self.rating)
