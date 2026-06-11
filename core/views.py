from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.db.models import Sum
from .models import Transacao, ContaBancaria, Categoria, Orcamento
from .forms import TransacaoForm, CategoriaForm, ContaBancariaForm, OrcamentoForm

@login_required
def dashboard(request):
    transacoes = Transacao.objects.filter(usuario=request.user).order_by('-data')[:5]
    saldo_contas = ContaBancaria.objects.filter(usuario=request.user).aggregate(Sum('saldo_inicial'))['saldo_inicial__sum'] or 0
    receitas = Transacao.objects.filter(usuario=request.user, tipo='R').aggregate(Sum('valor'))['valor__sum'] or 0
    despesas = Transacao.objects.filter(usuario=request.user, tipo='D').aggregate(Sum('valor'))['valor__sum'] or 0

    saldo_total = saldo_contas + receitas - despesas

    context = {
        'transacoes_recentes': transacoes,
        'saldo_total': saldo_total,
        'receitas': receitas,
        'despesas': despesas,
    }
    return render(request, 'core/dashboard.html', context)

class TransacaoListView(LoginRequiredMixin, ListView):
    model = Transacao
    template_name = 'core/transacao_list.html'
    context_object_name = 'transacoes'

    def get_queryset(self):
        return Transacao.objects.filter(usuario=self.request.user).order_by('-data')

class TransacaoCreateView(LoginRequiredMixin, CreateView):
    model = Transacao
    form_class = TransacaoForm
    template_name = 'core/transacao_form.html'
    success_url = reverse_lazy('core:transacao_list')

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['categoria'].queryset = Categoria.objects.filter(usuario=self.request.user)
        form.fields['conta'].queryset = ContaBancaria.objects.filter(usuario=self.request.user)
        return form

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        return super().form_valid(form)

class TransacaoUpdateView(LoginRequiredMixin, UpdateView):
    model = Transacao
    form_class = TransacaoForm
    template_name = 'core/transacao_form.html'
    success_url = reverse_lazy('core:transacao_list')

    def get_queryset(self):
        return Transacao.objects.filter(usuario=self.request.user)

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['categoria'].queryset = Categoria.objects.filter(usuario=self.request.user)
        form.fields['conta'].queryset = ContaBancaria.objects.filter(usuario=self.request.user)
        return form

class TransacaoDeleteView(LoginRequiredMixin, DeleteView):
    model = Transacao
    template_name = 'core/transacao_confirm_delete.html'
    success_url = reverse_lazy('core:transacao_list')

    def get_queryset(self):
        return Transacao.objects.filter(usuario=self.request.user)


# --- Categoria ---

class CategoriaListView(LoginRequiredMixin, ListView):
    model = Categoria
    template_name = 'core/categoria_list.html'
    context_object_name = 'categorias'

    def get_queryset(self):
        return Categoria.objects.filter(usuario=self.request.user).order_by('nome')

class CategoriaCreateView(LoginRequiredMixin, CreateView):
    model = Categoria
    form_class = CategoriaForm
    template_name = 'core/categoria_form.html'
    success_url = reverse_lazy('core:categoria_list')

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        return super().form_valid(form)

class CategoriaUpdateView(LoginRequiredMixin, UpdateView):
    model = Categoria
    form_class = CategoriaForm
    template_name = 'core/categoria_form.html'
    success_url = reverse_lazy('core:categoria_list')

    def get_queryset(self):
        return Categoria.objects.filter(usuario=self.request.user)

class CategoriaDeleteView(LoginRequiredMixin, DeleteView):
    model = Categoria
    template_name = 'core/categoria_confirm_delete.html'
    success_url = reverse_lazy('core:categoria_list')

    def get_queryset(self):
        return Categoria.objects.filter(usuario=self.request.user)


# --- Conta Bancária ---

class ContaBancariaListView(LoginRequiredMixin, ListView):
    model = ContaBancaria
    template_name = 'core/conta_list.html'
    context_object_name = 'contas'

    def get_queryset(self):
        return ContaBancaria.objects.filter(usuario=self.request.user).order_by('nome')

class ContaBancariaCreateView(LoginRequiredMixin, CreateView):
    model = ContaBancaria
    form_class = ContaBancariaForm
    template_name = 'core/conta_form.html'
    success_url = reverse_lazy('core:conta_list')

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        return super().form_valid(form)

class ContaBancariaUpdateView(LoginRequiredMixin, UpdateView):
    model = ContaBancaria
    form_class = ContaBancariaForm
    template_name = 'core/conta_form.html'
    success_url = reverse_lazy('core:conta_list')

    def get_queryset(self):
        return ContaBancaria.objects.filter(usuario=self.request.user)

class ContaBancariaDeleteView(LoginRequiredMixin, DeleteView):
    model = ContaBancaria
    template_name = 'core/conta_confirm_delete.html'
    success_url = reverse_lazy('core:conta_list')

    def get_queryset(self):
        return ContaBancaria.objects.filter(usuario=self.request.user)


# --- Orçamento ---

class OrcamentoListView(LoginRequiredMixin, ListView):
    model = Orcamento
    template_name = 'core/orcamento_list.html'
    context_object_name = 'orcamentos'

    def get_queryset(self):
        return Orcamento.objects.filter(usuario=self.request.user).order_by('-ano', '-mes')

class OrcamentoCreateView(LoginRequiredMixin, CreateView):
    model = Orcamento
    form_class = OrcamentoForm
    template_name = 'core/orcamento_form.html'
    success_url = reverse_lazy('core:orcamento_list')

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['categoria'].queryset = Categoria.objects.filter(usuario=self.request.user)
        return form

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        return super().form_valid(form)

class OrcamentoUpdateView(LoginRequiredMixin, UpdateView):
    model = Orcamento
    form_class = OrcamentoForm
    template_name = 'core/orcamento_form.html'
    success_url = reverse_lazy('core:orcamento_list')

    def get_queryset(self):
        return Orcamento.objects.filter(usuario=self.request.user)

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['categoria'].queryset = Categoria.objects.filter(usuario=self.request.user)
        return form

class OrcamentoDeleteView(LoginRequiredMixin, DeleteView):
    model = Orcamento
    template_name = 'core/orcamento_confirm_delete.html'
    success_url = reverse_lazy('core:orcamento_list')

    def get_queryset(self):
        return Orcamento.objects.filter(usuario=self.request.user)