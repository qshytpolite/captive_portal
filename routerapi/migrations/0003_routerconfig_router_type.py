# Generated by Django 5.2.1 on 2025-06-11 02:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('routerapi', '0002_routerconfig_delete_routersession'),
    ]

    operations = [
        migrations.AddField(
            model_name='routerconfig',
            name='router_type',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
