from django.db import models
from datetime import date

SN = [(True, 'SIM'), (False, 'NÃO')]
SEXO = [('MASCULINO', 'MASCULINO'),
        ('FEMININO', 'FEMININO'),
        ('OUTRO', 'OUTRO')]
ESTADO_CIVIL = [
    ('SOLTEIRO(A)', 'SOLTEIRO(A)'),
    ('CASADO(A)', 'CASADO(A)'),
    ('DIVORCIADO(A)', 'DIVORCIADO(A)'),
    ('VIÚVO(A)', 'VIÚVO(A)') 
]

SERIES = [
    ('1°A', '1°A'), ('1°B', '1°B'), ('1°C', '1°C'), ('1°D', '1°D'),
    ('2°A', '2°A'), ('2°B', '2°B'), ('2°C', '2°C'), ('2°D', '2°D'),
    ('3°A', '3°A'), ('3°B', '3°B'), ('3°C', '3°C'), ('3°D', '3°D'),
    ('4°A', '4°A'), ('4°B', '4°B'), ('4°C', '4°C'), ('4°D', '4°D'),
    ('5°A', '5°A'), ('5°B', '5°B'), ('5°C', '5°C'), ('5°D', '5°D'),
]
NACIONALIDADE = [
    ('BRASILEIRA', 'BRASILEIRA'),
    ('ESTRANGEIRA', 'ESTRANGEIRA'),
]



class Endereco(models.Model):
    cep = models.CharField("CEP", max_length=9)
    logradouro = models.CharField("Endereço", max_length=100)
    numero = models.CharField("Número", max_length=10)
    complemento = models.CharField("Complemento", max_length=50, blank=True)
    bairro = models.CharField("Bairro", max_length=50)
    cidade = models.CharField("Cidade", max_length=50)

    def __str__(self):
        return f"{self.logradouro}, {self.numero} - {self.bairro}, {self.cidade}"


class Aluno(models.Model): 
    ra = models.CharField("RA do Aluno", max_length=20, unique=True)
    rm = models.CharField("RM (Registro de Matrícula)", max_length=20, unique=True)
    nome = models.CharField("Nome do Aluno", max_length=100)
    sexo = models.CharField("Sexo", max_length=10, choices=SEXO)
    nacionalidade = models.CharField("Nacionalidade", max_length=20, choices=NACIONALIDADE)
    data_nascimento = models.DateField(("Data de Nascimento"), default=date(2010, 1, 1))
    serie = models.CharField("Série", max_length=3, choices=SERIES)
    transferido = models.BooleanField("Transferido", choices=SN, default=False, blank=True )
    necessidades_especiais = models.BooleanField("Necessidades Especiais", choices=SN, default=False)
    descricao_necessidade = models.TextField("Descrição da Necessidade e CID", blank=True)
    restricao_alimentar = models.CharField("Restrição Alimentar", max_length=30, default="N/A")
    uso_imagem = models.BooleanField("Autorização de Uso de Imagem", choices=SN)
    saida_sem_acompanhante = models.BooleanField("Saída sem Acompanhante", choices=SN)
    endereco = models.OneToOneField(Endereco, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.nome} ({self.ra})"


class Responsavel(models.Model):
    aluno = models.ForeignKey(Aluno, related_name='responsaveis', on_delete=models.CASCADE)
    cpf = models.CharField("CPF do Responsável", max_length=14, primary_key=True)
    nome = models.CharField("Nome", max_length=100)
    rg = models.CharField("RG", max_length=20)
    sexo = models.CharField("Sexo", max_length=10, choices= SEXO)
    nacionalidade = models.CharField("Nacionalidade", max_length=20, choices=NACIONALIDADE)
    estado_civil = models.CharField("Estado Civil", max_length=20, choices=ESTADO_CIVIL)

    tipo_responsavel = models.CharField("Tipo de Responsável", max_length=50, choices=[
        ('PAI', 'PAI'),
        ('MÃE', 'MÃE'),
        ('TUTOR', 'TUTOR'),
        ('OUTRO', 'OUTRO'),
    ])
    tipo_responsavel_outro = models.CharField("Se outro, especifique", max_length=50, blank=True)

    data_nascimento = models.DateField(("Data de Nascimento"), default=date(2010, 1, 1))
    email = models.EmailField("Email", blank=True)

    telefone = models.CharField("Telefone", max_length=15)

    def __str__(self):
        tipo = self.tipo_responsavel_outro if self.tipo_responsavel == 'OUTRO' else self.tipo_responsavel
        return f"{self.nome} ({tipo})"