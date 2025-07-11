# Generated by Django 5.2.1 on 2025-06-11 01:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('voucher', '0003_voucherusage_mac_address_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='voucher',
            name='usage_count',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='voucher',
            name='usage_limit',
            field=models.PositiveIntegerField(default=1),
        ),
        migrations.AlterUniqueTogether(
            name='voucherusage',
            unique_together={('voucher', 'mac_address')},
        ),
    ]
