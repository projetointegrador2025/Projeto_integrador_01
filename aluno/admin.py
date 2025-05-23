from django.contrib import admin
from .models import Aluno, Responsavel

class ResponsavelInline(admin.TabularInline):
    model = Responsavel
    extra = 1

@admin.register(Aluno)
class AlunoAdmin(admin.ModelAdmin):
    list_display = ('ra', 'nome', 'serie', 'get_cidade', 'get_telefones')
    search_fields = ('nome', 'ra', 'endereco__cidade')
    list_filter = ('serie', 'ativo')
    inlines = [ResponsavelInline]

    def get_cidade(self, obj):
        return obj.endereco.cidade if obj.endereco else "-"
    get_cidade.short_description = 'Cidade'

    def get_telefones(self, obj):
        telefones = [r.telefone for r in obj.responsaveis.all() if r.telefone]
        return ", ".join(telefones) if telefones else "-"
    get_telefones.short_description = 'Telefone(s)'

@admin.register(Responsavel)
class ResponsavelAdmin(admin.ModelAdmin):
    list_display = ('nome', 'tipo_responsavel', 'aluno', 'telefone')
    search_fields = ('nome', 'tipo_responsavel', 'telefone')