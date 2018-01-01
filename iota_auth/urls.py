from django.urls import path, include

from .views import (
	LoginView, 
	SignupView,
	LogoutView,
	AuthenticatedView,
	)

app_name = 'iota_auth'
urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('signup/', SignupView.as_view(), name='signup'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('', AuthenticatedView.as_view(), name='authenticated'),
]