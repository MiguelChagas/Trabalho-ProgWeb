from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.db.models import Sum
from .models import Transacao, ContaBancaria
from .forms import TransacaoForm

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

class TransacaoDeleteView(LoginRequiredMixin, DeleteView):
    model = Transacao
    template_name = 'core/transacao_confirm_delete.html'
    success_url = reverse_lazy('core:transacao_list')

    def get_queryset(self):
        return Transacao.objects.filter(usuario=self.request.user)