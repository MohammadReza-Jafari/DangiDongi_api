import uuid
import os

from django.db import models
from django.utils.translation import gettext as _
from django.core.exceptions import ValidationError
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.validators import FileExtensionValidator


def get_save_image_path(instance, filename: str):
    ext = filename.split('.')[-1]
    filename = f'{uuid.uuid4()}.{ext}'

    return os.path.join(f'uploads/profiles/{filename}')


class UserManager(BaseUserManager):

    def create_user(self, email, password=None, **kwargs):
        if not email:
            raise ValidationError(
                _('ایمیل اجباری می باشد'),
                code='null'
            )
        user = self.model(email=self.normalize_email(email), **kwargs)
        user.set_password(password)
        user.activation_code = uuid.uuid4()

        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **kwargs):
        user = self.create_user(email, password, **kwargs)
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True
        user.activation_code = None

        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(
        blank=False,
        null=False,
        unique=True,
        verbose_name='email address',
        error_messages={
            'unique': 'کاربری با این ایمیل قبلا ثبت نام کرده است.'
        }
    )
    first_name = models.CharField(max_length=30, null=False, blank=False)
    last_name = models.CharField(max_length=50, null=False, blank=False)
    profile_image = models.ImageField(
        null=True,
        upload_to=get_save_image_path,
        validators=[FileExtensionValidator(allowed_extensions=['jpeg', 'png', 'jpg'])]
    )
    phone_number = models.CharField(null=True, blank=True, max_length=13)
    activation_code = models.CharField(null=True, default=None, max_length=255)
    reset_code = models.IntegerField(null=True, default=None)

    is_active = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.email

