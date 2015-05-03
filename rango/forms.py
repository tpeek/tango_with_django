from django import forms
from rango.models import UserProfile
from django.contrib.auth.models import User


# A form for making User objects.
class UserForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput())
    email = forms.CharField(widget=forms.TextInput())
    password = forms.CharField(widget=forms.PasswordInput(render_value=True))

    class Meta:
        model = User
        fields = ('username', 'password', 'email')


# A form for making UserProfile objects.
class UserProfileForm(forms.ModelForm):
    first_name = forms.CharField(widget=forms.TextInput())
    last_name = forms.CharField(widget=forms.TextInput(), required=False)
    website = forms.CharField(widget=forms.TextInput(), required=False)
    
    class Meta:
        model = UserProfile
        fields = ('first_name', 'last_name', 'website', 'picture')

