from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=150, verbose_name="Nome")

    class Meta:
        verbose_name = "Categoria"
        verbose_name_plural = "Categorias"

    def __str__(self):
        return self.name


class Employee(models.Model):
    name = models.CharField(max_length=100, verbose_name="Nome")
    email = models.EmailField()
    mobile_phone = models.CharField(max_length=20, verbose_name="Celular")

    class Meta:
        verbose_name = "Funcionário"
        verbose_name_plural = "Funcionários"

    def __str__(self):
        return self.name


class Department(models.Model):
    name = models.CharField(max_length=100, verbose_name="Nome")

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

    requested_by = models.CharField(max_length=100, verbose_name="Solicitante")
    dept_name = models.ForeignKey(Department, verbose_name="Departamento", on_delete=models.DO_NOTHING)
    email = models.EmailField()
    phone = models.CharField(max_length=20, verbose_name="Celular")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="Categoria")
    responsible_employee = models.ForeignKey(
        Employee, on_delete=models.DO_NOTHING, verbose_name="Funcionário Responsável"
    )
    impact = models.CharField(max_length=25, choices=LEVEL, blank=True, null=True, verbose_name="Impacto")
    urgency = models.CharField(max_length=25, choices=LEVEL, blank=True, null=True, verbose_name="Urgência")
    priority = models.CharField(max_length=25, choices=LEVEL, blank=True, null=True, verbose_name="Prioridade")
    location = models.CharField(max_length=100, verbose_name="Local do Serviço")
    opening_date = models.DateTimeField(verbose_name="Data de Abertura")
    closing_date = models.DateTimeField(blank=True, null=True, verbose_name="Data de Fechamento")
    service_start_date = models.DateTimeField(blank=True, null=True, verbose_name="Data de Início do Serviço")
    service_end_date = models.DateTimeField(blank=True, null=True, verbose_name="Data de Término do Serviço")
    status = models.CharField(max_length=25, choices=STATUS, verbose_name="Status")
    title = models.CharField(max_length=50, verbose_name="Título do Relato")
    report_description = models.TextField(verbose_name="Detalhamento do Relato")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # TODO: Add attachment field

    class Meta:
        verbose_name = "Ordem de Serviço"
        verbose_name_plural = "Ordens de Serviço"

    def __str__(self):
        return self.title
