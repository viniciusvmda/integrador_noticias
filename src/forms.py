from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

class LoginForm(forms.Form):
	username = forms.CharField(widget=forms.TextInput(
		attrs={'class': 'form-control', 'placeholder' : 'Email'}))
	password = forms.CharField(widget=forms.PasswordInput(
		attrs={'class': 'form-control', 'placeholder' : 'Password'}))

	def authenticate(self, request):
		username = self.cleaned_data.get('username')
		password = self.cleaned_data.get('password')
		user = authenticate(username=username, password=password)
		return user