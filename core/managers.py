from django.db import models


class WorkOrderQuerySet(models.QuerySet):
    def get_opened_work_orders(self):
        return self.filter(status="Aberto")

    def get_ongoing_work_orders(self):
        return self.filter(status="Em Andamento")

    def get_closed_work_orders(self):
        return self.filter(status="Fechado")
