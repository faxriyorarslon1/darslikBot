from django.db import models
from django.contrib.auth.models import User 

ROLE_OF_USER_CHOICES = [
    ('AD', 'Admin'),
    ('TR', 'Teacher'),
    ('ST', 'Student')
]

SEMESTR_OF_USER_CHOICES = [
    (0, 0),
    (1, 1),
    (2, 2),
    (3, 3),
    (4, 4),
    (5, 5),
    (6, 6),
    (7, 7),
    (8, 8)
]

class Faculty(models.Model):
    name = models.CharField(max_length = 45, blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Fakultet'
        verbose_name_plural = 'Fakultetlar'


class Area(models.Model):
    faculty = models.ForeignKey(Faculty, on_delete = models.CASCADE)
    name = models.CharField(max_length = 45, blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Yo\'nalish'
        verbose_name_plural = 'Yo\'nalishlar'

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
    semestr = models.IntegerField(choices=SEMESTR_OF_USER_CHOICES, default=0)
    faculty = models.ForeignKey(Faculty, verbose_name="Fakultet", on_delete = models.CASCADE)
    area = models.ForeignKey(Area, verbose_name = "Yo'nalish", on_delete = models.CASCADE)
    phone = models.CharField(max_length=13, verbose_name="Telefon raqam")

    def __str__(self):
        return f'#{self.external_id} {self.name}'

    class Meta:
        verbose_name = 'Foydalanuvchi'
        verbose_name_plural = 'Foydalanuvchilar'


class Subjects(models.Model):
    area = models.ForeignKey(Area, on_delete=models.CASCADE)
    name = models.CharField(verbose_name="nomi",max_length=45)
    semestr = models.IntegerField(choices=SEMESTR_OF_USER_CHOICES,default=0)
    themes_list = models.FileField(verbose_name="Mavzular ro'yxati", upload_to="theme_list/")
    teacher = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'#{self.name} {self.semestr}'

    class Meta:
        verbose_name = 'Fan'
        verbose_name_plural = 'Fanlar'
        

class Laboratories(models.Model):
    teacher = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subjects, on_delete=models.CASCADE)
    name = models.CharField(verbose_name="nomi", max_length=100)
    ppt_file = models.CharField(verbose_name="Taqdimot manzili", max_length=100)
    word_file = models.CharField(verbose_name="Laboratoriya manzili", max_length=100)
    video = models.CharField(verbose_name="Video manzili", max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Laboratoriya'
        verbose_name_plural = 'Laboratoriyalar'



class Lectures(models.Model):
    teacher = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subjects, on_delete=models.CASCADE)
    name = models.CharField(verbose_name="nomi", max_length=100)
    ppt_file = models.CharField(verbose_name="Taqdimot manzili", max_length=100)
    word_file = models.CharField(verbose_name="Laboratoriya manzili", max_length=100)
    video = models.CharField(verbose_name="Video manzili", max_length=100)
    other_file  =models.CharField(verbose_name="Qo'shimcha Fayl manzili", max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Ma\'ruza'
        verbose_name_plural = 'Ma\'ruzalar'        