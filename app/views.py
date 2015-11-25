from django.shortcuts import render
from django.contrib.auth.models import User

from . import serializers

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['POST'])
def signup(request):
	serialized = serializers.UserSerializer(data=request.data)

	if serialized.is_valid():
		user = User.objects.create_user(
			username=serialized.initial_data['username'],
			email=serialized.initial_data['email'],
			password=serialized.initial_data['password'],
		)
		serialized = serializers.UserSerializer(user)
		return Response(serialized.data, status=status.HTTP_201_CREATED)

	return Response(serialized._errors, status=status.HTTP_400_BAD_REQUEST)