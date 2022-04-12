from django.db import models
#AbstractUser:元からフィールド定義してある。
from django.contrib.auth.models import AbstractUser
# Create your models here.

class CustomUser(AbstractUser):
    class Meta:
        verbose_name_plural='CustomUser'