from django.shortcuts import get_object_or_404
from rest_framework.generics import GenericAPIView, RetrieveUpdateAPIView
from .serializer import (
    RegistrationSerializer,
    CustomAuthTokenSerializer,
    CustomTokenObtainPairSerializer,
    ChangePasswordSerializer,
    ProfileSerializer)
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
from mail_templated import send_mail,EmailMessage
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()

class RegistrationApiView(GenericAPIView):
    serializer_class = RegistrationSerializer
  
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        data = {
            'email': serializer.validated_data['email']
        }
        return Response(data, status=status.HTTP_201_CREATED)

class CustomAuthToken(ObtainAuthToken):
    serializer_class = CustomAuthTokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email
        })

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
            if not self.object.check_password(serializer.data.get('old_password')):
                return Response({'old_password':'wrong password'}, status=status.HTTP_400_BAD_REQUEST)
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Password updated successfully',
                'data': []
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

class ActivateProfileView(GenericAPIView):
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

        self.user_email = 'armin@armin.com'
        self.user_obj = get_object_or_404(Profile, user__email=self.user_email)
        email = EmailMessage(
            'email/hello.tpl',
            {
                'user': f"{self.user_obj.first_name} {self.user_obj.last_name}", 
                'token': self.get_tokens_for_user(self.user_obj)
            },
            'admin@example.com',
            ['self.user_obj.user.email'])
        EmailThread(email).start()
        return Response({'details':'email sent'})

    def get_tokens_for_user(self, user):
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)
