from django.db import models
from equipment.models import Equipment


class MaintenanceType(models.Model):
    TYPE_CHOICES = [
        ('calibration', 'Calibration'),
        ('validation', 'Validation'),
        ('technical_service', 'Technical Service'),
        ('repair', 'Repair'),
    ]

    name = models.CharField(max_length=100)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    description = models.TextField()

    class Meta:
        verbose_name = "Maintenance Type"
        verbose_name_plural = "Maintenance Types"

    def __str__(self):
        return f"{self.name} ({self.get_type_display()})"


class MaintenanceRecord(models.Model):
    equipment = models.ForeignKey(
        Equipment,
        on_delete=models.CASCADE,
        related_name='maintenance_records'
    )
    maintenance_type = models.ForeignKey(
        MaintenanceType,
        on_delete=models.PROTECT,
        related_name='records'
    )
    performed_date = models.DateField()
    next_due_date = models.DateField(
        help_text="Дата на следващото калибриране/валидация"
    )
    performed_by = models.CharField(
        max_length=200,
        help_text="Отдел или име (напр. Метрологичен/КИП)"
    )
    certificate_number = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text="Номер на сертификат/протокол"
    )
    results = models.TextField(
        help_text="Резултати от калибрирането/валидацията"
    )
    cost = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True
    )
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Maintenance Record"
        verbose_name_plural = "Maintenance Records"
        ordering = ['-performed_date']

    def __str__(self):
        return f"{self.equipment.asset_number} - {self.maintenance_type.name} ({self.performed_date})"
