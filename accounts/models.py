from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class User(AbstractUser):
    username = None
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(null=False, blank=False, unique=True)
    phone = PhoneNumberField(null=False, blank=False, unique=True)
    role = models.SmallIntegerField(default=1)
    department = models.TextField(null=True, blank=True)  # For doctors
    status = models.fields.SmallIntegerField(default=1)
    password = models.CharField(max_length=200)
    is2FAEnabled = models.BooleanField(default=False)
    lastLogin = models.DateTimeField(default=None, null=True)
    photo = models.ImageField(upload_to="profile", null=True, default="profile/avatar.png")
    lastUpdated = models.DateTimeField(auto_now=True, editable=False)
    dateCreated = models.DateTimeField(auto_now_add=True, editable=False)
    REQUIRED_FIELDS = ['first_name', 'last_name']
    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'

    def __str__(self):
        if self is None:
            return "None"
        else:
            return self.first_name + " " + self.last_name
    pass

# TODO: Generalize the treatments to more than one doctor
