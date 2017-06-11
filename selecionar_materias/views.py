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

	def sem_noticias(self):
		if AgenciaNoticias.objects.all():
			return False
		return True

	def selecao_materias(self):
		materias_agencia_noticias = AgenciaNoticias.objects.all()
		materias_ja_cadastradas = [ m.conteudo for m in Materia.objects.all() ]
		novas_materias = []
		for m in materias_agencia_noticias:
			if m.conteudo not in materias_ja_cadastradas:
				novas_materias.append(m)
		return novas_materias

	def transferencia(self):
		if randint(1, 100) > 50:
			return True
		return False

	def nova_transferencia(self):
		for count in range(0,3):
			if randint(1, 100) > 50:
				return True	
		return False


def salvar_materia(POST_dict):

	try:
		for materia_exportar in POST_dict:
			if re.search('-materia-', materia_exportar):
				materia = Materia(titulo=materia_exportar.replace('-materia-', '').replace('_', ' '),
								  conteudo=POST_dict[materia_exportar],
								  publicada=0,
								  data_importacao=datetime.datetime.now())
				materia.save()
		return True
	except:
		return False


def selecao(request):

	materias_agencia_noticias = None
	lenSemCheckbox = 2
	conexao_agencia_noticias = ConexaoAgenciaNoticias()

	if request.method == 'POST':

		if 'importar_materias' in request.POST:

			if conexao_agencia_noticias.autenticacao():

				if conexao_agencia_noticias.sem_noticias():
					messages.warning(request, 'Não existem novas notícias na Agência de Notícias.')
				else:
					materias_agencia_noticias = conexao_agencia_noticias.selecao_materias()

					if materias_agencia_noticias:
						return render(request, 'selecao.html', {'materias_agencia_noticias': materias_agencia_noticias})
					else:
						messages.warning(request, 'Todas as matérias já foram exportadas.')	

			else:
				messages.warning(request, 'Ocorreu um erro na autenticação. Caso o problema persista contate o setor de suporte técnico.')


		elif 'exportar_materias' in request.POST:

			if len(request.POST) == lenSemCheckbox:
				messages.warning(request, 'Nenhuma matéria foi selecionada para exportação.')
			else:

				if conexao_agencia_noticias.transferencia():

					if salvar_materia(request.POST):
						messages.success(request, 'Transferência de matérias foi realizada com sucesso.')
					else:
						messages.warning(request, 'A transferência não pode ser efetuada. Tente novamente mais tarde.')
						
				else:

					messages.warning(request, 'A transferência das matérias está incompleta. Serão feitas três novas tentativas de transferência. Por favor aguarde.')

					if conexao_agencia_noticias.nova_transferencia():

						if salvar_materia(request.POST):
							messages.success(request, 'Transferência de matérias realizada com sucesso.')
						else:
							messages.warning(request, 'A transferência não pode ser efetuada. Tente novamente mais tarde.')

					else:

						messages.warning(request, 'A transferência não pode ser efetuada. Tente novamente mais tarde.')

		return redirect('/selecao')



	context = {'materias_agencia_noticias': materias_agencia_noticias}

	return render(request, 'selecao.html', context)
