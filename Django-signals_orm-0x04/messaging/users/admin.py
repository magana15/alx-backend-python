from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from .models import User

@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    model = User
    # keep default Django UserAdmin fields but swap PK and email display
    list_display = ("email", "username", "role", "is_staff", "is_superuser", "created_at")
    ordering = ("-created_at",)
    search_fields = ("email", "username", "first_name", "last_name")
