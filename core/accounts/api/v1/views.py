from django.shortcuts import get_object_or_404
from rest_framework.generics import GenericAPIView, RetrieveUpdateAPIView
from .serializer import (
    RegistrationSerializer,
    CustomAuthTokenSerializer,
    CustomTokenObtainPairSerializer,
    ChangePasswordSerializer,
    ProfileSerializer,
    ResendVerifySerializer,
)
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth import get_user_model
from accounts.models import Profile
from .utils import EmailThread

# from django.core.mail import send_mail
from mail_templated import send_mail, EmailMessage
from rest_framework_simplejwt.tokens import RefreshToken
from jwt import decode
from django.conf import settings
from jwt.exceptions import InvalidSignatureError, ExpiredSignatureError

User = get_user_model()


class RegistrationApiView(GenericAPIView):
    serializer_class = RegistrationSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user_email = serializer.validated_data["email"]
        data = {"email": user_email}
        self.user_email = user_email
        self.user_obj = get_object_or_404(
            Profile, user__email=self.user_email
        )
        email = EmailMessage(
            "email/email_verification.tpl",
            {
                "user": f"{self.user_obj.first_name} {self.user_obj.last_name}",
                "token": self.get_tokens_for_user(self.user_obj),
            },
            "admin@example.com",
            [self.user_obj.user.email],
        )
        EmailThread(email).start()
        return Response(data, status=status.HTTP_201_CREATED)

    def get_tokens_for_user(self, user):
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)


class CustomAuthToken(ObtainAuthToken):
    serializer_class = CustomAuthTokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        token, created = Token.objects.get_or_create(user=user)
        return Response(
            {"token": token.key, "user_id": user.pk, "email": user.email}
        )


class DestroyAuthToken(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class ChangePasswordApiView(GenericAPIView):
    model = User
    permission_classes = [IsAuthenticated]
    serializer_class = ChangePasswordSerializer

    def get_object(self):
        obj = self.request.user
        return obj

    def put(self, request):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            # check old password
            if not self.object.check_password(
                serializer.data.get("old_password")
            ):
                return Response(
                    {"old_password": "wrong password"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            response = {
                "status": "success",
                "code": status.HTTP_200_OK,
                "message": "Password updated successfully",
                "data": [],
            }
            return Response(response)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProfileApiView(RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()

    def get_object(self):
        queryset = self.queryset
        obj = get_object_or_404(queryset, id=self.request.user.id)
        return obj


class TestActivateProfileView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    # serializer_class = ActivateProfileSerializer
    def get(self, request, *args, **kwargs):
        # """STEP1: sending email via django.core.mail"""
        # send_mail(
        #     'Subject here',
        #     'Here is the message.',
        #     'from@example.com',
        #     ['to@example.com'],
        #     fail_silently=False,
        # )

        # """STEP2: sending email without threading"""
        # send_mail('email/hello.tpl', {'user': 'armindarabimahboub'}, 'admin@example.com', ['user@example.com'])

        self.user_email = "armin@armin.com"
        self.user_obj = get_object_or_404(
            Profile, user__email=self.user_email
        )
        email = EmailMessage(
            "email/hello.tpl",
            {
                "user": f"{self.user_obj.first_name} {self.user_obj.last_name}",
                "token": self.get_tokens_for_user(self.user_obj),
            },
            "admin@example.com",
            [self.user_obj.user.email],
        )
        EmailThread(email).start()
        return Response({"details": "email sent"})

    def get_tokens_for_user(self, user):
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)


class ConfirmVerifyView(APIView):
    def get(self, request, token, *args, **kwargs):
        try:
            decoded_info = decode(
                token, settings.SECRET_KEY, algorithms=["HS256"]
            )
        except InvalidSignatureError:
            return Response(
                {"details": "Invalid token"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except ExpiredSignatureError:
            return Response(
                {"details": "your token has expired"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        user_id = decoded_info.get("user_id")
        user_obj = get_object_or_404(User, id=user_id)
        if user_obj.is_verified:
            return Response(
                {"details": "your account is already activated"},
                status=status.HTTP_200_OK,
            )
        user_obj.is_verified = True
        user_obj.save()
        return Response(
            {"details": "your account activated successfully"},
            status=status.HTTP_200_OK,
        )


class ResendVerifyView(GenericAPIView):
    serializer_class = ResendVerifySerializer

    def post(self, request, *args, **kwargs):
        serializer = ResendVerifySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.profile_obj = serializer.validated_data["profile_obj"]
        self.user_obj = self.profile_obj.user
        email = EmailMessage(
            "email/email_verification.tpl",
            {
                "user": f"{self.profile_obj.first_name} {self.profile_obj.last_name}",
                "token": self.get_tokens_for_user(self.user_obj),
            },
            "admin@example.com",
            [self.user_obj.email],
        )
        EmailThread(email).start()
        return Response({"details": "email resent successfully"})

    def get_tokens_for_user(self, user):
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)
