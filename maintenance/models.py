from django.db import models
from equipment.models import Equipment
from dateutil.relativedelta import relativedelta


class MaintenanceType(models.Model):
    TYPE_CHOICES = [
        ('calibration', 'Calibration'),
        ('validation', 'OQ/PV Validation'),
        ('technical_service', 'Technical Service'),
        ('repair', 'Repair'),
    ]

    name = models.CharField(
        max_length=100,
        help_text="Maintenance type name"
    )
    type = models.CharField(
        max_length=20,
        choices=TYPE_CHOICES
    )
    period_months = models.PositiveIntegerField(
        default=12,
        help_text="Period in months (e.g., 12 for annual, 6 for semi-annual)"
    )
    description = models.TextField(
        help_text="Description of the maintenance type"
    )

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
    performed_date = models.DateField(
        help_text="Date when maintenance was performed"
    )
    next_due_date = models.DateField(
        blank=True,
        null=True,
        help_text="Next due date (auto-calculated from performed_date + period)"
    )
    performed_by = models.CharField(
        max_length=200,
        help_text="Department or person name (e.g., Metrology/QC)"
    )
    certificate_number = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text="Certificate/Protocol number"
    )
    results = models.TextField(
        help_text="Calibration/Validation results"
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

    def save(self, *args, **kwargs):
        """Auto-calculate next_due_date based on maintenance_type period"""
        if not self.next_due_date and self.performed_date and self.maintenance_type:
            self.next_due_date = self.performed_date + relativedelta(months=self.maintenance_type.period_months)
        super().save(*args, **kwargs)
        # Update equipment status after saving maintenance record
        self.equipment.update_status()

