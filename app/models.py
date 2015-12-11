from django.db import models
from django.contrib.auth.models import User

USER_STATES = (
    ('fb', 'From Facebook'),
    ('google', 'From Google'),
    ('clean', 'Native'),
)


class UserProfile(models.Model):
    user = models.OneToOneField(User, related_name='profile')
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
    id = models.CharField(max_length=255)
    profile = models.OneToOneField(UserProfile, related_name='facebook')
    email = models.EmailField()
    name = models.CharField(max_length=255)

    def __unicode__(self):
        return self.name


class GoogleProfile(models.Model):
    id = models.CharField(max_length=255)
    profile = models.OneToOneField(UserProfile, related_name='google')
    email = models.EmailField()
    name = models.CharField(max_length=255)

    def __unicode__(self):
        return self.name
