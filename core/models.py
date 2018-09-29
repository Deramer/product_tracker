from django.contrib.auth.models import AbstractUser
from django.contrib.staticfiles.templatetags.staticfiles import static
from django.db import models


class User(AbstractUser):
    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'

    first_name = models.CharField(verbose_name='имя', max_length=60, blank=True, null=True)
    last_name = models.CharField(verbose_name='фамилия', max_length=80, blank=True, null=True)
    avatar = models.ImageField(verbose_name='аватар', upload_to='avatars', null=True, blank=True)

    created_at = models.DateTimeField(verbose_name='дата регистрации', auto_now_add=True)

    def get_full_name(self):
        parts = []
        if self.first_name:
            parts.append(self.first_name)
        if self.last_name:
            parts.append(self.last_name)
        return ' '.join(parts)

    def get_short_name(self):
        return f'{self.email}'

    def __str__(self):
        return self.get_short_name()

    def get_avatar(self):
        if self.avatar:
            return self.avatar.url
        else:
            return static('core/no-avatar-icon.png')
