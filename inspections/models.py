from django.db import models
from equipment.models import Equipment


class InspectionType(models.Model):
    CATEGORY_CHOICES = [
        ('technical_review', 'Технически преглед'),
        ('suitability_check', 'Проверка за пригодност'),
    ]

    FREQUENCY_CHOICES = [
        ('daily', 'Дневна'),
        ('weekly', 'Седмична'),
        ('monthly', 'Месечна'),
        ('quarterly', 'Тримесечна (3 месеца)'),
        ('biannual', 'Шестмесечна (6 месеца)'),
        ('annual', 'Годишна'),
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
        help_text="Наименование на типа проверка"
    )
    category = models.CharField(
        max_length=30,
        choices=CATEGORY_CHOICES,
        default='suitability_check',
        help_text="Категория проверка"
    )
    frequency = models.CharField(
        max_length=20,
        choices=FREQUENCY_CHOICES,
        help_text="Честота на проверката"
    )
    description = models.TextField(
        help_text="Описание на проверката"
    )
    checklist = models.TextField(
        help_text="Списък с проверки, които трябва да се изпълнят"
    )

    class Meta:
        verbose_name = "Тип проверка"
        verbose_name_plural = "Типове проверки"
        ordering = ['category', 'frequency', 'name']

    def __str__(self):
        return f"{self.name} ({self.get_frequency_display()})"

    def get_frequency_days(self):
        """Връща брой дни за тази честота"""
        return self.FREQUENCY_DAYS.get(self.frequency, 30)


class Inspection(models.Model):
    STATUS_CHOICES = [
        ('passed', 'Годен'),
        ('failed', 'Негоден'),
        ('needs_attention', 'Изисква внимание'),
    ]

    equipment = models.ForeignKey(
        Equipment,
        on_delete=models.CASCADE,
        related_name='inspections',
        help_text="Оборудване"
    )
    inspection_type = models.ForeignKey(
        InspectionType,
        on_delete=models.PROTECT,
        related_name='inspections',
        help_text="Тип проверка"
    )
    inspection_date = models.DateField(
        help_text="Дата на изпълнение на проверката"
    )
    next_inspection_date = models.DateField(
        blank=True,
        null=True,
        help_text="Следваща дата на проверка (автоматично изчислена)"
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        help_text="Статус на проверката"
    )
    technician = models.ForeignKey(
        'equipment.Technician',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='inspections',
        verbose_name="Техник/Изпълнител",
        help_text="Техник извършил проверката"
    )
    inspector_name = models.CharField(
        max_length=100,
        blank=True,
        help_text="Име на проверяващия (старо поле за справка)"
    )
    findings = models.TextField(
        help_text="Констатации и резултати от проверката"
    )
    corrective_actions = models.TextField(
        blank=True,
        null=True,
        help_text="Коригиращи действия (ако има такива)"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Проверка"
        verbose_name_plural = "Проверки"
        ordering = ['-inspection_date']

    def __str__(self):
        return f"{self.equipment.asset_number} - {self.inspection_type.name} ({self.inspection_date})"

    def save(self, *args, **kwargs):
        """Автоматично изчислява next_inspection_date на база честотата"""
        from datetime import timedelta
        if not self.next_inspection_date and self.inspection_date and self.inspection_type:
            days = self.inspection_type.get_frequency_days()
            self.next_inspection_date = self.inspection_date + timedelta(days=days)
        super().save(*args, **kwargs)
        # Актуализира статуса на оборудването след записване на проверка
        self.equipment.update_status()
