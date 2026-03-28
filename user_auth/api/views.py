from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from verify_email.email_handler import ActivationMailManager
from .serializers import RegistrationSerializer

# Create your views here.


@api_view(['POST'])
def register_user(request):
    serializer = RegistrationSerializer(data=request.data)
    if serializer.is_valid():   
        user = serializer.save()
        ActivationMailManager.send_verification_link(request=request, inactive_user=user)
        return Response({'message': 'User erfolgreich registriert und Verifizierungs-Email versandt.'}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)