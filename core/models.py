from django.db import models

from .managers import WorkOrderQuerySet


class Category(models.Model):
    name = models.CharField(max_length=150, verbose_name="Nome")

    class Meta:
        verbose_name = "Categoria"
        verbose_name_plural = "Categorias"

    def __str__(self):
        return self.name


class Employee(models.Model):
    name = models.CharField(max_length=150, verbose_name="Nome")
    email = models.EmailField()
    mobile_phone = models.CharField(max_length=20, verbose_name="Celular")

    class Meta:
        verbose_name = "Funcionário"
        verbose_name_plural = "Funcionários"

    def __str__(self):
        return self.name


class Department(models.Model):
    name = models.CharField(max_length=150, verbose_name="Nome")

    class Meta:
        verbose_name = "Departamento"
        verbose_name_plural = "Departamentos"

    def __str__(self):
        return self.name


class WorkOrder(models.Model):
    LEVEL = (
        ("Baixo", "Baixo"),
        ("Médio", "Médio"),
        ("Alto", "Alto"),
        ("Crítico", "Crítico"),
    )
    STATUS = (
        ("Aberto", "Aberto"),
        ("Em Andamento", "Em Andamento"),
        ("Fechado", "Fechado"),
    )
    DEPT_NAMES = (
        ("REITORIA", "REITORIA"),
        ("COAD-GR", "COAD-GR"),
        ("CCS", "CCS"),
        ("NAI", "NAI"),
        ("CIDARQ", "CIDARQ"),
        ("BIBLIOTECA", "BIBLIOTECA"),
        ("CDPEC", "CDPEC"),
        ("EDITORA", "EDITORA"),
        ("SETI", "SETI"),
        ("SEAF", "SEAF"),
        ("PREF", "PREF"),
        ("CENTRAL DE OPERAÇÕES VIGILÂNCIA", "CENTRAL DE OPERAÇÕES VIGILÂNCIA"),
        ("SERVIÇO DE LIMPEZA", "SERVIÇO DE LIMPEZA"),
        ("DAA", "DAA"),
        ("PROAF", "PROAF"),
        ("DCMP", "DCMP"),
        ("CPATRI", "CPATRI"),
        ("DCF", "DCF"),
        ("DLT", "DLT"),
        ("PROEC", "PROEC"),
        ("PROPESQ", "PROPESQ"),
        ("CEP", "CEP"),
        ("PROGEP", "PROGEP"),
        ("SIASS", "SIASS"),
        ("PRPE", "PRPE"),
        ("PROGRAD", "PROGRAD"),
        ("CGEN", "CGEN"),
        ("FAE", "FAE"),
        ("FENG - Engenharia de Minas", "FENG - Engenharia de Minas"),
        ("FENG - Engenharia de Produção", "FENG - Engenharia de Produção"),
        ("FENG - Secretaria Administrativa", "FENG - Secretaria Administrativa"),
        ("FENG - Engenharia Civil", "FENG - Engenharia Civil"),
        ("IBIOTEC - Ciências Biológicas", "IBIOTEC - Ciências Biológicas"),
        ("IBIOTEC - Ciências da Computação", "IBIOTEC - Ciências da Computação"),
        ("IBIOTEC - Educação Física", "IBIOTEC - Educação Física"),
        ("IBIOTEC - Enfermagem", "IBIOTEC - Enfermagem"),
        ("IBIOTEC - LABIM", "IBIOTEC - LABIM"),
        ("IBIOTEC - Psicologia", "IBIOTEC - Psicologia"),
        ("IBIOTEC - Medicina", "IBIOTEC - Medicina"),
        ("IF", "IF"),
        ("IGEO", "IGEO"),
        ("INHCS", "INHCS"),
        ("IMTec", "IMTec"),
        ("IEL", "IEL"),
        ("IQ", "IQ"),
    )

    requested_by = models.CharField(max_length=150, verbose_name="Solicitante")
    dept_name = models.ForeignKey(Department, verbose_name="Departamento", on_delete=models.DO_NOTHING)
    email = models.EmailField()
    phone = models.CharField(max_length=20, verbose_name="Celular")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="Categoria")
    responsible_employee = models.ForeignKey(
        Employee, on_delete=models.DO_NOTHING, verbose_name="Funcionário Responsável"
    )
    impact = models.CharField(max_length=25, choices=LEVEL, verbose_name="Impacto")
    urgency = models.CharField(max_length=25, choices=LEVEL, verbose_name="Urgência")
    priority = models.CharField(max_length=25, choices=LEVEL, verbose_name="Prioridade")
    location = models.CharField(max_length=255, verbose_name="Local do Serviço")
    opening_date = models.DateTimeField(verbose_name="Data de Abertura")
    closing_date = models.DateTimeField(verbose_name="Data de Fechamento")
    service_start_date = models.DateTimeField(blank=True, null=True, verbose_name="Data de Início do Serviço")
    service_end_date = models.DateTimeField(blank=True, null=True, verbose_name="Data de Término do Serviço")
    status = models.CharField(max_length=25, choices=STATUS, verbose_name="Status")
    title = models.CharField(max_length=100, verbose_name="Título do Relato")
    report_description = models.TextField(verbose_name="Detalhamento do Relato")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # TODO: Add attachment field

    objects = WorkOrderQuerySet.as_manager()

    class Meta:
        verbose_name = "Ordem de Serviço"
        verbose_name_plural = "Ordens de Serviço"

    def __str__(self):
        return self.title
