from django.contrib.auth import authenticate
from django.contrib.auth.models import User

from app.models import UserProfile, FacebookProfile, GoogleProfile
from app.serializers import UserSerializer
from app.utils import is_client_known, get_access_token

from rest_framework.response import Response
from rest_framework.decorators import api_view

import re


@api_view(['POST'])
def signin_google(request):
    if not is_client_known(request):
        return Response('Forbidden', status=401)

    id = request.data.get('id')

    try:
        user = User.objects.get(profile__google__id=id)
    except User.DoesNotExist:
        email = request.data.get('email')

        user = User.objects.create_user(
            username='ANDGOREG' + email.split('@')[0],
            password='12345',
        )

        user.email = email
        user.save()

        user.profile = UserProfile()
        user.profile.state = 'google'
        user.profile.save()

        GoogleProfile.objects.create(
            profile=user.profile, id=id,
            email=email, name=request.data.get('name'))

    return get_access_token(user)


@api_view(['POST'])
def signin_fb(request):
    if not is_client_known(request):
        return Response('Forbidden', status=401)

    id = request.data.get('id')

    try:
        user = User.objects.get(profile__facebook__id=id)
    except User.DoesNotExist:
        email = request.data.get('email')

        user = User.objects.create_user(
            username='ANDFBREG' + email.split('@')[0],
            password='12345',
        )

        user.email = email
        user.save()

        user.profile = UserProfile()
        user.profile.state = 'fb'
        user.profile.save()

        FacebookProfile.objects.create(
            profile=user.profile, id=id,
            email=email, name=request.data.get('name'))

    return get_access_token(user)


@api_view(['POST'])
def signin(request):
    if not is_client_known(request):
        return Response('Forbidden', status=401)

    identifier = request.data.get('identifier')
    password = request.data.get('password')

    try:
        user = User.objects.get(username=identifier)

        if user.check_password(password):
            return get_access_token(user)
        else:
            return Response('Unauthorized', status=400)
    except User.DoesNotExist:
        try:
            user = User.objects.get(email=identifier)

            if user.check_password(password):
                return get_access_token(user)
            else:
                return Response('Unauthorized', status=400)
        except User.DoesNotExist:
            return Response('User Not Found', status=404)


@api_view(['POST'])
def register(request):
    if not is_client_known(request):
        return Response('Forbidden', status=401)

    serialized = UserSerializer(data=request.data)

    if serialized.is_valid():
        user = User.objects.create_user(
            username=serialized.validated_data['username'],
            password=serialized.validated_data['password'],
        )

        user.email = serialized.validated_data['email']
        user.save()

        user.profile = UserProfile()
        user.profile.save()

        return get_access_token(user)

    return Response(serialized._errors, status=400)