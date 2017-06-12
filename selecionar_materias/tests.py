from django.test import TestCase
from .views import *
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.test import Client
from .models import AgenciaNoticias, Materia
from utils.utils import VariaveisTeste  


class SelecionarMateriasTest(TestCase):
	def setUp(self):
		self.user = User.objects.create_user(username='jornalista', password='jornalista')
		self.c = Client()
		self.c.login(username='jornalista', password='jornalista')
		self.materias_agencia = AgenciaNoticias(titulo="Teste de importacao",conteudo="Conteudo")
		self.materias_agencia.save()

	def test_acesso_negado_pagina_selecionar_materias(self):	
		c = Client()
		response = c.get('/selecao/')
		self.assertEqual(302,response.status_code)

	def test_acesso_sucesso_pagina_selecionar_materias(self):
		response = self.c.get('/selecao/')
		self.assertEqual(200,response.status_code)
		self.assertIn('Selecionar matérias para inserção no sistema', response.content.decode())

	def test_importar_materias_sucesso(self):
		response = self.c.post('/selecao/',{'importar_materias' : [''],'caso_teste' : VariaveisTeste.TESTE_SUCESSO.value})
		self.assertIn('Teste de importacao',response.content.decode())
		self.assertIn('Conteudo',response.content.decode())
	
	def test_importar_materias_insucesso(self):
		response = self.c.post('/selecao/',{'importar_materias' : [''],'caso_teste' : VariaveisTeste.TESTE_ERRO.value})
		self.assertIn('Ocorreu um erro na autenticação. Caso o problema persista contate o setor de suporte técnico.',response.content.decode())

	def test_exportar_materias_sucesso(self):
		response = self.c.post('/selecao/',{'exportar_materias' : [''],'-materia-Teste de importacao':'Conteudo','caso_teste' : VariaveisTeste.TESTE_SUCESSO.value})	
		materia = Materia.objects.filter(titulo=self.materias_agencia.titulo)
		self.assertTrue(materia.exists())

	def test_exportar_materias_sucesso_com_ressalva(self):
		response = self.c.post('/selecao/',{'exportar_materias' : [''],'-materia-Teste de importacao':'Conteudo','caso_teste' : VariaveisTeste.TESTE_ERRO.value,'segunda_tentativa' : VariaveisTeste.TESTE_SUCESSO.value})	
		self.assertIn('A transferência das matérias está incompleta. Serão feitas três novas tentativas de transferência. Por favor aguarde.',response.content.decode())
		self.assertIn('Transferência de matérias realizada com sucesso.',response.content.decode())
		materia = Materia.objects.filter(titulo=self.materias_agencia.titulo)
		self.assertTrue(materia.exists())

	def test_exportar_insucesso(self):
		response = self.c.post('/selecao/',{'exportar_materias' : [''],'-materia-Teste de importacao':'Conteudo','caso_teste' : VariaveisTeste.TESTE_ERRO.value,'segunda_tentativa' : VariaveisTeste.TESTE_ERRO.value})	
		self.assertIn('A transferência das matérias está incompleta. Serão feitas três novas tentativas de transferência. Por favor aguarde.',response.content.decode())
		self.assertIn('A transferência não pode ser efetuada. Tente novamente mais tarde.',response.content.decode())
		