from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator


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
    valor = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0.01, message='O valor deve ser maior que zero.')]
    )
    data = models.DateField()
    tipo = models.CharField(max_length=1, choices=TIPO_CHOICES)

    def clean(self):
        if self.categoria_id and self.tipo and self.categoria.tipo != self.tipo:
            raise ValidationError(
                f'O tipo da transação ("{self.get_tipo_display()}") deve corresponder '
                f'ao tipo da categoria ("{self.categoria.get_tipo_display()}").'
            )

    def __str__(self):
        return self.descricao


class Orcamento(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orcamentos')
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name='orcamentos')
    mes = models.IntegerField(validators=[
        MinValueValidator(1, message='Mês deve ser entre 1 e 12.')
    ])
    ano = models.IntegerField(validators=[
        MinValueValidator(2000, message='Ano deve ser 2000 ou posterior.')
    ])
    valor_limite = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0.01, message='O valor limite deve ser maior que zero.')]
    )

    class Meta:
        unique_together = ['usuario', 'categoria', 'mes', 'ano']

    def clean(self):
        if self.mes and not (1 <= self.mes <= 12):
            raise ValidationError({'mes': 'Mês deve ser um valor entre 1 e 12.'})

    def __str__(self):
        return f"{self.categoria.nome} - {self.mes}/{self.ano}"