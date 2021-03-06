# from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from accounts.models import User, Profile
from django.core import exceptions
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class RegistrationSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(max_length=255)

    class Meta:
        model = User
        fields = ["email", "password", "password1"]

    def validate(self, attrs):
        if attrs.get("password1") != attrs.get("password"):
            raise serializers.ValidationError(
                {"detail": "passwords doesnt match"}
            )
        try:
            validate_password(attrs.get("password"))
        except exceptions.ValidationError as e:
            raise serializers.ValidationError({"password": list(e.messages)})
        return super().validate(attrs)

    def create(self, validated_data):
        validated_data.pop("password1", None)
        return User.objects.create_user(**validated_data)


class CustomAuthTokenSerializer(serializers.Serializer):
    email = serializers.CharField(label=_("email"), write_only=True)
    password = serializers.CharField(
        label=_("Password"),
        style={"input_type": "password"},
        trim_whitespace=False,
        write_only=True,
    )
    token = serializers.CharField(label=_("Token"), read_only=True)

    def validate(self, attrs):
        username = attrs.get("email")
        password = attrs.get("password")

        if username and password:
            user = authenticate(
                request=self.context.get("request"),
                username=username,
                password=password,
            )

            # The authenticate call simply returns None for is_active=False
            # users. (Assuming the default ModelBackend authentication
            # backend.)
            if not user:
                msg = _("Unable to log in with provided credentials.")
                raise serializers.ValidationError(msg, code="authorization")
            if not user.is_verified:
                raise serializers.ValidationError(
                    {"detail": "user is not verified"}
                )
        else:
            msg = _('Must include "username" and "password".')
            raise serializers.ValidationError(msg, code="authorization")

        attrs["user"] = user
        return attrs


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        validate_data = super().validate(attrs)
        if not self.user.is_verified:
            raise serializers.ValidationError(
                {"detail": "user is not verified"}
            )
        validate_data["email"] = self.user.email
        validate_data["user_id"] = self.user.id
        return validate_data


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(max_length=100, required=True)
    new_password = serializers.CharField(max_length=100, required=True)
    new_password1 = serializers.CharField(max_length=100, required=True)

    def validate(self, attrs):
        if attrs.get("new_password1") != attrs.get("new_password"):
            raise serializers.ValidationError(
                {"detail": "passwords doesnt match"}
            )
        try:
            validate_password(attrs.get("new_password"))
        except exceptions.ValidationError as e:
            raise serializers.ValidationError(
                {"new_password": list(e.messages)}
            )
        return super().validate(attrs)


class ProfileSerializer(serializers.ModelSerializer):
    email = serializers.CharField(source="user.email", read_only=True)

    class Meta:
        model = Profile
        fields = ["first_name", "last_name", "email", "image", "description"]
        # read_only_fields = ['email'] # does not work, you have to set read_only in email field which is above


class ResendVerifySerializer(serializers.Serializer):
    email = serializers.CharField(required=True)

    def validate(self, attrs):
        email = attrs.get("email")
        try:
            profile_obj = Profile.objects.get(user__email=email)
        except Profile.DoesNotExist:
            raise serializers.ValidationError(
                {"detail": "email is not valid"}
            )
        user_obj = profile_obj.user
        if user_obj.is_verified:
            raise serializers.ValidationError(
                {"detail": "your account is already verified"}
            )
        attrs["profile_obj"] = profile_obj
        return super().validate(attrs)
