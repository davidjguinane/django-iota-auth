from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import Group
from django.contrib.auth.forms import ReadOnlyPasswordHashField
 
from .models import User
 
class UserCreationForm(forms.ModelForm):
    #A form for creating new users. Includes all the required
    #fields, plus a repeated password.
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
 
    class Meta:
        model = User
        fields = ('email',)
 
    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user
 
 
class UserChangeForm(forms.ModelForm):
    #A form for updating users. Includes all the fields on
    #the user, but replaces the password field with admin's
    #password hash display field.
    
    password = ReadOnlyPasswordHashField()
 
    class Meta:
        model = User
        fields = ('email', 'password', 'address', 'first_name', 'last_name', 'is_active','is_staff')
 
    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]
 
 
class UserAdmin(DjangoUserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm
 
    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('email', 'first_name', 'last_name', 'is_staff')
    list_filter = ('email',)
    fieldsets = (
        (None, {'fields': ('email', 'password', 'address')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser','user_permissions')}),
        (_('Important dates'), {'fields': ('last_login',)}),
       )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email','password')}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()
 
# Now register the new UserAdmin...
admin.site.register(User, UserAdmin)
# ... and, since we're not using Django's built-in permissions,
# unregister the Group model from admin.
admin.site.unregister(Group)