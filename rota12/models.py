from django.db import models
from django.conf import settings

class Entidade(models.Model):
    TIPO_ENTIDAE = (
        ('R', 'Remetente'),
        ('D', 'Destinatário'),
        ('T', 'Tomadora')
    )
    TIPO_PESSOA = (
        ('F', 'Física'),
        ('J', 'Juridica')
    )

    Nome = models.CharField(max_length=300)
    TipoPessoa = models.CharField(max_length=1, choices=TIPO_PESSOA, blank=False, null=False, default='F')
    CpfCnpj = models.CharField(max_length=14, unique=True)
    Estado = models.CharField(max_length=2)
    Cidade = models.CharField(max_length=150)
    Bairro = models.CharField(max_length=300)
    Endereco = models.CharField(max_length=300)
    Cep = models.CharField(max_length=9)
    TipoEntidade = models.CharField(max_length=1, choices=TIPO_ENTIDAE, blank=False, null=False, default='R')
    Email = models.CharField(max_length=300)
    Telefone = models.CharField(max_length=15) # FORMATO (DD) 91234-5678
    Saldo = models.DecimalField(max_digits=15, decimal_places=2, null=False, blank=False, default=0)

    def __str__(self):
        return self.Nome

class EntidadeUser(models.Model):
    Entidade = models.ForeignKey(Entidade, on_delete=models.CASCADE)
    User = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        )

class Parametro(models.Model):
    Codigo = models.IntegerField(default=0, blank=False, null=False)
    Acesso = models.CharField(max_length=100, blank=False, null=False, default='ACESSO')
    Conteudo = models.CharField(max_length=500, blank=False, null=False, default='CONTEUDO')
    ValorUm = models.DecimalField(max_digits=15, decimal_places=2, null=False, blank=False, default=0)
    ValorDois = models.DecimalField(max_digits=15, decimal_places=2, null=False, blank=False, default=0)
    ValorTres = models.DecimalField(max_digits=15, decimal_places=2, null=False, blank=False, default=0)

    def __str__(self):
        return self.Codigo