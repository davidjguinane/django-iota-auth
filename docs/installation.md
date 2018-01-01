# Installation #

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
LOGIN_REDIRECT_URL = 'your_view_here'
LOGOUT_REDIRECT_URL = 'your_view_here'
```
