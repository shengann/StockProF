# Generated by Django 4.0.5 on 2023-04-10 21:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accInfo', '0006_savedresult_remarks'),
    ]

    operations = [
        migrations.AddField(
            model_name='savedresult',
            name='outlierTypeOptions',
            field=models.JSONField(default=list),
        ),
    ]
