from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


class PhoneRange(models.Model):
    """Модель для хранения диапазонов номеров из реестра."""

    registry_source = models.CharField(
        max_length=10,
        choices=[
            ('3xx', 'Диапазон 3XX'),
            ('4xx', 'Диапазон 4XX'),
            ('8xx', 'Диапазон 8XX'),
            ('9xx', 'Диапазон 9XX'),
        ],
        default=None,
        null=True,
        db_index=True,
    )
    abc = models.IntegerField(
        verbose_name='Код ABC/DEF',
        db_index=True,
        help_text='Первые 3 цифры номера (без 7/8)',
        validators=[
            MinValueValidator(0),
            MaxValueValidator(999)
        ],
    )
    start_range = models.IntegerField(
        verbose_name='Начало диапазона',
        db_index=True,
        help_text='Начало диапазона в формате хвоста от 1 до 7 знаков',
        validators=[
            MinValueValidator(0),
            MaxValueValidator(9999999)
        ],
    )
    end_range = models.IntegerField(
        verbose_name='Конец диапазона',
        db_index=True,
        help_text='Конец диапазона в формате хвоста от 1 до 7 знаков',
        validators=[
            MinValueValidator(0),
            MaxValueValidator(9999999)
        ],
    )
    capacity = models.IntegerField(
        verbose_name='Емкость',
        blank=True,
        null=True,
    )
    operator = models.CharField(
        verbose_name='Оператор связи',
        max_length=255,
    )
    region = models.CharField(
        verbose_name='Регион',
        max_length=255,
        blank=True,
        null=True,
    )
    territory = models.CharField(
        verbose_name='Территория ГАР',
        max_length=255,
        blank=True,
        null=True,
    )
    inn = models.CharField(
        verbose_name='ИНН',
        max_length=12,
        blank=True,
        null=True,
    )
    update_date = models.DateField(
        verbose_name='Дата обновления',
        auto_now=True,
    )

    class Meta:
        verbose_name = 'Диапазон номеров'
        verbose_name_plural = 'Диапазоны номеров'
        indexes = [
            models.Index(fields=['abc', 'start_range', 'end_range']),
        ]
        constraints = [
            models.CheckConstraint(
                check=models.Q(start_range__lte=models.F('end_range')),
                name='start_lte_end'
            ),
        ]

    def __str__(self):
        return f'{self.abc * 10000000 + self.start_range}-{self.abc * 10000000 + self.end_range} : {self.operator}'
