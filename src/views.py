from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, get_user, authenticate
from .forms import LoginForm
from django.http import HttpResponseForbidden

# Create your views here.
def main(request):
	if request.user.is_authenticated:
		return redirect('/home')
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

def selecao(request):
	return render (request, "selecao.html", {})

def classificacao(request):
	return render (request, "classificacao.html", {})

def sair(request):
	user = get_user(request)
	logout(request)
	return redirect('/')