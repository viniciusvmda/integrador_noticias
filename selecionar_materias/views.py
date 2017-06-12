from django.shortcuts import render, redirect
from .models import AgenciaNoticias, Materia
from django.contrib import messages
from random import randint
from django.contrib.auth.decorators import login_required
from utils.utils import VariaveisTeste  

import re
import datetime


class ConexaoAgenciaNoticias:

	def autenticacao(self,caso_teste):
		if caso_teste == VariaveisTeste.TESTE_SUCESSO.value:
			return True
		elif caso_teste == VariaveisTeste.TESTE_ERRO.value:
			return False
		elif randint(1, 100) > 50:
			return True
		return False

	def selecao_materias(self):
		materias_agencia_noticias = AgenciaNoticias.objects.all()
		materias_ja_cadastradas = [ m.conteudo for m in Materia.objects.all() ]
		novas_materias = []
		for m in materias_agencia_noticias:
			if m.conteudo not in materias_ja_cadastradas:
				novas_materias.append(m)
		return novas_materias

	transferencia = nova_transferencia = autenticacao


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


@login_required(login_url="/")
def selecao(request):

	materias_agencia_noticias = None
	conexao_agencia_noticias = ConexaoAgenciaNoticias()
	caso_teste = VariaveisTeste.FUNCIONAMENTO_NORMAL.value
	segunda_tentativa = VariaveisTeste.TESTE_SUCESSO.value

	if request.method == 'POST':
		if 'caso_teste' in request.POST:
			caso_teste = request.POST['caso_teste'] 
			caso_teste = int(caso_teste)
		if 'importar_materias' in request.POST:
			if conexao_agencia_noticias.autenticacao(caso_teste):

				materias_agencia_noticias = conexao_agencia_noticias.selecao_materias()
				return render(request, 'selecao.html', {'materias_agencia_noticias': materias_agencia_noticias})
			else:
				messages.warning(request, 'Ocorreu um erro na autenticação. Caso o problema persista contate o setor de suporte técnico.')
				return render(request, 'selecao.html', {})

		elif 'exportar_materias' in request.POST:
			if conexao_agencia_noticias.transferencia(caso_teste):

				if salvar_materia(request.POST):
					messages.success(request, 'Transferência de matérias foi realizada com sucesso.')
				else:
					messages.warning(request, 'A transferência não pode ser efetuada. Tente novamente mais tarde.')
					
			else:
				if 'segunda_tentativa' in request.POST:
					segunda_tentativa = request.POST['segunda_tentativa'] 
					segunda_tentativa = int(segunda_tentativa)

				messages.warning(request, 'A transferência das matérias está incompleta. Serão feitas três novas tentativas de transferência. Por favor aguarde.')

				if conexao_agencia_noticias.nova_transferencia(segunda_tentativa):

					if salvar_materia(request.POST):
						messages.success(request, 'Transferência de matérias realizada com sucesso.')
					else:
						messages.warning(request, 'A transferência não pode ser efetuada. Tente novamente mais tarde.')

				else:

					messages.warning(request, 'A transferência não pode ser efetuada. Tente novamente mais tarde.')
				return render(request, 'selecao.html', {})
		return redirect('/selecao')




	context = {'materias_agencia_noticias': materias_agencia_noticias}

	return render(request, 'selecao.html', context)
