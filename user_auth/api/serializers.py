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
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Ein Benutzer mit dieser E-Mail-Adresse existiert bereits.")
        return value

    def validate(self, data):
        if data['password'] != data['confirmed_password']:
            raise serializers.ValidationError({"password": "Passwörter stimmen nicht überein."})
        return data

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['email'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        user.is_active = False
        user.save()
        return user
