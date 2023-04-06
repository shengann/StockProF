# Generated by Django 4.0.5 on 2023-04-05 04:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='savedResult',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('portfolioList', models.TextField()),
                ('outlierList', models.TextField()),
                ('portfolioTYpe', models.TextField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sacedResult', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]