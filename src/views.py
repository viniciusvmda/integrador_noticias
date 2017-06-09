from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login,logout,get_user
from .forms import LoginForm
from django.http import HttpResponseForbidden

# Create your views here.
def main(request):
	if request.method == "POST":
		loginForm = LoginForm(request.POST or None)
		if(loginForm.is_valid()):
			user = loginForm.authenticate(request)
			if(user):
				login(request,user)
				return render(request,"index.html",[])
			else:
				loginForm = LoginForm(None)
				return render(request,"login.html",{'loginForm' : LoginForm})
		else:
			loginForm = LoginForm(None)
			return render(request,"login.html",{'loginForm' : LoginForm})
	else:
		loginForm = LoginForm(None)
		return render(request,"login.html",{'loginForm' : LoginForm})

def index(request):
	if request.user.is_authenticated:
		return render(request,"index.html",[])
	else:
		return HttpResponseForbidden()

def sair(request):
	user = get_user(request)
	logout(request)
	loginForm = LoginForm(None)
	return render(request,"login.html",{'loginForm' : LoginForm})