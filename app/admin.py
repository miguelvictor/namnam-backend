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


admin.site.register(models.UserProfile, UserProfileAdmin)
