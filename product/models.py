# -*- coding: utf-8 -*-

from django.db import models
from django.conf import settings


class Product(models.Model):
    class Meta:
        verbose_name = 'продукт'
        verbose_name_plural = 'продукты'
        indexes = (models.Index(fields=('bar_code', )), )

    name = models.CharField(max_length=255, verbose_name='название')
    description = models.TextField(max_length=10000, null=True, blank=True, verbose_name='описание')
    composition = models.TextField(max_length=10000, null=True, blank=True, verbose_name='состав')
    bar_code = models.CharField(max_length=13, unique=True, verbose_name='штрих-код')
    image = models.ImageField(upload_to='product_images', null=True, blank=True, verbose_name='картинка')

    def __str__(self):
        return self.name


class UserProduct(models.Model):
    class Meta:
        verbose_name = 'продукт пользователя'
        verbose_name_plural = 'продукты пользователя'

    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='пользователь', on_delete=models.PROTECT)
    product = models.ForeignKey('product.Product', verbose_name='продукт', on_delete=models.PROTECT)
    due_to = models.DateField(verbose_name='годен до')
    consumed = models.BooleanField(default=False, verbose_name = 'сожрано?')
    created_at = models.DateTimeField()
