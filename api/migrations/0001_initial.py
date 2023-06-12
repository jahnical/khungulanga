# Generated by Django 4.2 on 2023-06-12 20:57

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
            name='Appointment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('book_date', models.DateField(null=True)),
                ('appo_date', models.DateTimeField(null=True)),
                ('done', models.BooleanField(default=False)),
                ('duration', models.IntegerField(null=True)),
                ('cost', models.FloatField(default=0.0)),
                ('extra_info', models.TextField(max_length=1000, null=True)),
                ('patient_approved', models.DateTimeField(null=True)),
                ('dermatologist_approved', models.DateTimeField(null=True)),
                ('patient_rejected', models.DateTimeField(null=True)),
                ('dermatologist_rejected', models.DateTimeField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='AppointmentChat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('appointment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.appointment')),
            ],
        ),
        migrations.CreateModel(
            name='Clinic',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('latitude', models.FloatField()),
                ('longitude', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='Dermatologist',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('qualification', models.ImageField(upload_to='media/qualification/%Y/%m/%d/')),
                ('specialization', models.CharField(choices=[('COSMETIC', 'Cosmetic Dermatologist'), ('DERMATOPATHOLOGIST', 'Dermatopathologist'), ('DERMATOSURGEON', 'Dermatosurgeon'), ('IMMUNODERMATOLOGIST', 'Immunodermatologist'), ('MOHS_SURGEON', 'Mohs Surgeon'), ('PAEDIATRIC', 'Paediatric Dermatologist'), ('TELEDERMATOLOGIST', 'Teledermatologist')], default='DERMATOPATHOLOGIST', max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('phone_number', models.CharField(max_length=13)),
                ('houry_rate', models.FloatField()),
                ('clinic', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.clinic')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Diagnosis',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='media/diagnosis/%Y/%m/%d/')),
                ('body_part', models.CharField(max_length=100)),
                ('itchy', models.BooleanField(default=False)),
                ('date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Disease',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(max_length=500)),
                ('severity', models.IntegerField(choices=[(1, 'Mild'), (2, 'Moderate'), (3, 'Severe')])),
            ],
        ),
        migrations.CreateModel(
            name='Treatment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField(max_length=500)),
                ('title', models.CharField(max_length=100)),
                ('disease', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.disease')),
            ],
        ),
        migrations.CreateModel(
            name='Slot',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_time', models.IntegerField()),
                ('scheduled', models.BooleanField(default=False)),
                ('day_of_week', models.IntegerField(choices=[(0, 'Monday'), (1, 'Tuesday'), (2, 'Wednesday'), (3, 'Thursday'), (4, 'Friday'), (5, 'Saturday'), (6, 'Sunday')])),
                ('dermatologist', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.dermatologist')),
            ],
        ),
        migrations.CreateModel(
            name='Prediction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('probability', models.FloatField(default=0.0)),
                ('diagnosis', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.diagnosis')),
                ('disease', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='api.disease')),
            ],
        ),
        migrations.CreateModel(
            name='Patient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dob', models.DateTimeField()),
                ('gender', models.CharField(choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')], max_length=1)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='diagnosis',
            name='patient',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.patient'),
        ),
        migrations.CreateModel(
            name='ChatMessage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(max_length=1000)),
                ('time', models.DateTimeField(auto_now_add=True)),
                ('seen', models.BooleanField(default=False)),
                ('appointment', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='api.appointment')),
                ('chat', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.appointmentchat')),
                ('diagnosis', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='api.diagnosis')),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='appointmentchat',
            name='dermatologist',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.dermatologist'),
        ),
        migrations.AddField(
            model_name='appointmentchat',
            name='patient',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.patient'),
        ),
        migrations.AddField(
            model_name='appointment',
            name='dermatologist',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.dermatologist'),
        ),
        migrations.AddField(
            model_name='appointment',
            name='diagnosis',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='api.diagnosis'),
        ),
        migrations.AddField(
            model_name='appointment',
            name='patient',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.patient'),
        ),
        migrations.AddField(
            model_name='appointment',
            name='slot',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.slot'),
        ),
    ]
