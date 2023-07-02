from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .managers import CustomUserManager

# Create your models here.


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        verbose_name="Email Adress", max_length=255, unique=True)
    first_name = models.CharField(max_length=255, blank=True)
    phone = models.CharField(max_length=10, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    joined_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    # Email & Password are required by default.
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email
    @property
    def name(self):
        return self.first_name
    
    def natural_key(self):
        return (self.email,)

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    # def check_object_permissions(self, request, obj):
    #     """
    #     Check if the request should be permitted for a given object.
    #     Raises an appropriate exception if the request is not permitted.
    #     """
    #     for permission in self.get_permissions():
    #         if not permission.has_object_permission(request, self, obj):
    #             self.permission_denied(request)
