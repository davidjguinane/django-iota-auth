# Django-Iota-Auth #

Out of the box Django ships with a User authentication backend that is suitable for many development cases. `iota-auth` is a custom User authentication backend that maintains much of core Django functionality that site developers desire, while providing the ability to connect the User to the IOTA Tangle, and develop IOTA web applications with the Django web development framework. It includes:

1. Custom seed validator
2. [Encrytpted session cookies](https://github.com/brightinteractive/django-encrypted-cookie-session) to store the User's seed in Django's session framework securely, allowing access to the IOTA Tangle using the [PyOTA library](https://github.com/iotaledger/iota.lib.py)
2. Custom authentication backend which integrates with Django's admin interface

# Disclaimer #

WARNING! `iota-auth` saves your IOTA seed in the Django sessions framework. To make this secure, Encrypted Cookie Sessions have been implemented. However I have not tested security in production. Use at your own risk. I have been developing with a 'trial' seed in a empty or relatively empty wallet to ensure no wallets with significant balances are compromised. 

# Adding DIA to your project #

`iota-auth` is currently in development and has only been tested in new projects. Adding to an existing project may be unstable or cause unwanted consequences. To be tested.

You'll need Django X.X or greater and Python X.X are supported.

Install the module and its dependencies with pip:

```
pip install iota-auth
```

`iota-auth` relies on the `django-encrypted-session-cookie` module. Follow the installation instructions [here](https://github.com/brightinteractive/django-encrypted-cookie-session) for setup. The settings that needs to be configured are:

```
SESSION_ENGINE = 'encrypted_cookies'
ENCRYPTED_COOKIE_KEYS = ['your_key_here']
SESSION_COOKIE_SECURE = False #in development, True in production
```

Add the following configuration settings to your 'settings.py' file. Setting the 'AUTH_USER_MODEL' setting to point to 'django-iota-auth':

```
AUTH_USER_MODEL = 'iota_auth.User'
```

Add `iota-auth` to the `AUTHENTICATION_BACKENDS` setting:

```
AUTHENTICATION_BACKENDS = (
    'iota_auth.backend.IotaAuthBackend',
    'django.contrib.auth.backends.ModelBackend',
    ...
    )
```

Set a default IOTA Node to connect to. This may be your own full node, or you can connect to a list of nodes [here](http://iotasupport.com/lightwallet.shtml) that were made for the IOTA lightwallets. 

```
NODE_URI = 'http://iota.bitfinex.com:80/'
```

Other settings you can customise are:

```
LOGIN_URL = '<your_login_view_here>'
LOGIN_REDIRECT_URL = 'your_view_here'
LOGOUT_REDIRECT_URL = 'your_view_here'
```

# Connect a User to the Tangle #

Connecting a User to the Tangle is easy. An example is given below of returning the IOTA account data associated with the logged in User:

```
# urls.py

from .views import (
    AccountDetailView, 
    ...
    )

app_name = 'iota_account'
urlpatterns = [
    path('account/', AccountDetailView.as_view(), name='account'),
    ...
]

# views.py
from iota import Iota

from django.shortcuts import render
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View

class AccountDetailView(LoginRequiredView, View):

    template_name = 'iota_account/wallet.html'

    def get_template_name(self):
        return self.template_name   

    def connect_to_tangle(self, request):
        api = Iota(settings.NODE_URI, request.session['seed'])
        print(api.get_node_info())
        return api

    def get(self, request, *args):
        api = self.connect_to_tangle(request)
        data = api.get_account_data()
        context = { 'data' : data }
        return render(request, self.get_template_name(), context)

# wallet.html

{% extends 'base.html' %}

{% block body %}
<div>Balance: {{ data.balance }}</div>
<div>Address: {{ data.address }}</div>
<div>Bundles: {{ data.bundles }}</div>
{% endblock %}
```