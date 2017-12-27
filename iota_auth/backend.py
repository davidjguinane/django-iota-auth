from iota import Iota

from django.conf import settings
from django.middleware.csrf import rotate_token
from django.contrib.auth.signals import user_logged_in, user_logged_out, user_login_failed
from django.contrib.auth.hashers import (
	check_password, is_password_usable, make_password,
)
from django.contrib.auth.__init__ import _get_user_session_key, get_user_model
from django.utils.crypto import constant_time_compare

from project.iota_auth.models import User

SESSION_KEY = '_auth_user_id'
BACKEND_SESSION_KEY = '_auth_user_backend'
HASH_SESSION_KEY = '_auth_user_hash'
REDIRECT_FIELD_NAME = 'next'

class IotaAuthBackend:

	def get_user(self, email):
		try:
			user = User.objects.get(email=email)
			return user
		except User.DoesNotExist:
			return None

	def authenticate(self, email, password):
		# Check the seed exists on the tangle
		user = self.get_user(email)
		if check_password(password, user.password):
			api = Iota(settings.NODE_URI, password)
			#For debugging purposes
			print(api.get_node_info())
			return user
		# If the seed doesn't exist, return None or an error	
		else:
			return None

	def login(self, request, user, backend):
		"""
		Persist a user id and a backend in the request. This way a user doesn't
		have to reauthenticate on every request. Note that data set during
		the anonymous session is retained when the user logs in.
		"""
		session_auth_hash = ''
		if user is None:
			user = request.user
		if hasattr(user, 'get_session_auth_hash'):
			session_auth_hash = user.get_session_auth_hash()

		if SESSION_KEY in request.session:
			if _get_user_session_key(request) != user.pk or (
					session_auth_hash and
					not constant_time_compare(request.session.get(HASH_SESSION_KEY, ''), session_auth_hash)):
				# To avoid reusing another user's session, create a new, empty
				# session if the existing session corresponds to a different
				# authenticated user.
				request.session.flush()
		else:
			request.session.cycle_key()

		try:
			backend = backend or user.backend
		except AttributeError:
			backends = _get_backends(return_tuples=True)
			if len(backends) == 1:
				_, backend = backends[0]
			else:
				raise ValueError(
					'You have multiple authentication backends configured and '
					'therefore must provide the `backend` argument or set the '
					'`backend` attribute on the user.'
				)

		request.session[SESSION_KEY] = user._meta.pk.value_to_string(user)
		request.session[BACKEND_SESSION_KEY] = backend
		request.session[HASH_SESSION_KEY] = session_auth_hash
		if hasattr(request, 'user'):
			request.user = user
		rotate_token(request)
		user_logged_in.send(sender=user.__class__, request=request, user=user)


	def logout(request):
		"""
		Remove the authenticated user's ID from the request and flush their session
		data.
		"""
		# Dispatch the signal before the user is logged out so the receivers have a
		# chance to find out *who* logged out.
		user = getattr(request, 'user', None)
		if hasattr(user, 'is_authenticated') and not user.is_authenticated:
			user = None
		user_logged_out.send(sender=user.__class__, request=request, user=user)

		# remember language choice saved to session
		language = request.session.get(LANGUAGE_SESSION_KEY)

		request.session.flush()

		if language is not None:
			request.session[LANGUAGE_SESSION_KEY] = language

		if hasattr(request, 'user'):
			from django.contrib.auth.models import AnonymousUser
			request.user = AnonymousUser()