from django.db import models
from django.utils import timezone

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from .managers import CustomUserManager
from cryptography.fernet import Fernet
import os
import base64


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_("email address"), unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email


class Account(models.Model):
    public = models.CharField(max_length=256, blank=False, null=False)
    private = models.CharField(max_length=256, blank=False, null=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def save_private_key(self, private_key):
        cipher_suite = Fernet(os.getenv('ENCRYPTION_KEY'))
        encrypted_key = cipher_suite.encrypt(private_key.encode())
        self.private = base64.b64encode(encrypted_key).decode()

    def get_private_key(self):
        cipher_suite = Fernet(os.getenv('ENCRYPTION_KEY'))
        encrypted_key = base64.b64decode(self.private)
        private_key = cipher_suite.decrypt(encrypted_key).decode()
        return private_key
