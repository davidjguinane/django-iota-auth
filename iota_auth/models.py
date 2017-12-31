from django.db import models
from django.core.mail import send_mail
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.hashers import (
	check_password, is_password_usable, make_password,
)

from six import binary_type

"""
This module allows importing AbstractBaseUser even when django.contrib.auth is
not in INSTALLED_APPS.
"""
import unicodedata

from django.contrib.auth import password_validation
from django.contrib.auth.hashers import (
	check_password, is_password_usable, make_password,
)
from django.db import models
from django.utils.crypto import get_random_string, salted_hmac
from django.utils.translation import gettext_lazy as _

from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser, PermissionsMixin


class IotaBaseUserManager(BaseUserManager):

	def make_random_password(self, length=81,
							 allowed_chars='ABCDEFGHJKLMNPQRSTUVWXYZ9'):
		"""
		Generate a random password with the given length and given
		allowed_chars. The default value of allowed_chars does not have "I" or
		"O" or letters and digits that look similar -- just to avoid confusion.
		"""
		return get_random_string(length, allowed_chars)

class IotaUserManager(IotaBaseUserManager):
	use_in_migrations = True

	def _create_user(self, email, password, **extra_fields):
		"""Create and save a User with the given email and password."""
		if not email:
			raise ValueError('The given email must be set')
		email = self.normalize_email(email)
		user = self.model(email=email, **extra_fields)
		user.set_password(password)
		user.save(using=self._db)
		return user

	def create_user(self, email, password=None, **extra_fields):
		"""Create and save a regular User with the given email and password."""
		extra_fields.setdefault('is_staff', False)
		extra_fields.setdefault('is_superuser', False)
		return self._create_user(email, password, **extra_fields)

	def create_superuser(self, email, password, **extra_fields):
		"""Create and save a SuperUser with the given email and password."""
		extra_fields.setdefault('is_staff', True)
		extra_fields.setdefault('is_superuser', True)

		if extra_fields.get('is_staff') is not True:
			raise ValueError('Superuser must have is_staff=True.')
		if extra_fields.get('is_superuser') is not True:
			raise ValueError('Superuser must have is_superuser=True.')

		return self._create_user(email, password, **extra_fields)

class User(AbstractUser):

	username = None
	password = models.CharField(_('password'), max_length=128, unique=True)
	address = models.CharField(_('address'), max_length=128, blank=True)
	email = models.EmailField(_('email address'), blank=True, unique=True)
	first_name = models.CharField(_('first name'), max_length=30, blank=True)
	last_name = models.CharField(_('last name'), max_length=30, blank=True)
	date_joined = models.DateTimeField(_('date joined'), auto_now_add=True)
	is_staff = models.BooleanField(_('staff status'),default=False,help_text=_('Designates whether the user can log into this admin site.'),)
	is_active = models.BooleanField(_('active'),default=True,help_text=_('Designates whether this user should be treated as active. Unselect this instead of deleting accounts.'),)
	avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)

	objects = IotaUserManager()

	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = ['password']

	class Meta:
		verbose_name = _('user')
		verbose_name_plural = _('users')

	def get_email(self):
		return self.email

	def get_full_name(self):
		full_name = '%s %s' % (self.first_name, self.last_name)
		return full_name.strip()

	def get_short_name(self):
		return self.first_name

	def email_user(self, subject, message, from_email=None, **kwargs):
		send_mail(subject, message, from_email, [self.email], **kwargs)

	# this methods are require to login super user from admin panel
	def has_perm(self, perm, obj=None):
		return self.is_staff
 
	# this methods are require to login super user from admin panel
	def has_module_perms(self, app_label):
		return self.is_staff

	@property
	def is_anonymous(self):
		return False

	@property
	def is_authenticated(self):
		return True