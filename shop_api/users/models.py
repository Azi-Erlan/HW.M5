from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from users.managers import CustomUserManager


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    
    birthdate = models.DateField(null=True, blank=True)

    first_name = models.CharField(max_length=150,blank=True)
    last_name = models.CharField(max_length=150,blank=True)

    REGISTRATION_SOURCE_CHOICES = (
    ('local', 'local'),
    ('google', 'google'),
    ('facebook', 'facebook'),
)
    registration_source = models.CharField(max_length=20,choices=REGISTRATION_SOURCE_CHOICES,default='local')

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone_number']

    def __str__(self) -> str:
        return self.email


class ConfirmationCode(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.email} - {self.code}'