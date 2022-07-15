from django.db import models
from django.contrib.auth.models import BaseUserManager


class Role(models.Model):
    objects = BaseUserManager()
    id = models.AutoField(auto_created=True, primary_key=True)
    name = models.CharField(max_length=20)  # get_user_display()
    description = models.CharField(max_length=128, null=True)

    def __str__(self):
        return self.name



