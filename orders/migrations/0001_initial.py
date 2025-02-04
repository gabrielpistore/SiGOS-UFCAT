# Generated by Django 5.1.2 on 2025-01-27 23:45

import django.core.validators
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
                ('name', models.CharField(max_length=150, verbose_name='Nome')),
            ],
            options={
                'verbose_name': 'Categoria',
                'verbose_name_plural': 'Categorias',
            },
        ),
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Nome')),
            ],
            options={
                'verbose_name': 'Departamento',
                'verbose_name_plural': 'Departamentos',
            },
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Nome')),
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
                ('requested_by', models.CharField(max_length=100, verbose_name='Solicitante')),
                ('email', models.EmailField(max_length=254)),
                ('phone', models.CharField(max_length=20, verbose_name='Celular')),
                ('impact', models.CharField(blank=True, choices=[('Baixo', 'Baixo'), ('Médio', 'Médio'), ('Alto', 'Alto'), ('Crítico', 'Crítico')], max_length=25, null=True, verbose_name='Impacto')),
                ('urgency', models.CharField(blank=True, choices=[('Baixo', 'Baixo'), ('Médio', 'Médio'), ('Alto', 'Alto'), ('Crítico', 'Crítico')], max_length=25, null=True, verbose_name='Urgência')),
                ('priority', models.CharField(blank=True, choices=[('Baixo', 'Baixo'), ('Médio', 'Médio'), ('Alto', 'Alto'), ('Crítico', 'Crítico')], max_length=25, null=True, verbose_name='Prioridade')),
                ('location', models.CharField(max_length=100, verbose_name='Local do Serviço')),
                ('opening_date', models.DateTimeField(verbose_name='Data de Abertura')),
                ('closing_date', models.DateTimeField(blank=True, null=True, verbose_name='Data de Fechamento')),
                ('service_start_date', models.DateTimeField(blank=True, null=True, verbose_name='Data de Início do Serviço')),
                ('service_end_date', models.DateTimeField(blank=True, null=True, verbose_name='Data de Término do Serviço')),
                ('status', models.CharField(choices=[('Aberto', 'Aberto'), ('Em Andamento', 'Em Andamento'), ('Fechado', 'Fechado')], max_length=25, verbose_name='Status')),
                ('title', models.CharField(max_length=50, verbose_name='Título do Relato')),
                ('report_description', models.TextField(verbose_name='Detalhamento do Relato')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='orders.category', verbose_name='Categoria')),
                ('dept_name', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='orders.department', verbose_name='Departamento')),
                ('responsible_employee', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='orders.employee', verbose_name='Funcionário Responsável')),
            ],
            options={
                'verbose_name': 'Ordem de Serviço',
                'verbose_name_plural': 'Ordens de Serviço',
                'ordering': ['-opening_date'],
            },
        ),
        migrations.CreateModel(
            name='WorkOrderImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='work_orders/%Y/%m/%d/', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])], verbose_name='Imagem')),
                ('uploaded_at', models.DateTimeField(auto_now_add=True, verbose_name='Data de Upload')),
                ('work_order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='orders.workorder', verbose_name='Ordem de Serviço')),
            ],
            options={
                'verbose_name': 'Imagem da Ordem de Serviço',
                'verbose_name_plural': 'Imagens da Ordem de Serviço',
            },
        ),
    ]
