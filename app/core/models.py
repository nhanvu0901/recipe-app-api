from email.policy import default

from django.db import models

#setting is the app.settings
from django.conf import settings
# Create your models here.
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
    BaseUserManager,
)
from django.utils.regex_helper import normalize


class UserManager(BaseUserManager):
    def create_user(self,email,password=None, **extra_fields):
       #normalize the email
        # email_string = email.split('@')
        # if any(char[0].isupper() or char[1].isupper() for char in email_string[1].split('.')):
        #     email = f'{email_string[0]}@{email_string[1].split(".")[0].lower()}.com'

        if not email:
            raise ValueError('User must have email address')

        email = self.normalize_email(email)

        if self.filter(email=email).exists():
            raise ValueError('A user with this email address already exists')


       # The self.model attribute in UserManager refers to the User model because UserManager is assigned to the User model’s objects attribut
        user = self.model(email= self.normalize_email(email), **extra_fields)
        user.set_password(password)
        #recommend to use whenever create or saving new object using a user manager
        user.save(using=self._db)
        return user

    def create_superuser(self,email,password=None, **extra_fields):
        user = self.model(email= self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser,PermissionsMixin):
    email = models.EmailField(max_length=255, unique= True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default= True)
    is_staff = models.BooleanField(default= False)

    objects = UserManager()

    USERNAME_FIELD = 'email'


class CustomToken(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    access_token = models.TextField()
    refresh_token = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    tokenExpiredTime = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return {
            'access_token': self.access_token,
            'refresh_token': self.refresh_token,
            'created': self.created.isoformat(),
            'user': self.user.email,
            'tokenExpiredTime': self.tokenExpiredTime.isoformat(),
        }

class Recipe(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete= models.CASCADE,
    )
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    time_minutes = models.IntegerField()
    price = models.DecimalField(max_digits=5, decimal_places=2)
    link = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.title