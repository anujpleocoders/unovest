from django import forms
from django.contrib.auth.models import User



class ChangePasword(forms.Form):
    new_pasword = forms.CharField(max_length=100, widget=forms.PasswordInput)
    confirm_pasword = forms.CharField(max_length=100, widget=forms.PasswordInput)

    class Meta:
        model = User