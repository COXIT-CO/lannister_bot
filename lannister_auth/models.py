from django.db import models
from django.contrib.auth.models import (
    BaseUserManager,
    AbstractBaseUser,
    PermissionsMixin,
)
from django.core.exceptions import ObjectDoesNotExist
from django.db.models.signals import pre_save
from django.utils.translation import gettext_lazy as _
from lannister_roles.models import Role
from django.dispatch import receiver

class BaseManager(BaseUserManager):
    def get_or_none(self, **kwargs):
        try:
            return self.get(**kwargs)
        except ObjectDoesNotExist:
            return None


class LannisterUserManager(BaseManager):
    def create_user(
            self, email, username, password, first_name, last_name, **other_fields
    ):
        if not username:
            raise ValueError(_("Please provide username"))
        if not email:
            raise ValueError(_("Please provide an email"))

        email = self.normalize_email(email)
        user = self.model(
            email=email,
            username=username,
            first_name=first_name,
            last_name=last_name,
            **other_fields,
        )
        user.set_password(password)
        user.save()
        return user

    def create_superuser(
            self, email, username, password, first_name, last_name, **other_fields
    ):
        user = self.create_user(email, username, password, first_name, last_name)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user


def set_user_role():
    """ Get default status """
    return Role.objects.get_or_create(name="Worker")


class LannisterUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    slack_user_id = models.CharField(max_length=100, blank=True, null=True)
    slack_channel_id = models.CharField(max_length=100, blank=True, null=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    roles = models.ManyToManyField(Role, default=set_user_role)
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email", "first_name", "last_name"]

    objects = LannisterUserManager()

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        self.first_name = self.first_name.capitalize()
        self.last_name = self.last_name.capitalize()
        if self.is_superuser:
            self.roles.add(Role.objects.get(name="Administrator"))
            self.roles.add(Role.objects.get(name="Reviewer"))
            self.roles.add(Role.objects.get(name="Worker"))
        super().save(*args, **kwargs)

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        ordering = ["id"]
        verbose_name = "Lannister User"
        verbose_name_plural = "Lannister Users"


@receiver(pre_save, sender=LannisterUser)
def create_roles(sender, instance, *args, **kwargs):
    Role.objects.get_or_create(name="Administrator")
    Role.objects.get_or_create(name="Reviewer")
    Role.objects.get_or_create(name="Worker")
