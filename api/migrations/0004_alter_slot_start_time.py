# Generated by Django 4.2 on 2023-06-13 07:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_alter_slot_day_of_week'),
    ]

    operations = [
        migrations.AlterField(
            model_name='slot',
            name='start_time',
            field=models.TimeField(),
        ),
    ]