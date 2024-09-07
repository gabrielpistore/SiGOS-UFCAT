from django.db import models


class Category(models.Model):
    class Meta:
        verbose_name = "Categoria"
        verbose_name_plural = "Categorias"

    name = models.CharField(max_length=255, verbose_name="Nome")

    def __str__(self):
        return self.name


class Employee(models.Model):
    class Meta:
        verbose_name = "Funcionário"
        verbose_name_plural = "Funcionários"

    name = models.CharField(max_length=255, verbose_name="Nome")
    email = models.EmailField()
    mobile_phone = models.CharField(max_length=20, verbose_name="Celular")

    def __str__(self):
        return self.name


class WorkOrder(models.Model):
    class Meta:
        verbose_name = "Ordem de Serviço"
        verbose_name_plural = "Ordens de Serviço"

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
        ("", "Selecione"),
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

    requested_by = models.CharField(max_length=255, verbose_name="Solicitante")
    dept_name = models.CharField(
        max_length=32, choices=DEPT_NAMES, verbose_name="Departamento"
    )
    email = models.EmailField()
    phone = models.CharField(max_length=20, verbose_name="Celular")
    order_type = models.CharField(max_length=255, verbose_name="Tipo")
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, verbose_name="Categoria"
    )
    responsible_employee = models.ForeignKey(
        Employee, on_delete=models.DO_NOTHING, verbose_name="Funcionário Responsável"
    )
    impact = models.CharField(max_length=7, choices=LEVEL, verbose_name="Impacto")
    urgency = models.CharField(max_length=7, choices=LEVEL, verbose_name="Urgência")
    priority = models.CharField(max_length=7, choices=LEVEL, verbose_name="Prioridade")
    location = models.CharField(max_length=255, verbose_name="Local do Serviço")
    opening_date = models.DateTimeField(verbose_name="Data de Abertura")
    closing_date = models.DateTimeField(verbose_name="Data de Fechamento")
    service_start_date = models.DateTimeField(
        blank=True, null=True, verbose_name="Data de Início do Serviço"
    )
    service_end_date = models.DateTimeField(
        blank=True, null=True, verbose_name="Data de Término do Serviço"
    )
    status = models.CharField(max_length=12, choices=STATUS, verbose_name="Status")
    title = models.CharField(max_length=100, verbose_name="Título do Relato")
    report_description = models.TextField(verbose_name="Detalhamento do Relato")

    # attachments: to be added

    def __str__(self):
        return self.title
