from django.db import models
from django.contrib.auth.models import User
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
        verbose_name = "Производител"
        verbose_name_plural = "Производители"
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
        verbose_name = "Категория оборудване"
        verbose_name_plural = "Категории оборудване"
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
    location_old = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        verbose_name="Локация (старо поле)",
        help_text="Стара локация (само текст)"
    )
    location = models.ForeignKey(
        'Location',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='equipment',
        verbose_name="Локация",
        help_text="Локация на оборудването"
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
        verbose_name = "Оборудване"
        verbose_name_plural = "Оборудване"
        ordering = ['asset_number']

    def __str__(self):
        return f"{self.asset_number} - {self.name}"

    def get_missing_requirements(self):
        missing = []

        if not self.commissioning_date:
            missing.append('commissioning_date')
            return missing

        if self.requires_oq_pv:
            has_validation = self.maintenance_records.filter(
                maintenance_type__type='validation'
            ).exists()
            if not has_validation:
                missing.append('validation')

        if self.requires_calibration:
            has_calibration = self.maintenance_records.filter(
                maintenance_type__type='calibration'
            ).exists()
            if not has_calibration:
                missing.append('calibration')

        if self.requires_technical_review:
            has_technical_review = self.inspections.filter(
                inspection_type__category='technical_review'
            ).exists()
            if not has_technical_review:
                missing.append('technical_review')

        return missing

    def get_missing_requirements_display(self):
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
        from datetime import date, timedelta
        today = date.today()
        one_month_ahead = today + timedelta(days=30)

        missing_requirements = self.get_missing_requirements()

        if 'commissioning_date' in missing_requirements:
            return 'pending_validation'

        if len(missing_requirements) > 1:
            return 'pending_multiple'
        elif len(missing_requirements) == 1:
            if 'validation' in missing_requirements:
                return 'pending_validation'
            elif 'calibration' in missing_requirements:
                return 'pending_calibration'
            elif 'technical_review' in missing_requirements:
                return 'pending_technical_review'

        if self.requires_calibration:
            latest_calibration = self.maintenance_records.filter(
                maintenance_type__type='calibration'
            ).order_by('-performed_date').first()

            if latest_calibration and latest_calibration.next_due_date:
                if latest_calibration.next_due_date < today:
                    return 'pending_calibration'
                elif latest_calibration.next_due_date <= one_month_ahead:
                    return 'pending_calibration'

        if self.requires_oq_pv:
            latest_validation = self.maintenance_records.filter(
                maintenance_type__type='validation'
            ).order_by('-performed_date').first()

            if latest_validation and latest_validation.next_due_date:
                if latest_validation.next_due_date < today:
                    return 'pending_validation'
                elif latest_validation.next_due_date <= one_month_ahead:
                    return 'pending_validation'

        if self.requires_technical_review:
            latest_technical_review = self.inspections.filter(
                inspection_type__category='technical_review'
            ).order_by('-inspection_date').first()

            if latest_technical_review and latest_technical_review.next_inspection_date:
                if latest_technical_review.next_inspection_date < today:
                    return 'pending_technical_review'
                elif latest_technical_review.next_inspection_date <= one_month_ahead:
                    return 'pending_technical_review'

            if latest_technical_review and latest_technical_review.status == 'failed':
                return 'out_of_service'

        latest_any_inspection = self.inspections.order_by('-inspection_date').first()
        if latest_any_inspection and latest_any_inspection.status == 'failed':
            return 'out_of_service'

        return 'active'

    def update_status(self):
        self.status = self.get_calculated_status()
        self.save(update_fields=['status'])


class Department(models.Model):
    code = models.CharField(max_length=10, unique=True, verbose_name="Код на звено")
    name = models.CharField(max_length=200, verbose_name="Наименование")
    full_name = models.CharField(max_length=300, verbose_name="Пълно наименование")
    manager = models.CharField(max_length=200, blank=True, verbose_name="Ръководител")
    contact = models.CharField(max_length=200, blank=True, verbose_name="Контакт")
    is_active = models.BooleanField(default=True, verbose_name="Активно")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Звено"
        verbose_name_plural = "Звена"
        ordering = ['code']

    def __str__(self):
        return f"{self.code} - {self.name}"


class Location(models.Model):
    CATEGORY_CHOICES = [
        ('A', 'Категория A'),
        ('B', 'Категория B'),
        ('C', 'Категория C'),
        ('D', 'Категория D'),
        ('E', 'Категория E'),
    ]

    code = models.CharField(max_length=20, unique=True, verbose_name="Код на локация",
                           help_text="Формат: E-1-102 (Категория-Етаж-Помещение)")
    category = models.CharField(max_length=1, choices=CATEGORY_CHOICES,
                               verbose_name="Категория")
    floor = models.IntegerField(verbose_name="Етаж")
    room_number = models.CharField(max_length=10, verbose_name="Номер на помещение")

    name = models.CharField(max_length=200, verbose_name="Име на лаборатория/помещение",
                          help_text="Напр: Лаборатория ККП")
    department = models.ForeignKey(Department, on_delete=models.SET_NULL,
                                  null=True, blank=True,
                                  related_name='locations',
                                  verbose_name="Звено")

    building = models.CharField(max_length=100, blank=True, verbose_name="Сграда")
    area_sqm = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True,
                                   verbose_name="Площ (кв.м)")
    responsible_person = models.CharField(max_length=200, blank=True,
                                         verbose_name="Отговорно лице")
    phone = models.CharField(max_length=20, blank=True, verbose_name="Телефон")
    notes = models.TextField(blank=True, verbose_name="Забележки")

    has_controlled_temperature = models.BooleanField(default=False,
                                                     verbose_name="Контролирана температура")
    has_controlled_humidity = models.BooleanField(default=False,
                                                  verbose_name="Контролирана влажност")

    is_active = models.BooleanField(default=True, verbose_name="Активна")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Локация"
        verbose_name_plural = "Локации"
        ordering = ['category', 'floor', 'room_number']
        unique_together = [['category', 'floor', 'room_number']]

    def __str__(self):
        return f"{self.code} - {self.name}"

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = f"{self.category}-{self.floor}-{self.room_number}"
        super().save(*args, **kwargs)

    def get_full_description(self):
        desc = [self.code, self.name]
        if self.department:
            desc.append(f"({self.department.code})")
        if self.building:
            desc.append(f"Сграда {self.building}")
        return " - ".join(desc)


