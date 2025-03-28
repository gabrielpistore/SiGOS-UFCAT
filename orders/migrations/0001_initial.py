# Generated by Django 5.1.2 on 2025-02-14 12:58

import django.core.validators
import django.db.models.deletion
import simple_history.models
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, unique=True, verbose_name='Nome')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Categoria',
                'verbose_name_plural': 'Categorias',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='Nome')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Departamento',
                'verbose_name_plural': 'Departamentos',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Nome')),
                ('email', models.EmailField(max_length=254)),
                ('mobile_phone', models.CharField(max_length=20, verbose_name='Celular')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Funcionário',
                'verbose_name_plural': 'Funcionários',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='HistoricalWorkOrder',
            fields=[
                ('id', models.BigIntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
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
                ('created_at', models.DateTimeField(blank=True, editable=False)),
                ('updated_at', models.DateTimeField(blank=True, editable=False)),
                ('image', models.TextField(blank=True, max_length=100, null=True, validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])], verbose_name='Imagem')),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField(db_index=True)),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('category', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='orders.category', verbose_name='Categoria')),
                ('dept_name', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='orders.department', verbose_name='Departamento')),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('responsible_employee', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='orders.employee', verbose_name='Funcionário Responsável')),
            ],
            options={
                'verbose_name': 'historical Ordem de Serviço',
                'verbose_name_plural': 'historical Ordens de Serviço',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': ('history_date', 'history_id'),
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
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
                ('image', models.ImageField(blank=True, null=True, upload_to='ordens/%Y/%m/%d/', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])], verbose_name='Imagem')),
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
            name='WorkOrderProgress',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('progress_date', models.DateTimeField(auto_now_add=True)),
                ('progress_description', models.TextField(verbose_name='Descrição do Progresso')),
                ('work_order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='orders.workorder', verbose_name='Ordem de Serviço')),
            ],
            options={
                'verbose_name': 'Progresso da Ordem de Serviço',
                'verbose_name_plural': 'Progressos das Ordens de Serviço',
                'ordering': ['-progress_date'],
            },
        ),
    ]
