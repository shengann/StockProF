# Generated by Django 4.0.5 on 2023-02-13 16:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('StockProf_app', '0006_alter_stock_address_alter_stock_assettype_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='financialratios',
            name='ticket',
        ),
        migrations.AlterField(
            model_name='stock',
            name='Address',
            field=models.CharField(blank=True, max_length=220, null=True),
        ),
        migrations.AlterField(
            model_name='stock',
            name='CIK',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
