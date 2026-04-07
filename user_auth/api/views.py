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
    """
    API endpoint for user registration. Accepts email, password, and confirmed_password in the request data.
    Validates the data using the RegistrationSerializer, creates a new user with is_active set to
    False, and sends an email with an activation link to the user's email address.
    """
    serializer = RegistrationSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        
        verification_link = f"http://localhost:8000/api/activate/{uid}/{token}/"
        
        send_mail(
            subject="Welcome to Videoflix! Please verify your email",
            message=f"Hello,\n\nPlease click the following link to activate your account:\n\n{verification_link}",
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
    """
    API endpoint for user login. Accepts email and password in the request data.
    Authenticates the user, checks if the account is active, and if successful, generates
    JWT access and refresh tokens, sets them in HttpOnly cookies, and returns a success response.
    If authentication fails or the account is inactive, returns appropriate error responses.
    """
    email = request.data.get('email')
    password = request.data.get('password')

    try:
        user = User.objects.get(username=email)
    except User.DoesNotExist:
        return Response({"detail": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

    if not user.check_password(password):
        return Response({"detail": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

    if not user.is_active:
        return Response({"detail": "Please activate your account via email."}, status=status.HTTP_403_FORBIDDEN)

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
        samesite='None',
        secure=True
    )
    response.set_cookie(
        key='refresh_token',
        value=str(refresh),
        httponly=True,
        samesite='None',
        secure=True
    )
    return response

@api_view(['GET'])
@permission_classes([AllowAny])
def activate_user(request, uidb64, token):
    """
    API endpoint for account activation. Accepts uidb64 and token as URL parameters.
    Decodes the uidb64 to get the user ID, retrieves the user, and checks if the token is valid.
    If valid, sets the user's is_active to True and saves the user, effectively activating the account.
    Returns a success response if activation is successful, or an error response if activation fails.
    """
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return redirect('http://localhost:5500/login.html?activation=success')
    else:
        return redirect('http://localhost:5500/login.html?activation=failed')



@api_view(['POST'])
def logout_user(request):
    """
    API endpoint for user logout. Retrieves the refresh token from the cookies, blacklists it to invalidate it,
    and deletes the access and refresh tokens from the cookies. Returns a success response if logout is successful.
    If the refresh token is invalid or not provided, returns appropriate error responses.
    """
    refresh_token = request.COOKIES.get('refresh_token')
    if refresh_token:
        try:
            token = RefreshToken(refresh_token)
            token.blacklist()  
            return Response({"detail": "Logout successful! All tokens will be deleted. Refresh token is now invalid."}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"detail": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)

    response = Response({"detail": "Logout successful"}, status=status.HTTP_200_OK)
    response.delete_cookie('access_token')
    response.delete_cookie('refresh_token')
    return response



@api_view(['POST'])
def refresh_token(request):
    """
    API endpoint for refreshing the access token. Retrieves the refresh token from the cookies,
    generates a new access token, and sets it in the cookies. Returns the new access token in the response.
    If the refresh token is invalid or not provided, returns appropriate error responses.
    """
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
                samesite='None',
                secure=True
            )
            return response
        except Exception as e:
            return Response({"detail": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)
    return Response({"detail": "Refresh token not provided"}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def password_reset_request(request):
    """
    API endpoint for requesting a password reset. Accepts email in the request data.
    If a user with the provided email exists, generates a password reset token and sends an email with a password reset link to the user's email address.
    Returns a success response regardless of whether a user with the provided email exists, to prevent email enumeration.
    """
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
    """
    API endpoint for confirming a password reset and setting a new password. Accepts uidb64 and token as URL parameters, and new_password in the request data.
    Decodes the uidb64 to get the user ID, retrieves the user, and checks if the token is valid. If valid, sets the user's password to the new password provided in the request data and saves the user.
    Returns a success response if the password reset is successful, or an error response if the token is invalid or the new password is not provided.
    """
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