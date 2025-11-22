import uuid
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Custom user model with UUID primary key, unique email, phone number
    and role.
    Extends AbstractUser to reuse username/password/auth plumbing.
    """

    id = None  # deliberately hide the default 'id' field from AbstractUser

    user_id = models.UUIDField(
    primary_key=True, default=uuid.uuid4, editable=False, db_index=True)

    # We'll enforce email uniqueness and use it as a canonical identifier
    # in the app.
    email = models.EmailField("email address", unique=True)

    phone_number = models.CharField(max_length=20, blank=True, null=True)

    ROLE_GUEST = "guest"
    ROLE_HOST = "host"
    ROLE_ADMIN = "admin"
    ROLE_CHOICES = [
        (ROLE_GUEST, "Guest"),
        (ROLE_HOST, "Host"),
        (ROLE_ADMIN, "Admin"),
    ]
    role = models.CharField(
    max_length=10, choices=ROLE_CHOICES, default=ROLE_GUEST)

    created_at = models.DateTimeField(auto_now_add=True)

    
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]  
    # keep username required for compatibility; change if you remove username

    class Meta:
        verbose_name = "user"
        verbose_name_plural = "users"
        indexes = [
            models.Index(fields=["email"], name="idx_user_email"),
        ]

    def __str__(self):
        return f"{self.email}"
