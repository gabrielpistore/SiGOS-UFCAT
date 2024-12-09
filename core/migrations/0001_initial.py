# Generated by Django 5.1.2 on 2024-12-08 22:08

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Nome')),
            ],
            options={
                'verbose_name': 'Categoria',
                'verbose_name_plural': 'Categorias',
            },
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Nome')),
                ('email', models.EmailField(max_length=254)),
                ('mobile_phone', models.CharField(max_length=20, verbose_name='Celular')),
            ],
            options={
                'verbose_name': 'Funcionário',
                'verbose_name_plural': 'Funcionários',
            },
        ),
        migrations.CreateModel(
            name='WorkOrder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('requested_by', models.CharField(max_length=255, verbose_name='Solicitante')),
                ('dept_name', models.CharField(choices=[('REITORIA', 'REITORIA'), ('COAD-GR', 'COAD-GR'), ('CCS', 'CCS'), ('NAI', 'NAI'), ('CIDARQ', 'CIDARQ'), ('BIBLIOTECA', 'BIBLIOTECA'), ('CDPEC', 'CDPEC'), ('EDITORA', 'EDITORA'), ('SETI', 'SETI'), ('SEAF', 'SEAF'), ('PREF', 'PREF'), ('CENTRAL DE OPERAÇÕES VIGILÂNCIA', 'CENTRAL DE OPERAÇÕES VIGILÂNCIA'), ('SERVIÇO DE LIMPEZA', 'SERVIÇO DE LIMPEZA'), ('DAA', 'DAA'), ('PROAF', 'PROAF'), ('DCMP', 'DCMP'), ('CPATRI', 'CPATRI'), ('DCF', 'DCF'), ('DLT', 'DLT'), ('PROEC', 'PROEC'), ('PROPESQ', 'PROPESQ'), ('CEP', 'CEP'), ('PROGEP', 'PROGEP'), ('SIASS', 'SIASS'), ('PRPE', 'PRPE'), ('PROGRAD', 'PROGRAD'), ('CGEN', 'CGEN'), ('FAE', 'FAE'), ('FENG - Engenharia de Minas', 'FENG - Engenharia de Minas'), ('FENG - Engenharia de Produção', 'FENG - Engenharia de Produção'), ('FENG - Secretaria Administrativa', 'FENG - Secretaria Administrativa'), ('FENG - Engenharia Civil', 'FENG - Engenharia Civil'), ('IBIOTEC - Ciências Biológicas', 'IBIOTEC - Ciências Biológicas'), ('IBIOTEC - Ciências da Computação', 'IBIOTEC - Ciências da Computação'), ('IBIOTEC - Educação Física', 'IBIOTEC - Educação Física'), ('IBIOTEC - Enfermagem', 'IBIOTEC - Enfermagem'), ('IBIOTEC - LABIM', 'IBIOTEC - LABIM'), ('IBIOTEC - Psicologia', 'IBIOTEC - Psicologia'), ('IBIOTEC - Medicina', 'IBIOTEC - Medicina'), ('IF', 'IF'), ('IGEO', 'IGEO'), ('INHCS', 'INHCS'), ('IMTec', 'IMTec'), ('IEL', 'IEL'), ('IQ', 'IQ')], max_length=32, verbose_name='Departamento')),
                ('email', models.EmailField(max_length=254)),
                ('phone', models.CharField(max_length=20, verbose_name='Celular')),
                ('impact', models.CharField(choices=[('Baixo', 'Baixo'), ('Médio', 'Médio'), ('Alto', 'Alto'), ('Crítico', 'Crítico')], max_length=7, verbose_name='Impacto')),
                ('urgency', models.CharField(choices=[('Baixo', 'Baixo'), ('Médio', 'Médio'), ('Alto', 'Alto'), ('Crítico', 'Crítico')], max_length=7, verbose_name='Urgência')),
                ('priority', models.CharField(choices=[('Baixo', 'Baixo'), ('Médio', 'Médio'), ('Alto', 'Alto'), ('Crítico', 'Crítico')], max_length=7, verbose_name='Prioridade')),
                ('location', models.CharField(max_length=255, verbose_name='Local do Serviço')),
                ('opening_date', models.DateTimeField(verbose_name='Data de Abertura')),
                ('closing_date', models.DateTimeField(verbose_name='Data de Fechamento')),
                ('service_start_date', models.DateTimeField(blank=True, null=True, verbose_name='Data de Início do Serviço')),
                ('service_end_date', models.DateTimeField(blank=True, null=True, verbose_name='Data de Término do Serviço')),
                ('status', models.CharField(choices=[('Aberto', 'Aberto'), ('Em Andamento', 'Em Andamento'), ('Fechado', 'Fechado')], max_length=12, verbose_name='Status')),
                ('title', models.CharField(max_length=100, verbose_name='Título do Relato')),
                ('report_description', models.TextField(verbose_name='Detalhamento do Relato')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.category', verbose_name='Categoria')),
                ('responsible_employee', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='core.employee', verbose_name='Funcionário Responsável')),
            ],
            options={
                'verbose_name': 'Ordem de Serviço',
                'verbose_name_plural': 'Ordens de Serviço',
            },
        ),
    ]
