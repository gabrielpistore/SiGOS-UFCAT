from django.core.management.base import BaseCommand

from orders.models import Department


class Command(BaseCommand):
    help = "Populate the Department model with initial data"

    def handle(self, *args, **kwargs):
        dept_names = [
            "REITORIA",
            "COAD-GR",
            "CCS",
            "NAI",
            "CIDARQ",
            "BIBLIOTECA",
            "CDPEC",
            "EDITORA",
            "SETI",
            "SEAF",
            "PREF",
            "CENTRAL DE OPERAÇÕES VIGILÂNCIA",
            "SERVIÇO DE LIMPEZA",
            "DAA",
            "PROAF",
            "DCMP",
            "CPATRI",
            "DCF",
            "DLT",
            "PROEC",
            "PROPESQ",
            "CEP",
            "PROGEP",
            "SIASS",
            "PRPE",
            "PROGRAD",
            "CGEN",
            "FAE",
            "FENG - Engenharia de Minas",
            "FENG - Engenharia de Produção",
            "FENG - Secretaria Administrativa",
            "FENG - Engenharia Civil",
            "IBIOTEC - Ciências Biológicas",
            "IBIOTEC - Ciências da Computação",
            "IBIOTEC - Educação Física",
            "IBIOTEC - Enfermagem",
            "IBIOTEC - LABIM",
            "IBIOTEC - Psicologia",
            "IBIOTEC - Medicina",
            "IF",
            "IGEO",
            "INHCS",
            "IMTec",
            "IEL",
            "IQ",
        ]

        for dept_name in dept_names:
            _, created = Department.objects.get_or_create(name=dept_name)
            if created:
                self.stdout.write(self.style.SUCCESS(f"Added department: {dept_name}"))
            else:
                self.stdout.write(self.style.WARNING(f"Department already exists: {dept_name}"))
