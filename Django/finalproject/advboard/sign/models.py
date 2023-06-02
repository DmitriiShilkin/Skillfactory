from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class OneTimeCode(models.Model):
    code = models.CharField(max_length=255, primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Admin:
        pass
