# Generated by Django 4.2 on 2023-06-07 03:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_rename_work_email_dermatologist_email_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='treatment',
            name='gender',
        ),
        migrations.RemoveField(
            model_name='treatment',
            name='max_age',
        ),
        migrations.RemoveField(
            model_name='treatment',
            name='min_age',
        ),
    ]
