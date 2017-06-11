from django.shortcuts import render, redirect
from .models import AgenciaNoticias
from django.contrib import messages


def selecao(request):

	materias_agencia_noticias = None

	if request.method == 'POST':

		if 'importar_materias' in request.POST:

			materias_agencia_noticias = AgenciaNoticias.objects.all()

			return render(request, 'selecao.html', {'materias_agencia_noticias': materias_agencia_noticias})

		# 'exportar_materias' in request.POST
		else:
			messages.success(request, 'Transferência de matérias realizada com sucesso.')
			return redirect('/selecao')



	context = {'materias_agencia_noticias': materias_agencia_noticias}

	return render(request, 'selecao.html', context)
