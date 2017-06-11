from django.shortcuts import render, redirect
from .models import AgenciaNoticias, Materia
from django.contrib import messages
from random import randint

import re
import datetime


class ConexaoAgenciaNoticias:

	def autenticacao(self):
		if randint(1, 100) > 50:
			return True
		return False

	def transferencia(self):
		if randint(1, 100) > 50:
			return True
		return False

	def nova_transferencia(self):
		for count in range(0,3):
			if randint(1, 100) > 50:
				return True	
		return False


def salvar_materia(POST_dict, materia_exportar):
	materia = Materia(titulo=materia_exportar.replace('-materia-', '').replace('_', ' '),
					  conteudo=POST_dict[materia_exportar],
					  publicada=0,
					  data_importacao=datetime.datetime.now())
	materia.save()


def selecao(request):

	materias_agencia_noticias = None
	conexao_agencia_noticias = ConexaoAgenciaNoticias()

	if request.method == 'POST':

		if 'importar_materias' in request.POST:

			if conexao_agencia_noticias.autenticacao():
				materias_agencia_noticias = AgenciaNoticias.objects.all()

				return render(request, 'selecao.html', {'materias_agencia_noticias': materias_agencia_noticias})

			else:
				messages.warning(request, 'Ocorreu um erro na autenticação. Caso o problema persista, contate o setor de suporte técnico.')


		# 'exportar_materias' in request.POST
		else:

			for materia_exportar in request.POST:
				if re.search('-materia-', materia_exportar):

					if conexao_agencia_noticias.transferencia():
						salvar_materia(request.POST, materia_exportar)
						messages.success(request, 'Transferência de matérias realizada com sucesso.')
					
					else:
						messages.warning(request, 'A transferência das matérias está incompleta. Serão feitas três novas tentativas de transferência. Por favor aguarde.')
						if conexao_agencia_noticias.nova_transferencia():
							salvar_materia(request.POST, materia_exportar)
							messages.success(request, 'Transferência de matérias realizada com sucesso.')
						else:
							messages.warning(request, 'A transferência não pode ser efetuada. Tente novamente mais tarde.')

			return redirect('/selecao')



	context = {'materias_agencia_noticias': materias_agencia_noticias}

	return render(request, 'selecao.html', context)
