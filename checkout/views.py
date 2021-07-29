from json.encoder import JSONEncoder
from django.core.serializers.json import DjangoJSONEncoder
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from rota12.models import Entidade, Extrato
import json

@login_required
def cart(request):
    return render(request, 'checkout/cart.html')

@login_required
def cart_post(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        extrato = Extrato.objects.create(Entidade=request.user.entidade,Descricao=data['Descricao'], Valor=data['Valor'])
        extrato.save()
        dados = {
            'result': 'sucesso',
            'message': 'Compra registrada com pendência de pagamento',
            'conteudo': extrato.id,
        }

        return JsonResponse(dados, safe=True, encoder=DjangoJSONEncoder)
    else:
        dados = {
            'result': 'Erro',
            'message': 'Chamada inválida'
        }

        return JsonResponse(dados, encoder=DjangoJSONEncoder, safe=True, status=404)
