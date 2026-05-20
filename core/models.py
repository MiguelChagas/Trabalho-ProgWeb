from django.db import models
from django.contrib.auth.models import User

class Categoria(models.Model):
    TIPO_CHOICES = [
        ('R', 'Receita'),
        ('D', 'Despesa'),
    ]
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='categorias')
    nome = models.CharField(max_length=100)
    tipo = models.CharField(max_length=1, choices=TIPO_CHOICES)
    icone = models.CharField(max_length=50, blank=True, null=True)
    cor = models.CharField(max_length=7, default='#000000')

    def __str__(self):
        return self.nome

class ContaBancaria(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='contas')
    nome = models.CharField(max_length=100)
    saldo_inicial = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return self.nome

class Transacao(models.Model):
    TIPO_CHOICES = [
        ('R', 'Receita'),
        ('D', 'Despesa'),
    ]
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transacoes')
    categoria = models.ForeignKey(Categoria, on_delete=models.RESTRICT, related_name='transacoes')
    conta = models.ForeignKey(ContaBancaria, on_delete=models.SET_NULL, null=True, blank=True, related_name='transacoes')
    descricao = models.CharField(max_length=255)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    data = models.DateField()
    tipo = models.CharField(max_length=1, choices=TIPO_CHOICES)

    def __str__(self):
        return self.descricao

class Orcamento(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orcamentos')
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name='orcamentos')
    mes = models.IntegerField()
    ano = models.IntegerField()
    valor_limite = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        unique_together = ['usuario', 'categoria', 'mes', 'ano']

    def __str__(self):
        return f"{self.categoria.nome} - {self.mes}/{self.ano}"