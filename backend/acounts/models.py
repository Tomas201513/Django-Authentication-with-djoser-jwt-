from django.db import models

from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin


class UserAccountManager(BaseUserManager):
    def create_user(self, username,email, password=None, **extra_fields):
        if not email:
            raise ValueError("User must have an email")
        email = self.normalize_email(email)
        user = self.model(email=email,username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user


class UserAccount(AbstractBaseUser, PermissionsMixin):
    # These fields tie to the roles!
    ADMIN = 1
    EMPLOYEE = 2

    ROLE_CHOICES = (
        (ADMIN, 'Admin'),
        (EMPLOYEE, 'Employee')
    )
    

    email = models.EmailField(max_length=255, unique=True)
    username = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    role = models.CharField(max_length=20, default='Employee', choices=ROLE_CHOICES)

    objects = UserAccountManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def get_user_name(self):
        return self.user_name

    def get_short_name(self):
        return self.user_name

    def __str__(self):
        return self.email
