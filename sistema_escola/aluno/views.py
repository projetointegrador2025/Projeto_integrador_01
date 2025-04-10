from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.core.paginator import Paginator
from .models import Aluno, Responsavel
from .forms import AlunoForm, ResponsavelForm, EnderecoForm

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('lista_alunos')
        else:
            messages.error(request, 'Usuário ou senha inválidos.')
    
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('lista_alunos')

def lista_alunos(request):
    busca = request.GET.get('busca', '')
    serie = request.GET.get('serie', '')
    page_number = request.GET.get('page')

    alunos = Aluno.objects.all()

    if busca:
        alunos = alunos.filter(nome__icontains=busca)
    if serie:
        alunos = alunos.filter(serie=serie)

    paginator = Paginator(alunos, 10)  # 10 alunos por página
    page_obj = paginator.get_page(page_number)

    total_alunos = alunos.count()
    total_responsaveis = Responsavel.objects.count()
    alunos_recentes = Aluno.objects.order_by('-id')[:5]
    series = Aluno.objects.values_list('serie', flat=True).distinct().order_by('serie')

    return render(request, 'aluno/lista_alunos.html', {
        'page_obj': page_obj,
        'total_alunos': total_alunos,
        'total_responsaveis': total_responsaveis,
        'alunos_recentes': alunos_recentes,
        'usuario': request.user,
        'busca': busca,
        'serie': serie,
        'series': series,
    })

@login_required
def cadastrar_aluno(request):
    if request.method == 'POST':
        aluno_form = AlunoForm(request.POST, prefix='aluno')
        endereco_form = EnderecoForm(request.POST)
        responsavel_form = ResponsavelForm(request.POST, prefix='responsavel')

        if aluno_form.is_valid() and endereco_form.is_valid() and responsavel_form.is_valid():
            endereco = endereco_form.save()
            aluno = aluno_form.save(commit=False)
            aluno.endereco = endereco
            aluno.save()

            responsavel = responsavel_form.save(commit=False)
            responsavel.aluno = aluno
            responsavel.save()

            return redirect('lista_alunos')
    else:
        aluno_form = AlunoForm(prefix='aluno')
        endereco_form = EnderecoForm()
        responsavel_form = ResponsavelForm(prefix='responsavel')

    context = {
        'aluno_form': aluno_form,
        'endereco_form': endereco_form,
        'responsavel_form': responsavel_form,
    }
    return render(request, 'aluno/form_aluno.html', context)

@login_required
def editar_aluno(request, aluno_id):
    aluno = get_object_or_404(Aluno, id=aluno_id)
    endereco = aluno.endereco

    if request.method == 'POST':
        aluno_form = AlunoForm(request.POST, instance=aluno, prefix='aluno')
        endereco_form = EnderecoForm(request.POST, instance=endereco)

        if aluno_form.is_valid() and endereco_form.is_valid():
            endereco_form.save()
            aluno_form.save()
            return redirect('lista_alunos')
    else:
        aluno_form = AlunoForm(instance=aluno, prefix='aluno')
        endereco_form = EnderecoForm(instance=endereco)

    return render(request, 'aluno/form_editar_aluno.html', {
        'aluno_form': aluno_form,
        'endereco_form': endereco_form,
        'titulo': 'Editar Aluno',
    })


@login_required
def excluir_aluno(request, aluno_id):
    aluno = get_object_or_404(Aluno, id=aluno_id)
    if request.method == 'POST':
        aluno.delete()
        return redirect('lista_alunos')
    return render(request, 'aluno/confirmar_exclusao.html', {'aluno': aluno})

@login_required
def lista_responsaveis(request):
    responsaveis = Responsavel.objects.all()
    return render(request, 'aluno/lista_responsaveis.html', {'responsaveis': responsaveis})

@login_required
def adicionar_responsavel(request, aluno_id):
    aluno = get_object_or_404(Aluno, id=aluno_id)
    if request.method == 'POST':
        form = ResponsavelForm(request.POST)
        if form.is_valid():
            responsavel = form.save(commit=False)
            responsavel.aluno = aluno
            responsavel.save()
            return redirect('detalhes_aluno', aluno_id=aluno.id)
    else:
        form = ResponsavelForm()
    return render(request, 'aluno/form_responsavel.html', {
        'form': form,
        'titulo': 'Adicionar Responsável',
        'aluno': aluno
    })

@login_required
def editar_responsavel(request, aluno_id, responsavel_cpf):
    aluno = get_object_or_404(Aluno, id=aluno_id)
    responsavel = get_object_or_404(Responsavel, cpf=responsavel_cpf, aluno=aluno)

    if request.method == 'POST':
        form = ResponsavelForm(request.POST, instance=responsavel)
        if form.is_valid():
            form.save()
            return redirect('detalhes_aluno', aluno_id=aluno.id)
    else:
        form = ResponsavelForm(instance=responsavel)

    return render(request, 'aluno/form_responsavel.html', {
        'form': form,
        'titulo': 'Editar Responsável',
        'aluno': aluno
    })


@login_required
def excluir_responsavel(request, aluno_id, responsavel_cpf):
    aluno = get_object_or_404(Aluno, id=aluno_id)
    responsavel = get_object_or_404(Responsavel, cpf=responsavel_cpf, aluno=aluno)

    if aluno.responsaveis.count() <= 1:
        return render(request, 'aluno/erro_exclusao.html', {
            'mensagem': 'Não é possível excluir o único responsável do aluno.',
            'aluno': aluno
        })

    if request.method == 'POST':
        responsavel.delete()
        return redirect('detalhes_aluno', aluno_id=aluno.id)

    return render(request, 'aluno/confirmar_exclusao_responsavel.html', {
        'responsavel': responsavel,
        'aluno': aluno
    })

@login_required
def detalhes_aluno(request, aluno_id):
    aluno = get_object_or_404(Aluno, id=aluno_id)
    return render(request, 'aluno/detalhes_aluno.html', {'aluno': aluno})