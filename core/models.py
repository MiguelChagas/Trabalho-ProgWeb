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