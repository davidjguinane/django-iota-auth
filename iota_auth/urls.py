from django.urls import path, include

from project.iota_auth import views
from .views import (
	LoginView, 
	SignupView,
	AuthenticatedView,
	)

app_name = 'iota_auth'
urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('signup/', SignupView.as_view(), name='signup'),
    path('authenticated/', AuthenticatedView.as_view(), name='authenticated'),
]
