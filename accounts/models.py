from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.db import models

from phonenumber_field.modelfields import PhoneNumberField


class UserManager(BaseUserManager):
    def create_user(self, email, nickname, address, phone, password, role='회원'):
        if not email:
            raise ValueError('must have user email')
        if not nickname:
            raise ValueError('must have user nickname')
        if not phone:
            raise ValueError('must have user phone')
        user = self.model(
            email=self.normalize_email(email),
            nickname=nickname,
            address=address,
            phone=phone,
            role=role
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, nickname, phone, address='우주',password=None):
        user = self.create_user(
            email,
            password=password,
            nickname=nickname,
            address=address,
            phone=phone
        )
        user.is_admin = True
        user.is_staff = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    nickname = models.CharField(max_length=30, unique=True)
    email = models.EmailField(unique=True)
    address = models.TextField()
    phone = PhoneNumberField(unique=True, null=True)
    role = models.CharField(default='회원', max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nickname', 'phone']

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return self.is_admin
