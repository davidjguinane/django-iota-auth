# Usage #

## Connect a User to the Tangle ##

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