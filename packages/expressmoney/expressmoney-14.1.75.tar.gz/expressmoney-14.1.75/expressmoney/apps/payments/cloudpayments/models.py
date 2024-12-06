from django.db import models


class BankCard(models.Model):
    created = models.DateTimeField('Создана', auto_now_add=True)
    updated = models.DateTimeField('Изменена', auto_now=True)
    user_id = models.PositiveIntegerField()
    is_active = models.BooleanField('Активна', default=True)
    bin = models.CharField('Бин', max_length=6)
    number = models.CharField('Номер', max_length=4)
    expiry_month = models.PositiveSmallIntegerField('Месяц')
    expiry_year = models.PositiveSmallIntegerField('Год')
    token = models.CharField('Токен', max_length=1024, unique=True)

    def __str__(self):
        return f'{self.bin}****{self.number}'

    class Meta:
        managed = False
        verbose_name_plural = 'Банковские карты'
        verbose_name = 'Банковская карта'
        unique_together = ('bin', 'number', 'expiry_month', 'expiry_year')
        constraints = (
            models.UniqueConstraint(fields=['bin', 'number', 'expiry_month', 'expiry_year'], name='unique_bank_card'),
        )



class HolderName(models.Model):
    created = models.DateTimeField('Создана', auto_now_add=True)
    user_id = models.PositiveIntegerField()
    full_number = models.CharField('Номер карты', max_length=64, blank=True)
    number = models.CharField('Номер', max_length=4, help_text='Последние 4 цифры номера карты', blank=True)

    bin = models.CharField('BIN', max_length=6, blank=True)
    brand = models.CharField('Марка', max_length=64, blank=True)
    type = models.CharField('Тип', max_length=24, blank=True)
    category = models.CharField('Категория', max_length=64, blank=True)
    issuer = models.CharField('Банк', max_length=128, blank=True)
    issuer_phone = models.CharField('Номер телефона банка', max_length=128, blank=True)
    issuer_url = models.URLField('Сайт банка', max_length=128, blank=True)
    iso_code2 = models.CharField('Страна', max_length=24, help_text='по стандарту ISO 3166-1 alpha-2', blank=True)
    iso_code3 = models.CharField('Страна', max_length=24, help_text='по стандарту ISO 3166-1 alpha-3', blank=True)
    country_name = models.CharField('Страна полное название', max_length=64, blank=True)

    def save(self, *args, **kwargs):
        pass

    def __str__(self):
        return str(self.full_number)

    class Meta:
        managed = False
        verbose_name_plural = 'Имена владельцев'
        verbose_name = 'Имя владельца'
