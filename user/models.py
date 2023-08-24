from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.apps import apps

class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("The given username must be set")
        email = self.normalize_email(email)
        GlobalUserModel = apps.get_model(
            self.model._meta.app_label, self.model._meta.object_name
        )
        email = GlobalUserModel.normalize_username(email)
        user = self.model(email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    avatar = models.ImageField(verbose_name='Аватар', upload_to='user/')
    number = PhoneNumberField(verbose_name='Номер телефона')
    country = models.CharField(max_length=100, verbose_name='Страна')
    username = None
    email = models.EmailField(verbose_name='Почта', unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    email_verified = models.BooleanField(default=False, verbose_name='Почта подтверждена')
    email_verification_token = models.CharField(max_length=255, blank=True, null=True)

    objects = UserManager()



