from django.contrib import admin
from rota12.models import *

# Register your models here.
class Entidades(admin.ModelAdmin):
    list_display = (
        'id', 'Nome', 'TipoPessoa', 'CpfCnpj',
        'Estado', 'Cidade', 'Bairro', 'Endereco',
        'Cep', 'TipoEntidade', 'Email', 'Telefone', 
        'Saldo',
        )
    list_display_links = ('id', 'Nome', 'CpfCnpj')
    search_fields = ('Nome','CpfCnpj')
    list_per_page = 20

admin.site.register(Entidade, Entidades)

class Parametros(admin.ModelAdmin):
    list_display = (
        'id', 'Codigo', 'Acesso', 'Conteudo', 'ValorUm', 'ValorDois', 'ValorTres',
    )
    list_display_links = ('id', 'Codigo', 'Acesso')
    search_fields = ('Codigo', 'Acesso')

admin.site.register(Parametro, Parametros)

class Extratos(admin.ModelAdmin):
    list_display = (
        'id', 'Entidade', 'Data', 'Descricao', 'CreditoDebito', 'Valor',
    )
    list_display_links = ('id', 'Entidade', 'Data')
    search_fields = ('Entidade__Nome', 'Data')
    list_per_page = 20

admin.site.register(Extrato, Extratos)