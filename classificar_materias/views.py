from django.shortcuts import render, redirect
from selecionar_materias.models import Materia, Caderno
from django.db.models import Q
from django.contrib.auth.decorators import login_required


@login_required(login_url="/")
def classificacao(request):
    materias = Materia.objects.filter(Q(publicada=0) & Q(caderno=None)).order_by('data_importacao')
    cadernos = Caderno.objects.all()

    if request.method == 'POST':
        materia_id = request.POST['materia_id']
        caderno_id = request.POST['caderno_id']
        materia = Materia.objects.get(id=materia_id)
        caderno = Caderno.objects.get(id=caderno_id)
        materia.caderno = caderno
        materia.save()

    return render (request, "classificacao.html", {
        'materias': materias,
        'cadernos': cadernos
    })