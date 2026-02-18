from django.db import models
from equipment.models import Equipment


class InspectionType(models.Model):
    FREQUENCY_CHOICES = [
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
        ('quarterly', '3 Months'),
        ('biannual', '6 Months'),
        ('annual', 'Annual'),
    ]

    FREQUENCY_DAYS = {
        'daily': 1,
        'weekly': 7,
        'monthly': 30,
        'quarterly': 90,
        'biannual': 180,
        'annual': 365,
    }

    name = models.CharField(
        max_length=100,
        help_text="Inspection type name (daily, monthly, etc.)"
    )
    frequency = models.CharField(
        max_length=20,
        choices=FREQUENCY_CHOICES
    )
    description = models.TextField(
        help_text="Description of the inspection"
    )
    checklist = models.TextField(
        help_text="List of checks to be performed"
    )

    class Meta:
        verbose_name = "Inspection Type"
        verbose_name_plural = "Inspection Types"
        ordering = ['frequency', 'name']

    def __str__(self):
        return f"{self.name} ({self.get_frequency_display()})"

    def get_frequency_days(self):
        """Return number of days for this frequency"""
        return self.FREQUENCY_DAYS.get(self.frequency, 30)


class Inspection(models.Model):
    STATUS_CHOICES = [
        ('passed', 'Passed'),
        ('failed', 'Failed'),
        ('needs_attention', 'Needs Attention'),
    ]

    equipment = models.ForeignKey(
        Equipment,
        on_delete=models.CASCADE,
        related_name='inspections'
    )
    inspection_type = models.ForeignKey(
        InspectionType,
        on_delete=models.PROTECT,
        related_name='inspections'
    )
    inspection_date = models.DateField(
        help_text="Date when inspection was performed"
    )
    next_inspection_date = models.DateField(
        blank=True,
        null=True,
        help_text="Next inspection date (auto-calculated from inspection_date + frequency)"
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES
    )
    inspector_name = models.CharField(
        max_length=100,
        help_text="Name of the inspector"
    )
    findings = models.TextField(
        help_text="Inspection results and remarks"
    )
    corrective_actions = models.TextField(
        blank=True,
        null=True,
        help_text="Corrective actions (if any)"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Inspection"
        verbose_name_plural = "Inspections"
        ordering = ['-inspection_date']

    def __str__(self):
        return f"{self.equipment.asset_number} - {self.inspection_type.name} ({self.inspection_date})"

    def save(self, *args, **kwargs):
        """Auto-calculate next_inspection_date based on inspection_type frequency"""
        from datetime import timedelta
        if not self.next_inspection_date and self.inspection_date and self.inspection_type:
            days = self.inspection_type.get_frequency_days()
            self.next_inspection_date = self.inspection_date + timedelta(days=days)
        super().save(*args, **kwargs)
        # Update equipment status after saving inspection
        self.equipment.update_status()
