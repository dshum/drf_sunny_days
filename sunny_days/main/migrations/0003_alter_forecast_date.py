# Generated by Django 4.1.7 on 2023-03-31 07:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_alter_forecast_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='forecast',
            name='date',
            field=models.DateField(),
        ),
    ]
