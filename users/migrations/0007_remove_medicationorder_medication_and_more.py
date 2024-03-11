# Generated by Django 5.0.3 on 2024-03-09 13:52

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_property_medicationorder_order_number_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='medicationorder',
            name='medication',
        ),
        migrations.RemoveField(
            model_name='medicationorder',
            name='quantity',
        ),
        migrations.RemoveField(
            model_name='medicationorder',
            name='total_amount',
        ),
        migrations.RemoveField(
            model_name='medicationorder',
            name='unit_price',
        ),
        migrations.AddField(
            model_name='medicationorder',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField()),
                ('medication', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.medication')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.medicationorder')),
            ],
        ),
        migrations.AddField(
            model_name='medicationorder',
            name='medications',
            field=models.ManyToManyField(through='users.OrderItem', to='users.medication'),
        ),
    ]