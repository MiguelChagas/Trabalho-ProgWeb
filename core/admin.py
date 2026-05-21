from django.contrib import admin
from .models import Categoria, ContaBancaria, Transacao, Orcamento

class TransacaoInline(admin.TabularInline):
    model = Transacao
    extra = 1
    fields = ('descricao', 'valor', 'data', 'tipo', 'conta')
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if not request.user.is_superuser and db_field.name == "conta":
            kwargs["queryset"] = ContaBancaria.objects.filter(usuario=request.user)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'tipo', 'cor', 'icone')
    list_filter = ('tipo',)
    search_fields = ('nome',)
    exclude = ('usuario',) 
    inlines = [TransacaoInline]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(usuario=request.user)

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.usuario = request.user
        super().save_model(request, obj, form, change)
    
    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)
        for instance in instances:
            # Se for uma nova transação sendo criada pelo inline, atribui o usuário logado
            if not instance.pk:
                instance.usuario = request.user
            instance.save()
        formset.save_m2m()

@admin.register(ContaBancaria)
class ContaBancariaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'saldo_inicial')
    search_fields = ('nome',)
    exclude = ('usuario',)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(usuario=request.user)

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.usuario = request.user
        super().save_model(request, obj, form, change)

@admin.register(Transacao)
class TransacaoAdmin(admin.ModelAdmin):
    list_display = ('descricao', 'valor', 'data', 'tipo', 'categoria', 'conta')
    list_filter = ('tipo', 'data', 'categoria')
    search_fields = ('descricao',)
    exclude = ('usuario',)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(usuario=request.user)

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.usuario = request.user
        super().save_model(request, obj, form, change)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if not request.user.is_superuser:
            if db_field.name == "categoria":
                kwargs["queryset"] = Categoria.objects.filter(usuario=request.user)
            elif db_field.name == "conta":
                kwargs["queryset"] = ContaBancaria.objects.filter(usuario=request.user)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

@admin.register(Orcamento)
class OrcamentoAdmin(admin.ModelAdmin):
    list_display = ('categoria', 'mes', 'ano', 'valor_limite')
    list_filter = ('mes', 'ano', 'categoria')
    exclude = ('usuario',)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(usuario=request.user)

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.usuario = request.user
        super().save_model(request, obj, form, change)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "categoria" and not request.user.is_superuser:
            kwargs["queryset"] = Categoria.objects.filter(usuario=request.user)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)