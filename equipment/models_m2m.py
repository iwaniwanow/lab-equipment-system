"""
Many-to-Many relationships models for Equipment
"""
from django.db import models
from equipment.models import Equipment
from django.contrib.auth.models import User


class Tag(models.Model):
    """
    Етикети/Тагове за категоризация на оборудването
    Many-to-Many relationship с Equipment
    """
    name = models.CharField(
        max_length=50,
        unique=True,
        verbose_name="Име на таг",
        help_text="Кратко име (напр. 'Критично', 'GMP', 'Нов', 'Legacy')"
    )
    color = models.CharField(
        max_length=7,
        default='#007bff',
        verbose_name="Цвят (hex)",
        help_text="Цвят за визуализация (напр. #FF5733)"
    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name="Описание"
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="Активен"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    # Many-to-Many relationship with Equipment
    equipment = models.ManyToManyField(
        Equipment,
        related_name='tags',
        blank=True,
        verbose_name="Оборудване"
    )

    class Meta:
        verbose_name = "Таг"
        verbose_name_plural = "Тагове"
        ordering = ['name']

    def __str__(self):
        return self.name

    def equipment_count(self):
        """Брой оборудване с този таг"""
        return self.equipment.count()


class Document(models.Model):
    """
    Документи свързани с оборудването
    Many-to-Many relationship с Equipment
    """
    DOCUMENT_TYPE_CHOICES = [
        ('manual', 'Ръководство за употреба'),
        ('certificate', 'Сертификат'),
        ('protocol', 'Протокол'),
        ('validation', 'Документация за валидиране'),
        ('sop', 'SOP (Standard Operating Procedure)'),
        ('drawing', 'Технически чертеж'),
        ('photo', 'Снимка'),
        ('other', 'Друг'),
    ]

    name = models.CharField(
        max_length=200,
        verbose_name="Име на документ"
    )
    document_type = models.CharField(
        max_length=20,
        choices=DOCUMENT_TYPE_CHOICES,
        default='other',
        verbose_name="Тип документ"
    )
    file = models.FileField(
        upload_to='equipment_documents/%Y/%m/',
        verbose_name="Файл"
    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name="Описание"
    )
    uploaded_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='uploaded_documents',
        verbose_name="Качен от"
    )
    uploaded_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата на качване"
    )
    version = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        verbose_name="Версия",
        help_text="Версия на документа (напр. 1.0, 2.5)"
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="Активен"
    )

    # Many-to-Many relationship with Equipment
    equipment = models.ManyToManyField(
        Equipment,
        related_name='documents',
        blank=True,
        verbose_name="Оборудване"
    )

    class Meta:
        verbose_name = "Документ"
        verbose_name_plural = "Документи"
        ordering = ['-uploaded_at']

    def __str__(self):
        return f"{self.name} ({self.get_document_type_display()})"

    def equipment_count(self):
        """Брой оборудване свързано с този документ"""
        return self.equipment.count()

    def file_size_mb(self):
        """Размер на файла в MB"""
        if self.file:
            return round(self.file.size / (1024 * 1024), 2)
        return 0


class EquipmentGroup(models.Model):
    """
    Групи оборудване - за групиране на оборудване по произволен критерий
    Many-to-Many relationship с Equipment
    """
    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name="Име на група"
    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name="Описание"
    )
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='created_equipment_groups',
        verbose_name="Създадена от"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(
        default=True,
        verbose_name="Активна"
    )

    # Many-to-Many relationship with Equipment
    equipment = models.ManyToManyField(
        Equipment,
        related_name='groups',
        blank=True,
        verbose_name="Оборудване",
        help_text="Изберете оборудване за тази група"
    )

    class Meta:
        verbose_name = "Група оборудване"
        verbose_name_plural = "Групи оборудване"
        ordering = ['name']

    def __str__(self):
        return self.name

    def equipment_count(self):
        """Брой оборудване в групата"""
        return self.equipment.count()

