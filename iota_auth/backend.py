from django.conf import settings
from django.contrib.auth.hashers import check_password
from django.contrib.auth import get_user_model

class IotaAuthBackend:

	def authenticate(self, request, username=None, password=None, **kwargs):
		User = get_user_model()
		try:
			user = User.objects.get(email=username)
		except User.DoesNotExist:
			return None
		else:
			if getattr(user, 'is_active', False) and  user.check_password(password):
				request.session['seed'] = password
				return user
		return None

	def get_user(self, user_id):
		User = get_user_model()        
		try:
			return User.objects.get(pk=user_id)
		except User.DoesNotExist:
			return None
