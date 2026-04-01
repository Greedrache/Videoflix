from rest_framework import serializers
from django.contrib.auth.models import User

class RegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration. Validates that the email is unique and that the password and confirmed_password match.
    """
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    confirmed_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'email', 'password', 'confirmed_password']

    def validate_email(self, value):
        """
        Validates that the email is unique.
        """
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("A user with that email already exists.")
        return value

    def validate(self, data):
        """
        Validates that the password and confirmed_password match.
        """
        if data['password'] != data['confirmed_password']:
            raise serializers.ValidationError({"password": "Passwords do not match."})
        return data

    def create(self, validated_data):
        """
        Creates a new user with the provided email and password. 
        The user is created with is_active set to False, and will need to verify their email before they can log in.
        """
        user = User.objects.create_user(
            username=validated_data['email'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        user.is_active = False
        user.save()
        return user
