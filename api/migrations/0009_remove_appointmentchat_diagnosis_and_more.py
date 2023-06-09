# Generated by Django 4.2 on 2023-06-08 19:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0008_remove_treatment_gender_remove_treatment_max_age_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='appointmentchat',
            name='diagnosis',
        ),
        migrations.AddField(
            model_name='appointment',
            name='diagnosis',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='api.diagnosis'),
        ),
        migrations.AlterField(
            model_name='dermatologist',
            name='clinic',
            field=models.CharField(max_length=200),
        ),
    ]