from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from verify_email.email_handler import ActivationMailManager
from .serializers import RegistrationSerializer

# Create your views here.




def register_user(request):
    if request.method == 'POST':
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():   
            user = serializer.save()
            ActivationMailManager.send_verification_link(request=request, inactive_user=user)
            return redirect('verification_sent')
    return render(request, 'register.html', {'serializer': serializer})