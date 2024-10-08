# Generated by Django 5.1 on 2024-09-07 19:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='workorder',
            name='dept_name',
            field=models.CharField(choices=[('', 'Selecione'), ('REITORIA', 'REITORIA'), ('COAD-GR', 'COAD-GR'), ('CCS', 'CCS'), ('NAI', 'NAI'), ('CIDARQ', 'CIDARQ'), ('BIBLIOTECA', 'BIBLIOTECA'), ('CDPEC', 'CDPEC'), ('EDITORA', 'EDITORA'), ('SETI', 'SETI'), ('SEAF', 'SEAF'), ('PREF', 'PREF'), ('CENTRAL DE OPERAÇÕES VIGILÂNCIA', 'CENTRAL DE OPERAÇÕES VIGILÂNCIA'), ('SERVIÇO DE LIMPEZA', 'SERVIÇO DE LIMPEZA'), ('DAA', 'DAA'), ('PROAF', 'PROAF'), ('DCMP', 'DCMP'), ('CPATRI', 'CPATRI'), ('DCF', 'DCF'), ('DLT', 'DLT'), ('PROEC', 'PROEC'), ('PROPESQ', 'PROPESQ'), ('CEP', 'CEP'), ('PROGEP', 'PROGEP'), ('SIASS', 'SIASS'), ('PRPE', 'PRPE'), ('PROGRAD', 'PROGRAD'), ('CGEN', 'CGEN'), ('FAE', 'FAE'), ('FENG - Engenharia de Minas', 'FENG - Engenharia de Minas'), ('FENG - Engenharia de Produção', 'FENG - Engenharia de Produção'), ('FENG - Secretaria Administrativa', 'FENG - Secretaria Administrativa'), ('FENG - Engenharia Civil', 'FENG - Engenharia Civil'), ('IBIOTEC - Ciências Biológicas', 'IBIOTEC - Ciências Biológicas'), ('IBIOTEC - Ciências da Computação', 'IBIOTEC - Ciências da Computação'), ('IBIOTEC - Educação Física', 'IBIOTEC - Educação Física'), ('IBIOTEC - Enfermagem', 'IBIOTEC - Enfermagem'), ('IBIOTEC - LABIM', 'IBIOTEC - LABIM'), ('IBIOTEC - Psicologia', 'IBIOTEC - Psicologia'), ('IBIOTEC - Medicina', 'IBIOTEC - Medicina'), ('IF', 'IF'), ('IGEO', 'IGEO'), ('INHCS', 'INHCS'), ('IMTec', 'IMTec'), ('IEL', 'IEL'), ('IQ', 'IQ')], max_length=32, verbose_name='Departamento'),
        ),
    ]
