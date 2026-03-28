from rest_framework import serializers
from django.contrib.auth.models import User



class RegistrationSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    confirmed_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'email', 'password', 'confirmed_password']

    def validate(self, data):
        if data['password'] != data['confirmed_password']:
            raise serializers.ValidationError({"password": "Passwörter stimmen nicht überein."})
        return data

    def create(self, validated_data):
        # Das Passwort wird sicher (gehasht) gespeichert
        user = User.objects.create_user(
            username=validated_data['email'], # Oft wird Email als Username genutzt
            email=validated_data['email'],
            password=validated_data['password']
        )
        user.is_active = False # Deaktiviert bis zur Email-Bestätigung
        user.save()
        return user

