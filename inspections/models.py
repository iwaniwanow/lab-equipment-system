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

    name = models.CharField(
        max_length=100,
        help_text="Тип на проверката (дневна, месечна и т.н.)"
    )
    frequency = models.CharField(
        max_length=20,
        choices=FREQUENCY_CHOICES
    )
    description = models.TextField()
    checklist = models.TextField(
        help_text="Списък с проверки, които трябва да се направят"
    )

    class Meta:
        verbose_name = "Inspection Type"
        verbose_name_plural = "Inspection Types"
        ordering = ['frequency', 'name']

    def __str__(self):
        return f"{self.name} ({self.get_frequency_display()})"


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
    inspection_date = models.DateField()
    next_inspection_date = models.DateField(
        help_text="Дата на следващата проверка"
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES
    )
    inspector_name = models.CharField(
        max_length=100,
        help_text="Име на извършилия проверката"
    )
    findings = models.TextField(
        help_text="Резултати и забележки от проверката"
    )
    corrective_actions = models.TextField(
        blank=True,
        null=True,
        help_text="Коригиращи действия (ако има)"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Inspection"
        verbose_name_plural = "Inspections"
        ordering = ['-inspection_date']

    def __str__(self):
        return f"{self.equipment.asset_number} - {self.inspection_type.name} ({self.inspection_date})"
