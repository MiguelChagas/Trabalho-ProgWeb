from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    # Transações
    path('transacoes/', views.TransacaoListView.as_view(), name='transacao_list'),
    path('transacoes/nova/', views.TransacaoCreateView.as_view(), name='transacao_create'),
    path('transacoes/<int:pk>/editar/', views.TransacaoUpdateView.as_view(), name='transacao_update'),
    path('transacoes/<int:pk>/excluir/', views.TransacaoDeleteView.as_view(), name='transacao_delete'),
    # Categorias
    path('categorias/', views.CategoriaListView.as_view(), name='categoria_list'),
    path('categorias/nova/', views.CategoriaCreateView.as_view(), name='categoria_create'),
    path('categorias/<int:pk>/editar/', views.CategoriaUpdateView.as_view(), name='categoria_update'),
    path('categorias/<int:pk>/excluir/', views.CategoriaDeleteView.as_view(), name='categoria_delete'),
    # Contas Bancárias
    path('contas/', views.ContaBancariaListView.as_view(), name='conta_list'),
    path('contas/nova/', views.ContaBancariaCreateView.as_view(), name='conta_create'),
    path('contas/<int:pk>/editar/', views.ContaBancariaUpdateView.as_view(), name='conta_update'),
    path('contas/<int:pk>/excluir/', views.ContaBancariaDeleteView.as_view(), name='conta_delete'),
    # Orçamentos
    path('orcamentos/', views.OrcamentoListView.as_view(), name='orcamento_list'),
    path('orcamentos/novo/', views.OrcamentoCreateView.as_view(), name='orcamento_create'),
    path('orcamentos/<int:pk>/editar/', views.OrcamentoUpdateView.as_view(), name='orcamento_update'),
    path('orcamentos/<int:pk>/excluir/', views.OrcamentoDeleteView.as_view(), name='orcamento_delete'),
]