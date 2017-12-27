1. Install Django Iota Auth

	pip install django-iota-auth

1. Add "django-iota-auth" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'django-iota-auth',
    ]

2. Include the 'django-iota-auth' URLconf in your project urls.py like this::

    path('iota-auth/', include('django-iota-auth.urls')),

3. Add the following configuration settings to your 'settings.py' file:

You need to tell Django to use the django-iota-auth User model.
x
AUTH_USER_MODEL = 'iota_auth.User'

And let 

AUTHENTICATION_BACKENDS = (
    'project.iota_auth.backend.IotaAuthBackend',
    'django.contrib.auth.backends.ModelBackend',
    )

When developing with Iota, you need to connect to a node. The default node is 'http://iota.bitfinex.com:80/'. To connect to a different node, override the NODE_URI setting with a different node: 

NODE_URI = 'http://<different_node_here>:14265/'

To customize where the User is redirected to after logging in or signing up, set the LOGIN_REDIRECT_URL and SIGNUP_REDIRECT_URL.

4. Run `python manage.py migrate` to create the custom User models.
