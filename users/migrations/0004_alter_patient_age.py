# Generated by Django 5.0.3 on 2024-03-06 07:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_patient_created_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patient',
            name='age',
            field=models.IntegerField(),
        ),
    ]
