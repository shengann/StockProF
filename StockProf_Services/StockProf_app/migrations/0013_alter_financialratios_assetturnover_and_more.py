# Generated by Django 4.0.5 on 2023-02-14 02:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('StockProf_app', '0012_rename_ticket_financialratios_ticker'),
    ]

    operations = [
        migrations.AlterField(
            model_name='financialratios',
            name='assetturnover',
            field=models.DecimalField(decimal_places=2, max_digits=6),
        ),
        migrations.AlterField(
            model_name='financialratios',
            name='debttoequity',
            field=models.DecimalField(decimal_places=2, max_digits=6),
        ),
        migrations.AlterField(
            model_name='financialratios',
            name='dividendyield',
            field=models.DecimalField(decimal_places=2, max_digits=6),
        ),
        migrations.AlterField(
            model_name='financialratios',
            name='pricetoearnings',
            field=models.DecimalField(decimal_places=2, max_digits=6),
        ),
        migrations.AlterField(
            model_name='financialratios',
            name='quickratio',
            field=models.DecimalField(decimal_places=2, max_digits=6),
        ),
        migrations.AlterField(
            model_name='financialratios',
            name='roe',
            field=models.DecimalField(decimal_places=2, max_digits=6),
        ),
    ]
