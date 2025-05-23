from django import forms
from django.forms import inlineformset_factory
from .models import Aluno, Responsavel, Endereco

class EnderecoForm(forms.ModelForm):
    class Meta:
        model = Endereco
        fields = ['cep', 'logradouro', 'numero', 'complemento', 'bairro', 'cidade']
        widgets = {
            'cep': forms.TextInput(attrs={'class': 'form-control'}),
            'logradouro': forms.TextInput(attrs={'class': 'form-control', 'style': 'text-transform: uppercase;'}),
            'numero': forms.TextInput(attrs={'class': 'form-control'}),
            'complemento': forms.TextInput(attrs={'class': 'form-control', 'style': 'text-transform: uppercase;'}),
            'bairro': forms.TextInput(attrs={'class': 'form-control', 'style': 'text-transform: uppercase;'}),
            'cidade': forms.TextInput(attrs={'class': 'form-control', 'style': 'text-transform: uppercase;'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        for field in ['logradouro', 'complemento', 'bairro', 'cidade']:
            valor = cleaned_data.get(field)
            if valor and isinstance(valor, str):
                cleaned_data[field] = valor.upper()
        return cleaned_data


class AlunoForm(forms.ModelForm):
    data_nascimento = forms.DateField(
        widget=forms.DateInput(
            format='%Y-%m-%d',  
            attrs={
                'type': 'date',
                'class': 'form-control'
            }
        ),
        input_formats=['%Y-%m-%d'] 
    ) 

    class Meta:
        model = Aluno
        fields = [
            'ra', 'rm', 'nome', 'sexo', 'nacionalidade', 'data_nascimento', 'serie',
            'transferido', 'necessidades_especiais', 'descricao_necessidade',
            'restricao_alimentar', 'uso_imagem', 'saida_sem_acompanhante'
        ]
        widgets = {
            'ra': forms.TextInput(attrs={'class': 'form-control', 'style': 'text-transform: uppercase;'}),
            'rm': forms.TextInput(attrs={'class': 'form-control', 'style': 'text-transform: uppercase;'}),
            'nome': forms.TextInput(attrs={'class': 'form-control', 'style': 'text-transform: uppercase;'}),
            'sexo': forms.Select(attrs={'class': 'form-select'}),
            'nacionalidade': forms.Select(attrs={'class': 'form-select'}),
            'data_nascimento': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'serie': forms.Select(attrs={'class': 'form-select'}),
            'transferido': forms.Select(attrs={'class': 'form-select'}),
            'necessidades_especiais': forms.Select(attrs={'class': 'form-select'}),
            'descricao_necessidade': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'style': 'text-transform: uppercase;'}),
            'restricao_alimentar': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'não', 'style': 'text-transform: uppercase;'}),
            'uso_imagem': forms.Select(attrs={'class': 'form-select'}),
            'saida_sem_acompanhante': forms.Select(attrs={'class': 'form-select'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        for field in ['ra', 'rm', 'nome', 'restricao_alimentar', 'descricao_necessidade']:
            valor = cleaned_data.get(field)
            if valor and isinstance(valor, str):
                cleaned_data[field] = valor.upper()
        return cleaned_data



class ResponsavelForm(forms.ModelForm):
    class Meta:
        model = Responsavel
        fields = [
            'cpf', 'nome', 'rg', 'sexo', 'nacionalidade', 'estado_civil',
            'tipo_responsavel', 'tipo_responsavel_outro', 'data_nascimento',
            'email', 'telefone'
        ]
        widgets = {
            'cpf': forms.TextInput(attrs={'class': 'form-control', 'style': 'text-transform: uppercase;'}),
            'nome': forms.TextInput(attrs={'class': 'form-control', 'style': 'text-transform: uppercase;'}),
            'rg': forms.TextInput(attrs={'class': 'form-control', 'style': 'text-transform: uppercase;'}),
            'sexo': forms.Select(attrs={'class': 'form-select'}),
            'nacionalidade': forms.Select(attrs={'class': 'form-select'}),
            'estado_civil': forms.Select(attrs={'class': 'form-select'}),
            'tipo_responsavel': forms.Select(attrs={'class': 'form-select'}),
            'tipo_responsavel_outro': forms.TextInput(attrs={'class': 'form-control', 'style': 'text-transform: uppercase;'}),
            'data_nascimento': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}, format='%Y-%m-%d'),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'style': 'text-transform: lowercase;'}),
            'telefone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '(xx) xxxxx-xxxx'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields['cpf'].disabled = True

    def clean(self):
        cleaned_data = super().clean()
        for field in ['nome', 'rg', 'tipo_responsavel_outro']:
            valor = cleaned_data.get(field)
            if valor and isinstance(valor, str):
                cleaned_data[field] = valor.upper()
        email = cleaned_data.get('email')
        if email and isinstance(email, str):
            cleaned_data['email'] = email.lower()
        return cleaned_data


ResponsavelFormSet = inlineformset_factory(
    Aluno,
    Responsavel,
    form=ResponsavelForm,
    extra=1,
    can_delete=True
)