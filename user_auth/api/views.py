from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import RegistrationSerializer

@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    serializer = RegistrationSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        
        verification_link = f"http://localhost:8000/api/activate/{uid}/{token}/"
        
        send_mail(
            subject="Willkommen bei Videoflix! Bitte E-Mail bestaetigen",
            message=f"Hallo,\n\nbitte klicke auf den folgenden Link, um deinen Account freizuschalten:\n\n{verification_link}",
            from_email="noreply@videoflix.com",
            recipient_list=[user.email],
            fail_silently=False,
        )

        return Response({
            "user": {
                "id": user.id,
                "email": user.email
            },
            "token": token
        }, status=status.HTTP_201_CREATED)
        
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])
def login_user(request):
    email = request.data.get('email')
    password = request.data.get('password')
    
    # In Django default auth, authenticate() returns None if user.is_active is False.
    # We need to manually check password first to return the 403 instead of 401
    try:
        user = User.objects.get(username=email)
    except User.DoesNotExist:
        return Response({"detail": "Ungueltige Anmeldedaten"}, status=status.HTTP_401_UNAUTHORIZED)

    if not user.check_password(password):
        return Response({"detail": "Ungueltige Anmeldedaten"}, status=status.HTTP_401_UNAUTHORIZED)

    if not user.is_active:
        # Authenticate returns None if inactive, which is why we do it manually
        return Response({"detail": "Bitte aktiviere deinen Account ueber die Email."}, status=status.HTTP_403_FORBIDDEN)

    # generate tokens
    refresh = RefreshToken.for_user(user)
    response = Response({
        "detail": "Login successful",
        "user": {
            "id": user.id,
            "username": user.username
        }
    }, status=status.HTTP_200_OK)
    
    response.set_cookie(
        key='access_token',
        value=str(refresh.access_token),
        httponly=True,
        samesite='Lax'
    )
    response.set_cookie(
        key='refresh_token',
        value=str(refresh),
        httponly=True,
        samesite='Lax'
    )
    return response

@api_view(['GET'])
@permission_classes([AllowAny])
def activate_user(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return Response({"message": "Account successfully activated."}, status=status.HTTP_200_OK)
    else:
        return Response({"message": "Aktivierung fehlgeschlagen."}, status=status.HTTP_400_BAD_REQUEST)



@api_view(['POST'])
def logout_user(request):
    refresh_token = request.COOKIES.get('refresh_token')
    if refresh_token:
        try:
            token = RefreshToken(refresh_token)
            token.blacklist()  # Blacklist the refresh token
            return Response({"detail": "Logout successful! All tokens will be deleted. Refresh token is now invalid."}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"detail": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)

    response = Response({"detail": "Logout successful"}, status=status.HTTP_200_OK)
    response.delete_cookie('access_token')
    response.delete_cookie('refresh_token')
    return response



@api_view(['POST'])
def refresh_token(request):
    refresh_token = request.COOKIES.get('refresh_token')
    if refresh_token:
        try:
            token = RefreshToken(refresh_token)
            new_access_token = str(token.access_token)
            response = Response({"access_token": new_access_token}, status=status.HTTP_200_OK)
            response.set_cookie(
                key='access_token',
                value=new_access_token,
                httponly=True,
                samesite='Lax'
            )
            return response
        except Exception as e:
            return Response({"detail": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)
    return Response({"detail": "Refresh token not provided"}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def password_reset_request(request):
    email = request.data.get('email')
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return Response({"detail": "If an account with this email exists, a password reset email has been sent."}, status=status.HTTP_200_OK)

    token = default_token_generator.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    
    reset_link = f"https://tim-thiele.de/pages/auth/confirm_password.html?uid={uid}&token={token}"   
    send_mail(
        subject="Password Reset Request for Videoflix",
        message=f"Hello,\n\nClick the following link to reset your password:\n\n{reset_link}",
        from_email="noreply@videoflix.com",
        recipient_list=[email],
    )
    return Response({"detail": "If an account with this email exists, a password reset email has been sent."}, status=status.HTTP_200_OK)


@api_view(['POST'])
def password_reset_confirm(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        new_password = request.data.get('new_password')
        if new_password:
            user.set_password(new_password)
            user.save()
            return Response({"detail": "Password successfully reset."}, status=status.HTTP_200_OK)
        else:
            return Response({"detail": "New password not provided."}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({"detail": "Invalid link or token."}, status=status.HTTP_400_BAD_REQUEST)