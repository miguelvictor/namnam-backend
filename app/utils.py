import re
import uuid
from django.db import IntegrityError
from django.http import JsonResponse
from django.utils.timezone import now, timedelta

from oauth2_provider.models import AccessToken, Application, RefreshToken
from oauth2_provider.settings import oauth2_settings

from oauthlib.common import generate_token


def is_client_known(request):
    try:
        return Application.objects.get(
            client_id=request.data.get('client_id', None),
            client_secret=request.data.get('client_secret', None),
        )
        return True
    except Application.DoesNotExist:
        return False


def get_default_app():
    return Application.objects.get(name='Namnam Android')


def get_token_json(access_token):
    """
    Takes an AccessToken instance as an argument
    and returns a JsonResponse instance from that
    AccessToken
    """
    token = {
        'access_token': access_token.token,
        'expires_in': oauth2_settings.ACCESS_TOKEN_EXPIRE_SECONDS,
        'token_type': 'Bearer',
        'refresh_token': access_token.refresh_token.token,
        'scope': access_token.scope
    }
    return JsonResponse(token)


def get_access_token(user):
    """
    Takes a user instance and return an access_token as a JsonResponse
    instance.
    """

    app = get_default_app()

    try:
        old_access_token = AccessToken.objects.get(
            user=user, application=app)
        old_refresh_token = RefreshToken.objects.get(
            user=user, access_token=old_access_token)
    except:
        pass
    else:
        old_access_token.delete()
        old_refresh_token.delete()

    token = generate_token()
    refresh_token = generate_token()

    expires = now() + timedelta(seconds=oauth2_settings.
                                ACCESS_TOKEN_EXPIRE_SECONDS)
    scope = "read write"

    access_token = AccessToken.objects.create(
        user=user, application=app, expires=expires,
        token=token, scope=scope)

    RefreshToken.objects.create(
        user=user, application=app, token=refresh_token,
        access_token=access_token)

    return get_token_json(access_token)


def normalize_recipe_params(ingredients):
    if ingredients is None or ingredients == '':
        return []

    return [int(x) for x in ingredients.split(',')]


def generate_slug(model):
    '''
    Generates UUID for User Profiles
    '''
    generated_uuid = uuid.uuid4().bytes.encode('base64')
    generated_uuid = re.sub('[^A-Za-z0-9]+', '', generated_uuid)[:5]
    try:
        model.objects.get(activation_key=generated_uuid)
    except (model.DoesNotExist, IntegrityError):
        return generated_uuid
    return generate_slug()
