# Generated by Django 2.2.7 on 2021-12-06 11:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ugc', '0002_laboratories_subjects_themes'),
    ]

    operations = [
        migrations.AlterField(
            model_name='themes',
            name='subject',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='themes', to='ugc.Subjects'),
        ),
    ]