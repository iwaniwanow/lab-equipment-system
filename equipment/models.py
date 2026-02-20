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
        ('active', 'В експлоатация'),
        ('pending_validation', 'Чака валидиране'),
        ('pending_calibration', 'Чака калибровка'),
        ('pending_technical_review', 'Чака технически преглед'),
        ('pending_multiple', 'Чака множество проверки'),
        ('maintenance', 'На поддръжка'),
        ('out_of_service', 'Извън експлоатация'),
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
        related_name='equipment',
        help_text="Категория оборудване"
    )
    manufacturer = models.ForeignKey(
        Manufacturer,
        on_delete=models.PROTECT,
        related_name='equipment',
        help_text="Производител"
    )
    model = models.CharField(
        max_length=100,
        help_text="Модел"
    )
    serial_number = models.CharField(
        max_length=100,
        unique=True,
        help_text="Сериен номер"
    )
    location = models.CharField(
        max_length=200,
        help_text="Локация в лабораторията"
    )

    # Дата на въвеждане в експлоатация
    commissioning_date = models.DateField(
        null=True,
        blank=True,
        help_text="Дата на въвеждане в експлоатация"
    )

    # Изисквания за проверки при въвеждане в експлоатация
    requires_oq_pv = models.BooleanField(
        default=False,
        help_text="Подлежи на OQ/PV (Operational Qualification / Performance Validation)"
    )
    requires_calibration = models.BooleanField(
        default=False,
        help_text="Подлежи на калибровка (везни, pH метри и др.)"
    )
    requires_technical_review = models.BooleanField(
        default=False,
        help_text="Подлежи на технически преглед"
    )

    # Периодичност на проверките за пригодност (в месеци)
    CHECK_INTERVAL_CHOICES = [
        (1, 'Месечна'),
        (3, 'Тримесечна (3 месеца)'),
        (6, 'Шестмесечна (6 месеца)'),
        (12, 'Годишна'),
    ]
    check_interval_months = models.IntegerField(
        choices=CHECK_INTERVAL_CHOICES,
        default=12,
        help_text="Периодичност на проверки за пригодност"
    )

    status = models.CharField(
        max_length=30,
        choices=STATUS_CHOICES,
        default='active',
        help_text="Текущ статус (изчислява се автоматично на база дати)"
    )

    notes = models.TextField(
        blank=True,
        null=True,
        help_text="Допълнителни бележки"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Equipment"
        verbose_name_plural = "Equipment"
        ordering = ['asset_number']

    def __str__(self):
        return f"{self.asset_number} - {self.name}"

    def get_missing_requirements(self):
        """
        Връща списък с липсващите изисквания при въвеждане в експлоатация
        """
        missing = []

        if not self.commissioning_date:
            missing.append('commissioning_date')
            return missing  # Ако няма дата, няма смисъл да проверяваме останалото

        # Проверка за валидиране
        if self.requires_oq_pv:
            has_validation = self.maintenance_records.filter(
                maintenance_type__type='validation'
            ).exists()
            if not has_validation:
                missing.append('validation')

        # Проверка за калибровка
        if self.requires_calibration:
            has_calibration = self.maintenance_records.filter(
                maintenance_type__type='calibration'
            ).exists()
            if not has_calibration:
                missing.append('calibration')

        # Проверка за технически преглед
        if self.requires_technical_review:
            has_technical_review = self.inspections.filter(
                inspection_type__category='technical_review'
            ).exists()
            if not has_technical_review:
                missing.append('technical_review')

        return missing

    def get_missing_requirements_display(self):
        """
        Връща текстово описание на липсващите изисквания на български
        """
        missing = self.get_missing_requirements()

        if not missing:
            return "Всички изисквания са изпълнени"

        display_map = {
            'commissioning_date': 'Дата на въвеждане в експлоатация',
            'validation': 'OQ/PV Валидиране',
            'calibration': 'Калибровка',
            'technical_review': 'Технически преглед'
        }

        missing_text = [display_map.get(item, item) for item in missing]

        if len(missing_text) == 1:
            return f"Липсва: {missing_text[0]}"
        else:
            return f"Липсват: {', '.join(missing_text)}"

    def get_calculated_status(self):
        """
        Автоматично изчислява статуса на оборудването въз основа на:
        - Изпълнени ли са изискванията при въвеждане в експлоатация (OQ/PV, калибровка, технически преглед)
        - Просрочени записи за калибровка/валидиране (MaintenanceRecord)
        - Просрочени технически прегледи (Inspection)
        - Предупреждение 1 месец преди изтичане на срока
        - Резултати от последни проверки
        """
        from datetime import date, timedelta
        today = date.today()
        one_month_ahead = today + timedelta(days=30)

        # 1. Проверка дали са изпълнени изискванията при въвеждане в експлоатация
        missing_requirements = self.get_missing_requirements()

        if 'commissioning_date' in missing_requirements:
            return 'pending_validation'  # Няма дата на въвеждане

        if len(missing_requirements) > 1:
            # Липсват множество изисквания
            return 'pending_multiple'
        elif len(missing_requirements) == 1:
            # Липсва точно едно изискване
            if 'validation' in missing_requirements:
                return 'pending_validation'
            elif 'calibration' in missing_requirements:
                return 'pending_calibration'
            elif 'technical_review' in missing_requirements:
                return 'pending_technical_review'

        # 2. Проверка за просрочени или скоро изтичащи записи за калибровка
        if self.requires_calibration:
            latest_calibration = self.maintenance_records.filter(
                maintenance_type__type='calibration'
            ).order_by('-performed_date').first()

            if latest_calibration and latest_calibration.next_due_date:
                # Просрочена калибровка
                if latest_calibration.next_due_date < today:
                    return 'pending_calibration'
                # Предупреждение: изтича след 1 месец
                elif latest_calibration.next_due_date <= one_month_ahead:
                    return 'pending_calibration'

        # 3. Проверка за просрочени или скоро изтичащи записи за валидиране (OQ/PV)
        if self.requires_oq_pv:
            latest_validation = self.maintenance_records.filter(
                maintenance_type__type='validation'
            ).order_by('-performed_date').first()

            if latest_validation and latest_validation.next_due_date:
                # Просрочено валидиране
                if latest_validation.next_due_date < today:
                    return 'pending_validation'
                # Предупреждение: изтича след 1 месец
                elif latest_validation.next_due_date <= one_month_ahead:
                    return 'pending_validation'

        # 4. Проверка за просрочени или скоро изтичащи технически прегледи
        if self.requires_technical_review:
            # Вземаме само технически прегледи, НЕ проверки за пригодност
            latest_technical_review = self.inspections.filter(
                inspection_type__category='technical_review'
            ).order_by('-inspection_date').first()

            if latest_technical_review and latest_technical_review.next_inspection_date:
                # Просрочен технически преглед
                if latest_technical_review.next_inspection_date < today:
                    return 'pending_technical_review'
                # Предупреждение: изтича след 1 месец
                elif latest_technical_review.next_inspection_date <= one_month_ahead:
                    return 'pending_technical_review'

            # Проверка дали последният технически преглед е провален
            if latest_technical_review and latest_technical_review.status == 'failed':
                return 'out_of_service'

        # 5. Проверка дали последната проверка (общо) е провалена
        latest_any_inspection = self.inspections.order_by('-inspection_date').first()
        if latest_any_inspection and latest_any_inspection.status == 'failed':
            return 'out_of_service'

        # Ако всичко е наред
        return 'active'

    def update_status(self):
        """Update the status field with calculated status"""
        self.status = self.get_calculated_status()
        self.save(update_fields=['status'])

