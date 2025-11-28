from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    """
    Public user representation used for nested displays.
    Excludes sensitive fields like password.
    """
    class Meta:
        model = User
        # include fields you want exposed in APIs
        fields = ("user_id", "username", "email", "first_name", "last_name", "phone_number", "role", "created_at")
        read_only_fields = ("user_id", "created_at")

class UserCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating users. Handles password properly with set_password.
    """
    password = serializers.CharField(write_only=True, required=True, min_length=8)

    class Meta:
        model = User
        fields = ("user_id", "username", "email", "first_name", "last_name", "phone_number", "role", "password")
        read_only_fields = ("user_id",)

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        # allow password update through this serializer
        password = validated_data.pop("password", None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)
        instance.save()
        return instance
