# Generated by Django 5.0.3 on 2024-03-06 14:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_alter_patient_age'),
    ]

    operations = [
        migrations.AddField(
            model_name='patient',
            name='deleted',
            field=models.BooleanField(default=False),
        ),
    ]