from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('transacoes/', views.TransacaoListView.as_view(), name='transacao_list'),
    path('transacoes/nova/', views.TransacaoCreateView.as_view(), name='transacao_create'),
    path('transacoes/<int:pk>/editar/', views.TransacaoUpdateView.as_view(), name='transacao_update'),
    path('transacoes/<int:pk>/excluir/', views.TransacaoDeleteView.as_view(), name='transacao_delete'),
]