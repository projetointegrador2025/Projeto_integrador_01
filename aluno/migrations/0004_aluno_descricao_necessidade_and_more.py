# Generated by Django 5.2 on 2025-05-23 05:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("aluno", "0003_alter_aluno_saida_sem_acompanhante_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="aluno",
            name="descricao_necessidade",
            field=models.TextField(
                blank=True, verbose_name="Descrição da Necessidade e CID"
            ),
        ),
        migrations.AddField(
            model_name="aluno",
            name="necessidades_especiais",
            field=models.BooleanField(
                choices=[(True, "SIM"), (False, "NÃO")],
                default=False,
                verbose_name="Necessidades Especiais",
            ),
        ),
        migrations.AddField(
            model_name="aluno",
            name="rm",
            field=models.CharField(
                default="00000",
                max_length=20,
                unique=True,
                verbose_name="RM (Registro de Matrícula)",
            ),
        ),
    ]
