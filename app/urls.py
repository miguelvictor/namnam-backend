from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^signin/$', views.signin, name='signin'),
    url(r'^signin-google/$', views.signin_google, name='signup-google'),
    url(r'^signin-fb/$', views.signin_fb, name='signup-fb'),
    url(r'^signup/$', views.register, name='signup'),
]
