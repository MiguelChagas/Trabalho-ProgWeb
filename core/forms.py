from django import forms
from .models import Transacao, Categoria, ContaBancaria, Orcamento

class TransacaoForm(forms.ModelForm):
    class Meta:
        model = Transacao
        fields = ['descricao', 'valor', 'data', 'tipo', 'categoria', 'conta']
        widgets = {
            'descricao': forms.TextInput(attrs={'class': 'form-control'}),
            'valor': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'data': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'tipo': forms.Select(attrs={'class': 'form-select'}),
            'categoria': forms.Select(attrs={'class': 'form-select'}),
            'conta': forms.Select(attrs={'class': 'form-select'}),
        }

class CategoriaForm(forms.ModelForm):
    pass

class ContaBancariaForm(forms.ModelForm):
    pass

class OrcamentoForm(forms.ModelForm):
    pass