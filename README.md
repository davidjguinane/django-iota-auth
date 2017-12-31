# Django-Iota-Auth #

Out of the box Django ships with a User authentication backend that is suitable for many development cases. `django-iota-auth` is a custom User authentication backend that maintains much of core Django functionality that site developers desire, while providing the ability to connect the User to the IOTA Tangle, and develop IOTA web applications with the Django web development framework. It includes:

1. Custom seed validator
2. [Encrytpted session cookies](https://github.com/brightinteractive/django-encrypted-cookie-session) to store the User's seed in Django's session framework securely, allowing access to the IOTA Tangle using the [PyOTA library](https://github.com/iotaledger/iota.lib.py)
2. Custom authentication backend which integrates with Django's admin interface

# Adding DIA to your project #

`django-iota-auth` is currently in development and has only been tested in new projects. Adding to an existing project may be unstable or cause unwanted consequences. To be tested.

You'll need Django X.X or greater and Python X.X are supported.

Install the module and its dependencies with pip:

```
pip install django-iota-auth
```

`django-iota-auth` relies on the `django-encrypted-session-cookie` module. Follow the installation instructions [here]](https://github.com/brightinteractive/django-encrypted-cookie-session) for setup. The settings that needs to be configured are:

```
SESSION_ENGINE = 'encrypted_cookies'
ENCRYPTED_COOKIE_KEYS = ['your_key_here']
SESSION_COOKIE_SECURE = False # in development, true in production
```

Add the following configuration settings to your 'settings.py' file. Setting the 'AUTH_USER_MODEL' setting to point to 'django-iota-auth':

```
AUTH_USER_MODEL = 'iota_auth.User'
```

Add `django-iota-auth` to the `AUTHENTICATION_BACKENDS` setting:

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
LOGIN_REDIRECT_URL = 'your_view_here'
LOGOUT_REDIRECT_URL = 'your_view_here'
```

# Connect a User to the Tangle #

Connecting a User to the Tangle is easy. An example is given below of returning the IOTA account data associated with the logged in User:

```
#views.py
from iota import Iota

from django.shortcuts import render
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.contrib.auth import get_user_model

User = get_user_model()

class AccessUsersAccountView(LoginRequiredView, View):

    def connect_to_tangle(self, request):
        api = Iota(settings.NODE_URI, request.session['seed'])
        print(api.get_node_info())
        return api

    def get_account_data(self, api):
        account_data = api.get_account_data()
        return account_data

    def get(self, request, *args):
        api = self.connect_to_tangle(request)
        data = self.get_account_data(api)
        context = { 'data' : data }
        return render(request, self.get_template_name(), context)

```