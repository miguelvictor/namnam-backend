from django.contrib.auth.models import User, Group

from rest_framework import permissions, serializers, viewsets

from oauth2_provider.ext.rest_framework import TokenHasReadWriteScope
from oauth2_provider.ext.rest_framework import TokenHasScope


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'email',
                  'first_name', 'last_name')
        read_only_fields = 'id',
        extra_kwargs = {'password': {'write_only': True}}


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group


class UserViewSet(viewsets.ModelViewSet):
    permission_classes = permissions.IsAuthenticated, TokenHasReadWriteScope
    queryset = User.objects.all()
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    permission_classes = permissions.IsAuthenticated, TokenHasScope
    required_scopes = 'groups',
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
