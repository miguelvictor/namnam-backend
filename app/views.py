from django.conf import settings
from django.contrib.auth.models import User
from django.core.mail.message import EmailMessage
from django.views.generic.base import TemplateView

from app.models import UserProfile, FacebookProfile, GoogleProfile
from app.serializers import UserSerializer
from app.utils import is_client_known, get_access_token

from rest_framework.response import Response
from rest_framework.decorators import api_view


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

        user.email = 'REG_GOOGLE_' + email
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

        user.email = 'REG_FACEBOOK_' + email
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
            return Response('Incorrect password', status=400)
    except User.DoesNotExist:
        try:
            user = User.objects.get(email=identifier)

            if user.check_password(password):
                return get_access_token(user)
            else:
                return Response('Unauthorized', status=400)
        except User.DoesNotExist:
            return Response('Account does not exist', status=404)


def createMail(user):
    key = user.profile.activation_key
    email_subject = 'NamNam Account Confirmation'
    email_body = "Hi %s,<br/>Confirming your email address will give you full access to Nam-Nam. Your Activation Code: <br/><center><h3 style=\"background:black;color:white;\">%s</h3></center> You can also click the link below to confirm otherwise ignore this message.<br/><a href=\"http://activate/%s\">Activate Email</a></br>Thank you,<br/> Jc and Friends Inc." % (
        user, key, key)
    mail = EmailMessage(
        email_subject, email_body, settings.EMAIL_HOST_USER, [user.email])
    mail.content_subtype = "html"
    mail.send()


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
        createMail(user)
        return get_access_token(user)

    return Response(serialized._errors, status=400)


class IndexView(TemplateView):
    template_name = 'app/index.html'
