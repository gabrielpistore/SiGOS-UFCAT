from django.core.management.base import BaseCommand

from orders.models import Category


class Command(BaseCommand):
    help = "Populate categories"

    def handle(self, *args, **kwargs):
        categories = [
            "Instalações Hidrossanitárias",
            "Instalações elétricas",
            "Instalações e/ou Manutenção em Cabeamento de Rede",
            "Câmeras de Segurança",
            "Pequenos serviços de reparos em Marcenaria",
            "Serralheria",
            "Reparos (alvenaria, piso, forro e telhado)",
            "Jardinagem",
            "Vidraçaria",
            "Pintura",
        ]

        for category in categories:
            _, created = Category.objects.get_or_create(name=category)
            if not created:
                self.stdout.write(
                    self.style.WARNING(f"Category already exists: {category}")
                )
        self.stdout.write(self.style.SUCCESS(f"Created {len(categories)} categories."))
