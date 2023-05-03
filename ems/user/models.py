from django.db import models
from django. contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    is_user=models.BooleanField(default=False)
    fullname=models.CharField(null=True,max_length=100)
    is_admin = models.BooleanField(default=False,null=True)

    class meta:
        db_table = 'user'