from django.db import models
from equipment.models import Equipment
from dateutil.relativedelta import relativedelta


class MaintenanceType(models.Model):
    TYPE_CHOICES = [
        ('calibration', 'Калибровка'),
        ('validation', 'OQ/PV Валидиране'),
        ('technical_service', 'Технически преглед'),
        ('repair', 'Ремонт'),
    ]

    name = models.CharField(
        max_length=100,
        help_text="Наименование на типа поддръжка"
    )
    type = models.CharField(
        max_length=20,
        choices=TYPE_CHOICES,
        help_text="Тип на поддръжката"
    )
    period_months = models.PositiveIntegerField(
        default=12,
        help_text="Периодичност в месеци (например: 12 за годишна, 6 за шестмесечна)"
    )
    description = models.TextField(
        help_text="Описание на типа поддръжка"
    )

    class Meta:
        verbose_name = "Тип поддръжка"
        verbose_name_plural = "Типове поддръжка"
        ordering = ['type', 'name']

    def __str__(self):
        return f"{self.name} ({self.get_type_display()})"


class MaintenanceRecord(models.Model):
    RESULT_CHOICES = [
        ('passed', 'Годен'),
        ('failed', 'Негоден'),
        ('conditional', 'Условно годен'),
    ]

    CURRENCY_CHOICES = [
        ('BGN', 'BGN (Лева)'),
        ('EUR', 'EUR (Евро)'),
    ]

    equipment = models.ForeignKey(
        Equipment,
        on_delete=models.CASCADE,
        related_name='maintenance_records',
        help_text="Оборудване"
    )
    maintenance_type = models.ForeignKey(
        MaintenanceType,
        on_delete=models.PROTECT,
        related_name='records',
        help_text="Тип поддръжка"
    )
    performed_date = models.DateField(
        help_text="Дата на изпълнение"
    )
    next_due_date = models.DateField(
        blank=True,
        null=True,
        help_text="Следваща дата (автоматично изчислена от дата + период)"
    )
    technician = models.ForeignKey(
        'equipment.Technician',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='maintenance_records',
        verbose_name="Техник/Изпълнител",
        help_text="Техник извършил поддръжката"
    )
    performed_by = models.CharField(
        max_length=200,
        blank=True,
        help_text="Изпълнено от (старо поле за справка)"
    )
    certificate_number = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text="Номер на сертификат/протокол"
    )
    result = models.CharField(
        max_length=20,
        choices=RESULT_CHOICES,
        default='passed',
        help_text="Резултат от проверката"
    )
    work_performed = models.TextField(
        blank=True,
        default='',
        help_text="Извършена работа/резултати"
    )
    parts_used = models.TextField(
        blank=True,
        null=True,
        help_text="Използвани части/материали"
    )
    cost = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Цена"
    )
    currency = models.CharField(
        max_length=3,
        choices=CURRENCY_CHOICES,
        default='BGN',
        help_text="Валута"
    )
    notes = models.TextField(
        blank=True,
        null=True,
        help_text="Допълнителни бележки"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Запис за поддръжка"
        verbose_name_plural = "Записи за поддръжка"
        ordering = ['-performed_date']

    def __str__(self):
        return f"{self.equipment.asset_number} - {self.maintenance_type.name} ({self.performed_date})"

    def save(self, *args, **kwargs):
        """Автоматично изчислява next_due_date на база периода на типа поддръжка"""
        if not self.next_due_date and self.performed_date and self.maintenance_type:
            self.next_due_date = self.performed_date + relativedelta(months=self.maintenance_type.period_months)
        super().save(*args, **kwargs)
        self.equipment.update_status()

