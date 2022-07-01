from django.contrib import admin
from lannister_auth.models import LannisterUser, Role


@admin.register(LannisterUser)
class LannisterUserAdmin(admin.ModelAdmin):
    list_display = ("id", "username", "email")


admin.site.register(Role)