class Technician(models.Model):
    SPECIALIZATION_CHOICES = [
        ('electrical', 'Електротехник'),
        ('mechanical', 'Механик'),
        ('it', 'IT специалист'),
        ('metrology', 'Метролог'),
        ('quality_control', 'Контрол на качеството'),
        ('laboratory', 'Лаборант'),
        ('hvac', 'Отопление/Климатици'),
        ('safety', 'Пожарна безопасност'),
        ('general', 'Общи проверки'),
        ('other', 'Друго'),
    ]

    # Връзка с потребител (опционална - може да е и външен техник)
    user = models.OneToOneField(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='technician_profile',
        verbose_name="Потребител",
        help_text="Свързване с потребителски акаунт (само за вътрешни техници)"
    )

    first_name = models.CharField(max_length=100, verbose_name="Име")
    last_name = models.CharField(max_length=100, verbose_name="Фамилия")
    position = models.CharField(max_length=200, blank=True, verbose_name="Длъжност")
    specialization = models.CharField(max_length=50, choices=SPECIALIZATION_CHOICES,
                                     default='general', verbose_name="Специализация")

    phone = models.CharField(max_length=20, blank=True, verbose_name="Телефон")
    email = models.EmailField(blank=True, verbose_name="Email")

    department = models.ForeignKey(Department, on_delete=models.SET_NULL,
                                  null=True, blank=True,
                                  related_name='technicians',
                                  verbose_name="Звено")
    company = models.CharField(max_length=200, blank=True, verbose_name="Външна фирма",
                              help_text="Попълва се само ако е от външна фирма")

    certification = models.TextField(blank=True, verbose_name="Сертификати/Квалификации")
    certification_expiry = models.DateField(null=True, blank=True,
                                           verbose_name="Валидност на сертификат до")

    notes = models.TextField(blank=True, verbose_name="Забележки")
    is_active = models.BooleanField(default=True, verbose_name="Активен")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Техник"
        verbose_name_plural = "Техници"
        ordering = ['last_name', 'first_name']

    def __str__(self):
        name = f"{self.first_name} {self.last_name}"
        if self.position:
            name += f" - {self.position}"
        if self.department:
            name += f" ({self.department.code})"
        elif self.company:
            name += f" ({self.company})"
        return name

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    def save(self, *args, **kwargs):
        # Ако има свързан потребител, синхронизирай данните
        if self.user:
            # Ако няма име и фамилия, вземи ги от потребителя
            if not self.first_name:
                self.first_name = self.user.first_name
            if not self.last_name:
                self.last_name = self.user.last_name
            if not self.email:
                self.email = self.user.email

            # Синхронизирай звеното от UserProfile ако има
            if hasattr(self.user, 'profile') and self.user.profile.department and not self.department:
                self.department = self.user.profile.department

        super().save(*args, **kwargs)

