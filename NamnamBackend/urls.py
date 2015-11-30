from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^api-auth/', include('app.urls', namespace='app')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^oauth/', include('oauth2_provider.urls',
        namespace='oauth2_provider')),
]
