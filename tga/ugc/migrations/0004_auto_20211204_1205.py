# Generated by Django 2.2.7 on 2021-12-04 12:05

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('ugc', '0003_auto_20191130_1356'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='faculty',
            field=models.CharField(default=django.utils.timezone.now, max_length=30),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='profile',
            name='role',
            field=models.CharField(choices=[('AD', 'Admin'), ('TR', 'Teacher'), ('ST', 'Student')], default='ST', max_length=7),
        ),
        migrations.AddField(
            model_name='profile',
            name='semestr',
            field=models.IntegerField(choices=[('1', 1), ('2', 2), ('3', 3), ('4', 4), ('5', 5), ('6', 6), ('7', 7), ('8', 8)], default='1'),
        ),
        migrations.AddField(
            model_name='profile',
            name='surname',
            field=models.CharField(default=django.utils.timezone.now, max_length=15, verbose_name='Foydalanuvchi familyasi'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='profile',
            name='external_id',
            field=models.PositiveIntegerField(unique=True, verbose_name='Foydalanuvchining Telegram ID raqami'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='name',
            field=models.CharField(max_length=15, verbose_name='Foydalanuvchi ismi'),
        ),
    ]
