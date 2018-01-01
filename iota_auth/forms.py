from django import forms
from django.conf import settings

from .models import User

class LoginForm(forms.Form):

	password = None
	remember = forms.BooleanField(
		label='Remember Me',
		required=False
		)

class LoginSeedForm(LoginForm):

	password = forms.CharField(
		widget=forms.PasswordInput(),
		label='Seed', 
		max_length=1000
		)
	email = forms.EmailField(
		label='Email'
		)

class SignupForm(forms.Form):
	email = forms.EmailField(
		label='Email'
		)
	first_name = forms.CharField(
		label='First name', 
		max_length=150
		)
	last_name = forms.CharField(
		label='Last name', 
		max_length=150
		)
	seed = forms.CharField(
		widget=forms.PasswordInput(),
		label='Seed', 
		max_length=1000
		)