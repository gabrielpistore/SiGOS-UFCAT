from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from django.db import models
from simple_history.models import HistoricalRecords


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
    dept_name = models.ForeignKey(
        Department, verbose_name="Departamento", on_delete=models.DO_NOTHING
    )
    email = models.EmailField()
    phone = models.CharField(max_length=20, verbose_name="Celular")
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, verbose_name="Categoria"
    )
    responsible_employee = models.ForeignKey(
        Employee,
        on_delete=models.DO_NOTHING,
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
    opening_date = models.DateTimeField(verbose_name="Data de Abertura")
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
    history = HistoricalRecords()

    def clean(self):
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
        super().clean()

    class Meta:
        verbose_name = "Ordem de Serviço"
        verbose_name_plural = "Ordens de Serviço"
        ordering = ["-opening_date"]

    def __str__(self):
        return self.title


class WorkOrderImage(models.Model):
    work_order = models.ForeignKey(
        WorkOrder,
        on_delete=models.CASCADE,
        related_name="images",
        verbose_name="Ordem de Serviço",
    )
    image = models.ImageField(
        upload_to="work_orders/%Y/%m/%d/",
        validators=[FileExtensionValidator(allowed_extensions=["jpg", "jpeg", "png"])],
        verbose_name="Imagem",
    )
    uploaded_at = models.DateTimeField(auto_now_add=True, verbose_name="Data de Upload")

    class Meta:
        verbose_name = "Imagem da Ordem de Serviço"
        verbose_name_plural = "Imagens da Ordem de Serviço"

    def __str__(self):
        return f"Imagem {self.id} - {self.work_order.title}"

    def clean(self):
        # Limit the number of images to 3 per WorkOrder
        if self.work_order.images.count() >= 3:
            raise ValidationError("Cada ordem de serviço pode ter no máximo 3 imagens.")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
