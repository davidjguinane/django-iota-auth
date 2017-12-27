from django.shortcuts import render, redirect, reverse
from django.http import HttpResponseRedirect
from django.views import View
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.password_validation import validate_password

from project.iota_auth.backend import IotaAuthBackend
from project.iota_auth.forms import (
		SignupForm,
		LoginSeedForm,
	)
from project.iota_auth.utils import seed_generator

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

	def get_template_name(self):
		return self.template_name

	def get_success_url(self):
		return settings.LOGIN_REDIRECT_URL

	def get(self, request):
		form = self.form_class
		context = {'form':form}
		return render(request, self.get_template_name(), context)

	def login_user(self, email, password):
		user = auth.authenticate(email, password)
		if user is not None:
			auth.login(self.request, user, settings.AUTHENTICATION_BACKENDS[0])
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
			self.login_user(email, password)
			return HttpResponseRedirect(reverse('iota_auth:authenticated'))
		else:
			self.form_invalid(form)

class AuthenticatedView(LoginRequiredMixin, View):

	login_url = '/login/'
	redirect_field_name = 'redirect_to'
	template_name = 'iota_auth/authenticated.html'	

	def get_template_name(self):
		return self.template_name	

	def get(self, request):
		return render(request, self.get_template_name())