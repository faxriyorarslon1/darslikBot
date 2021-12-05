from django.db import models

ROLE_OF_USER_CHOICES = [
    ('AD', 'Admin'),
    ('TR', 'Teacher'),
    ('ST', 'Student')
]

SEMESTR_OF_USER_CHOICES = [
    ('1', 1),
    ('2', 2),
    ('3', 3),
    ('4', 4),
    ('5', 5),
    ('6', 6),
    ('7', 7),
    ('8', 8)
]


class Profile(models.Model):
    external_id = models.PositiveIntegerField(
        verbose_name='Foydalanuvchining Telegram ID raqami',
        unique=True,
    )
    name = models.CharField(max_length=15,
        verbose_name='Foydalanuvchi ismi',
    )
    surname = models.CharField(max_length=15,
        verbose_name='Foydalanuvchi familyasi',
    )
    role = models.CharField(max_length=7,choices=ROLE_OF_USER_CHOICES, default='ST')
    semestr = models.IntegerField(choices=SEMESTR_OF_USER_CHOICES, default='1')
    faculty = models.CharField(max_length=30)
    phone = models.CharField(max_length=13, verbose_name="Telefon raqam")

    def __str__(self):
        return f'#{self.external_id} {self.name}'

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'


class Message(models.Model):
    profile = models.ForeignKey(
        to='ugc.Profile',
        verbose_name='Профиль',
        on_delete=models.PROTECT,
    )
    text = models.TextField(
        verbose_name='Текст',
    )
    created_at = models.DateTimeField(
        verbose_name='Время получения',
        auto_now_add=True,
    )

    def __str__(self):
        return f'Сообщение {self.pk} от {self.profile}'

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'
