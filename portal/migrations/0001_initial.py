# Generated by Django 5.2.1 on 2025-06-04 21:02

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('voucher', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CaptiveSession',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mac_address', models.CharField(max_length=17)),
                ('ip_address', models.GenericIPAddressField()),
                ('user_agent', models.TextField(blank=True)),
                ('start_time', models.DateTimeField(auto_now_add=True)),
                ('end_time', models.DateTimeField(blank=True, null=True)),
                ('is_authenticated', models.BooleanField(default=False)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('voucher_used', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='voucher.voucher')),
            ],
            options={
                'verbose_name': 'Captive Session',
                'verbose_name_plural': 'Captive Sessions',
                'ordering': ['-start_time'],
            },
        ),
    ]
