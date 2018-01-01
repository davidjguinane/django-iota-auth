# Usage #

## Connect a User to the Tangle ##

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