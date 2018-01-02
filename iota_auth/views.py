from django.shortcuts import render, redirect, reverse
from django.http import HttpResponseRedirect
from django.views import View
from django.conf import settings
from django.contrib.auth import get_user_model, authenticate, login, logout
from django.contrib.auth.password_validation import validate_password
from django.views.decorators.debug import sensitive_post_parameters
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.mixins import LoginRequiredMixin

from .backend import IotaAuthBackend
from .forms import (
		SignupForm,
		LoginSeedForm,
	)

auth = IotaAuthBackend()
User = get_user_model()

class SignupView(View):

	template_name = 'iota_auth/signup.html'
	form_class = SignupForm

	def get_template_name(self):
		return self.template_name

	def get_success_url(self):
		return settings.SIGNUP_REDIRECT_URL

	def get(self, request):
		form = self.form_class
		context = {'form':form}
		return render(request, self.get_template_name(), context)

	def send_email_confirmation(self, email_address):
		email_address.send_confirmation(site=get_current_site(self.request))

	def login_user(self, email, password):
		user = auth.authenticate(email, password)
		if user is not None:
			auth.login(self.request, user, settings.AUTHENTICATION_BACKENDS[0])
			self.request.session.set_expiry(0)
		else:
			print('Error')

	def post(self, request):
		form = self.form_class(request.POST)
		if form.is_valid():
			email = form.cleaned_data['email']
			first_name = form.cleaned_data['first_name']
			last_name = form.cleaned_data['last_name']
			seed = form.cleaned_data['seed']
			validation = validate_password(seed)
			if validation is None:
				user = User.objects.create(email=email, first_name=first_name, last_name=last_name, password=seed)
				user.set_password(seed)
				user.save()
				self.login_user(user.email, seed)
				# send_email_confirmation(user.email):
				return redirect(self.get_success_url())
		else:
			form = self.form_class()


class LoginView(View):

	template_name = 'iota_auth/login.html'
	form_class = LoginSeedForm

	@method_decorator(sensitive_post_parameters())
	@method_decorator(csrf_protect)
	@method_decorator(never_cache)
	def dispatch(self, request, *args, **kwargs):
		return super(LoginView, self).dispatch(request, *args, **kwargs)

	def get_template_name(self):
		return self.template_name

	def get_success_url(self):
		return settings.LOGIN_REDIRECT_URL

	def get(self, request):
		form = self.form_class
		context = {'form':form}
		return render(request, self.get_template_name(), context)

	def login_user(self, request, email=None, password=None):
		user = auth.authenticate(request, username=email, password=password)
		if user is not None:
			login(request, user, settings.AUTHENTICATION_BACKENDS[0])
			self.request.session.set_expiry(0)
		else:
			print('Error')

	# If the email or seed is invalid
	def form_invalid(self, form):
		return super(SignupView, self).form_invalid(form)	

	def post(self, request):
		form = self.form_class(request.POST)
		if form.is_valid():
			password = form.cleaned_data['password']
			email = form.cleaned_data['email']
			self.login_user(self.request, email=email, password=password)
			return redirect(self.get_success_url())
		else:
			self.form_invalid(form)

class LogoutView(LoginRequiredMixin, View):

	template_name = 'iota_auth/logout.html'

	def get_template_name(self):
		return self.template_name

	def get_success_url(self):
		return settings.LOGOUT_REDIRECT_URL

	def get(self, request):
		return render(request, self.get_template_name())

	def post(self, request):
		logout(request)
		return redirect(self.get_success_url())	

class AuthenticatedView(LoginRequiredMixin, View):

	template_name = 'iota_auth/authenticated.html'	

	def get_object(self):
		return self.request.user

	def get_template_name(self):
		return self.template_name	

	def get(self, request, *args):
		return render(request, self.get_template_name())