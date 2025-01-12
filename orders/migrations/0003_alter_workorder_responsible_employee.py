# Generated by Django 5.1.2 on 2025-01-09 14:33

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0002_alter_department_name_alter_employee_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='workorder',
            name='responsible_employee',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='orders.employee', verbose_name='Funcionário Responsável'),
        ),
    ]
