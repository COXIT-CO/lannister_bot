from django.db import models
from django.contrib.auth.models import (
    BaseUserManager,
    AbstractBaseUser,
    PermissionsMixin,
)
from django.core.exceptions import ObjectDoesNotExist
from django.db.models.signals import pre_save
from django.utils.translation import gettext_lazy as _


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


class Role(models.Model):
    """
    Roles could be implemented with is_staff and is_superuser but it depends on schema.
    If we'll want to scale aka add another user type, we'll have to do something similar anyway.
    """

    objects = BaseUserManager()

    ADMIN = 1
    REVIEWER = 2
    WORKER = 3

    USER_ROLE_CHOISES = (
        (ADMIN, _("Administrator")),
        (REVIEWER, _("Reviewer")),
        (WORKER, _("Worker")),
    )

    id = models.PositiveSmallIntegerField(choices=USER_ROLE_CHOISES, primary_key=True)
    users = models.ManyToManyField("LannisterUser")
    description = models.CharField(max_length=128, null=True)

    def __str__(self):
        return self.get_id_display()


class LannisterUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    slack_user_id = models.CharField(max_length=100, blank=True, null=True)
    slack_channel_id = models.CharField(max_length=100, blank=True, null=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    roles = models.ManyToManyField(Role)
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email", "first_name", "last_name"]

    objects = LannisterUserManager()

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        self.first_name = self.first_name.capitalize()
        self.last_name = self.last_name.capitalize()
        if self.is_superuser:
            self.roles.add(Role.objects.get(id=1))
            self.roles.add(Role.objects.get(id=2))
            self.roles.add(Role.objects.get(id=3))

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


def create_roles(sender, instance, *args, **kwargs):
    Role.objects.get_or_create(id=1)
    Role.objects.get_or_create(id=2)
    Role.objects.get_or_create(id=3)


pre_save.connect(create_roles, sender=LannisterUser)
