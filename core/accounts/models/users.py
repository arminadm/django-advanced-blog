from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.utils.translation import ugettext_lazy as _

# Create your models here.
class CustomeUserManager(BaseUserManager):
    '''
    Custom user model manager where email is the unique identifiers
        for authentication instead of usernames.
    '''
    def create_user(self, email, password, **extra_fields):
        '''
        Create and save a new user by their email and password
        '''
        if not email:
            raise ValueError(_('The Email field can not be empty'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self , email, password, **extra_fields):
        '''
        Create and save a new superuser their email and password
        '''
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        
        # just in case that everything goes right
        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        if extra_fields.get('is_active') is not True:
            raise ValueError(_('Superuser must have is_active=True.'))
        
        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    '''
    User base models
    note: we dont need to add password field, abstractbaseuser already did that for us
    '''
    email = models.EmailField(unique=True, null=False, blank=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomeUserManager()

    def __str__(self):
        return self.email