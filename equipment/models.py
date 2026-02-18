from django.db import models
from django.core.validators import MinLengthValidator, RegexValidator


class Manufacturer(models.Model):
    name = models.CharField(
        max_length=100,
        unique=True,
        help_text="Manufacturer name"
    )
    country = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text="Country of origin"
    )
    website = models.URLField(
        blank=True,
        null=True,
        help_text="Manufacturer website"
    )
    contact_info = models.TextField(
        blank=True,
        null=True,
        help_text="Contact information"
    )

    class Meta:
        verbose_name = "Manufacturer"
        verbose_name_plural = "Manufacturers"
        ordering = ['name']

    def __str__(self):
        return self.name


class EquipmentCategory(models.Model):
    name = models.CharField(
        max_length=100,
        unique=True,
        help_text="Тип оборудване (pH метър, спектрофотометър, везна и т.н.)"
    )
    description = models.TextField(
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = "Equipment Category"
        verbose_name_plural = "Equipment Categories"
        ordering = ['name']

    def __str__(self):
        return self.name


class Equipment(models.Model):
    STATUS_CHOICES = [
        ('operational', 'Operational'),
        ('maintenance', 'Under Maintenance'),
        ('calibration', 'Calibration Required'),
        ('out_of_service', 'Out of Service'),
    ]

    asset_number = models.CharField(
        max_length=50,
        unique=True,
        validators=[
            MinLengthValidator(3),
            RegexValidator(
                regex=r'^[A-Z0-9-]+$',
                message='ASSET номерът трябва да съдържа само главни букви, цифри и тире'
            )
        ],
        help_text="Уникален ASSET номер на оборудването"
    )
    name = models.CharField(
        max_length=200,
        help_text="Име на оборудването"
    )
    category = models.ForeignKey(
        EquipmentCategory,
        on_delete=models.PROTECT,
        related_name='equipment'
    )
    manufacturer = models.ForeignKey(
        Manufacturer,
        on_delete=models.PROTECT,
        related_name='equipment',
        help_text="Equipment manufacturer"
    )
    model = models.CharField(
        max_length=100
    )
    serial_number = models.CharField(
        max_length=100,
        unique=True
    )
    location = models.CharField(
        max_length=200,
        help_text="Laboratory location"
    )
    required_maintenance_types = models.ManyToManyField(
        'maintenance.MaintenanceType',
        blank=True,
        related_name='applicable_equipment',
        help_text="Types of maintenance required for this equipment (Calibration, OQ/PV, Technical Service)"
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='operational',
        help_text="Current equipment status (auto-calculated based on maintenance/inspection dates)"
    )
    purchase_date = models.DateField(
        null=True,
        blank=True
    )
    notes = models.TextField(
        blank=True,
        null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Equipment"
        verbose_name_plural = "Equipment"
        ordering = ['asset_number']

    def __str__(self):
        return f"{self.asset_number} - {self.name}"

    def get_calculated_status(self):
        """
        Automatically calculate equipment status based on:
        - Overdue maintenance records (calibration, validation)
        - Overdue inspections
        """
        from datetime import date
        today = date.today()

        # Check for overdue maintenance
        latest_maintenance = self.maintenance_records.order_by('-next_due_date').first()
        if latest_maintenance and latest_maintenance.next_due_date < today:
            return 'calibration'

        # Check for overdue inspections
        latest_inspection = self.inspections.order_by('-next_inspection_date').first()
        if latest_inspection and latest_inspection.next_inspection_date < today:
            return 'maintenance'

        # Check if failed last inspection
        if latest_inspection and latest_inspection.status == 'failed':
            return 'out_of_service'

        return 'operational'

    def update_status(self):
        """Update the status field with calculated status"""
        self.status = self.get_calculated_status()
        self.save(update_fields=['status'])

