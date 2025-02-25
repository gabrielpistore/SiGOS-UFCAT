from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from django.db import models
from django.utils import timezone
from simple_history.models import HistoricalRecords


class Category(models.Model):
    name = models.CharField(max_length=150, verbose_name="Nome", unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Categoria"
        verbose_name_plural = "Categorias"
        ordering = ["-created_at", "name"]

    def __str__(self):
        return self.name


class Employee(models.Model):
    name = models.CharField(max_length=100, verbose_name="Nome")
    email = models.EmailField()
    mobile_phone = models.CharField(max_length=20, verbose_name="Celular")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Funcionário"
        verbose_name_plural = "Funcionários"
        ordering = ["-created_at", "name"]

    def __str__(self):
        return self.name


class Department(models.Model):
    name = models.CharField(max_length=100, verbose_name="Nome", unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Departamento"
        verbose_name_plural = "Departamentos"
        ordering = ["-created_at", "name"]

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
    dept_name = models.ForeignKey(
        Department, verbose_name="Departamento", on_delete=models.PROTECT
    )
    email = models.EmailField()
    phone = models.CharField(max_length=20, verbose_name="Celular")
    category = models.ForeignKey(
        Category, on_delete=models.PROTECT, verbose_name="Categoria"
    )
    responsible_employee = models.ForeignKey(
        Employee,
        on_delete=models.PROTECT,
        verbose_name="Funcionário Responsável",
        blank=True,
        null=True,
    )
    impact = models.CharField(
        max_length=25, choices=LEVEL, blank=True, null=True, verbose_name="Impacto"
    )
    urgency = models.CharField(
        max_length=25, choices=LEVEL, blank=True, null=True, verbose_name="Urgência"
    )
    priority = models.CharField(
        max_length=25, choices=LEVEL, blank=True, null=True, verbose_name="Prioridade"
    )
    location = models.CharField(max_length=100, verbose_name="Local do Serviço")
    opening_date = models.DateTimeField(
        verbose_name="Data de Abertura", auto_now_add=True
    )
    closing_date = models.DateTimeField(
        blank=True, null=True, verbose_name="Data de Fechamento"
    )
    service_start_date = models.DateTimeField(
        blank=True, null=True, verbose_name="Data de Início do Serviço"
    )
    service_end_date = models.DateTimeField(
        blank=True, null=True, verbose_name="Data de Término do Serviço"
    )
    status = models.CharField(max_length=25, choices=STATUS, verbose_name="Status")
    title = models.CharField(max_length=50, verbose_name="Título do Relato")
    report_description = models.TextField(verbose_name="Detalhamento do Relato")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image = models.ImageField(
        upload_to="ordens/%Y/%m/%d/",
        validators=[FileExtensionValidator(allowed_extensions=["jpg", "jpeg", "png"])],
        verbose_name="Imagem",
        blank=True,
        null=True,
    )
    history = HistoricalRecords()

    def clean(self, *args, **kwargs):
        # Validate that opening_date is before closing_date
        if self.closing_date and self.opening_date > self.closing_date:
            raise ValidationError(
                {
                    "closing_date": "A data de fechamento deve ser posterior à data de abertura."
                }
            )

        # Validate that service_start_date is before service_end_date
        if self.service_start_date and self.service_end_date:
            if self.service_start_date > self.service_end_date:
                raise ValidationError(
                    {
                        "service_end_date": "A data de término do serviço deve ser posterior à data de início."
                    }
                )

        if (
            self.status == "Fechado"
            and self.service_start_date
            and not self.service_end_date
        ):
            raise ValidationError(
                {
                    "service_end_date": "Não é possível fechar uma orderm, se o serviço ainda não foi concluído."
                }
            )

        super().clean()

    def save(self, *args, **kwargs):
        # Set closing_date when status is "Fechado"
        if self.status == "Fechado":
            self.closing_date = timezone.now()

        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Ordem de Serviço"
        verbose_name_plural = "Ordens de Serviço"
        ordering = ["-opening_date"]

    def __str__(self):
        return self.title


class WorkOrderProgress(models.Model):
    work_order = models.ForeignKey(
        WorkOrder, on_delete=models.CASCADE, verbose_name="Ordem de Serviço"
    )
    progress_date = models.DateTimeField(auto_now_add=True)
    progress_description = models.TextField(verbose_name="Descrição do Progresso")

    class Meta:
        verbose_name = "Progresso da Ordem de Serviço"
        verbose_name_plural = "Progressos das Ordens de Serviço"
        ordering = ["-progress_date"]

    def __str__(self):
        return self.progress_description
