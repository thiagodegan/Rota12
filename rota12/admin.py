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

class EntidadeUsers(admin.ModelAdmin):
    list_display = (
        'id', 'Entidade', 'User'
    )
    list_display_links = ('id','Entidade', 'User')

admin.site.register(EntidadeUser, EntidadeUsers)

class Parametros(admin.ModelAdmin):
    list_display = (
        'id', 'Codigo', 'Acesso', 'Conteudo', 'ValorUm', 'ValorDois', 'ValorTres',
    )
    list_display_links = ('id', 'Codigo', 'Acesso')
    search_fields = ('Codigo', 'Acesso')

admin.site.register(Parametro, Parametros)