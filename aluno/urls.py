from django.urls import path
from . import views
from .views import login_view, logout_view


urlpatterns = [
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),

    path('', views.lista_alunos, name='lista_alunos'),
    path('cadastrar/', views.cadastrar_aluno, name='cadastrar_aluno'),
    path('editar/<int:aluno_id>/', views.editar_aluno, name='editar_aluno'),
    path('excluir/<int:aluno_id>/', views.excluir_aluno, name='excluir_aluno'),


    path('responsaveis/', views.lista_responsaveis, name='lista_responsaveis'),
    path('aluno/<int:aluno_id>/responsavel/<str:responsavel_cpf>/editar/', views.editar_responsavel, name='editar_responsavel'),
    path('aluno/<int:aluno_id>/responsavel/<str:responsavel_cpf>/excluir/', views.excluir_responsavel, name='excluir_responsavel'),
    path('aluno/<int:aluno_id>/adicionar_responsavel/', views.adicionar_responsavel, name='adicionar_responsavel'),

    path('aluno/<int:aluno_id>/', views.detalhes_aluno, name='detalhes_aluno'),
]