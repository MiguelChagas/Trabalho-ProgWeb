from django.contrib import admin
from .models import Categoria, ContaBancaria, Transacao, Orcamento

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'tipo', 'usuario', 'cor')
    list_filter = ('tipo', 'usuario')
    search_fields = ('nome',)

@admin.register(ContaBancaria)
class ContaBancariaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'usuario', 'saldo_inicial')
    list_filter = ('usuario',)
    search_fields = ('nome',)

@admin.register(Transacao)
class TransacaoAdmin(admin.ModelAdmin):
    list_display = ('descricao', 'valor', 'data', 'tipo', 'categoria', 'conta', 'usuario')
    list_filter = ('tipo', 'data', 'categoria', 'usuario')
    search_fields = ('descricao',)
    date_hierarchy = 'data'

@admin.register(Orcamento)
class OrcamentoAdmin(admin.ModelAdmin):
    list_display = ('categoria', 'mes', 'ano', 'valor_limite', 'usuario')
    list_filter = ('mes', 'ano', 'usuario', 'categoria')