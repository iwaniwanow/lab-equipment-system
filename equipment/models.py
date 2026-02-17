from django.db import models
from django.core.validators import MinLengthValidator, RegexValidator


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
    manufacturer = models.CharField(
        max_length=100
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
        help_text="Локация в лабораторията"
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='operational'
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
