from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.db import models

class UserManager(BaseUserManager):
    def create_user(self, email, nickname, address, password):
        if not email:
            raise ValueError('must have user email')
        if not nickname:
            raise ValueError('must have user nickname')
        if not address:
            raise ValueError('must have user name')
        user = self.model(
            email=self.normalize_email(email),
            nickname=nickname,
            address=address
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, nickname, address, password=None):
        user = self.create_user(
            email,
            password=password,
            nickname=nickname,
            address=address
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    nickname = models.CharField(max_length=30, unique=True)
    email = models.EmailField(unique=True)
    address = models.TextField()
    refresh_token = models.CharField(max_length=255, default="")
    access_token = models.CharField(max_length=255, default="")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nickname', 'address']
