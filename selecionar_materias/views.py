from django.shortcuts import render


def selecao(request):
	return render (request, "selecao.html", {})
