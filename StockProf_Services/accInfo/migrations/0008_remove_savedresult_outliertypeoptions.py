# Generated by Django 4.0.5 on 2023-04-10 22:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accInfo', '0007_savedresult_outliertypeoptions'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='savedresult',
            name='outlierTypeOptions',
        ),
    ]
