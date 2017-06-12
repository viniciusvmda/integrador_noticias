from django.test import TestCase
from .views import *
from django.contrib.auth.models import User
from selecionar_materias.models import Materia, Caderno
from django.contrib.auth import login, authenticate
from django.test import Client
from datetime import datetime


class SelecionarMateriasTest(TestCase):

	def test_acesso_negado_pagina_classificar_materias(self):	
		c = Client()
		response = c.get('/classificacao/')
		self.assertEqual(302,response.status_code)

	def test_acesso_sucesso_pagina_classificar_materias(self):
		user = User.objects.create_user(username='jornalista', password='jornalista')
		c = Client()
		c.login(username='jornalista', password='jornalista')
		response = c.get('/classificacao/')
		self.assertEqual(200,response.status_code)
		self.assertIn('Classificar matérias', response.content.decode())

	def test_sucesso_associar_materia(self):
		user = User.objects.create_user(username='jornalista', password='jornalista')
		materia = Materia.objects.create(id='1', caderno=None, titulo='titulo', publicada=0, conteudo='conteudo', data_importacao=datetime.today())
		caderno = Caderno.objects.create(id='3', descricao='Esportes')
		c = Client()
		c.login(username='jornalista', password='jornalista')
		post_data = {
	        'materia_id': '1',
	        'caderno_id': '3',
		}
		response = c.post('/classificacao/', post_data)
		self.assertEqual(200, response.status_code)
		self.assertIn('Cadastro realizado com sucesso!', response.content.decode())
		

