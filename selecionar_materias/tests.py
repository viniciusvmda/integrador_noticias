from django.test import TestCase
from .views import *
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.test import Client


class SelecionarMateriasTest(TestCase):

	def test_acesso_negado_pagina_selecionar_materias(self):	
		c = Client()
		response = c.get('/selecao/')
		self.assertEqual(302,response.status_code)

	def test_acesso_sucesso_pagina_selecionar_materias(self):
		user = User.objects.create_user(username='jornalista', password='jornalista')
		c = Client()
		c.login(username='jornalista', password='jornalista')
		response = c.get('/selecao/')
		self.assertEqual(200,response.status_code)
		self.assertIn('Selecionar matérias para inserção no sistema', response.content.decode())

	def test_importar_materias_sucesso(self):
		# Nao da certo o post
		user = User.objects.create_user(username='jornalista', password='jornalista')
		c = Client()
		c.login(username='jornalista', password='jornalista')
		response = c.post('/selecao/')

