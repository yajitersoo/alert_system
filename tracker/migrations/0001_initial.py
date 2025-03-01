# Generated by Django 5.1.6 on 2025-02-28 06:54

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='SupplierContract',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('supplier_name', models.CharField(max_length=255)),
                ('contract_file', models.FileField(upload_to='supplier_contracts/')),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='EmployeeProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('employee_type', models.CharField(choices=[('National Staff', 'National Staff'), ('Expatriate Staff', 'Expatriate Staff')], max_length=20)),
                ('position', models.CharField(max_length=255)),
                ('department', models.CharField(blank=True, max_length=255, null=True)),
                ('phone_number', models.CharField(blank=True, max_length=20, null=True)),
                ('date_of_birth', models.DateField(blank=True, null=True)),
                ('hire_date', models.DateField()),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ExpatDocument',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('document_type', models.CharField(max_length=255)),
                ('document_file', models.FileField(upload_to='expat_documents/')),
                ('expiry_date', models.DateField()),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tracker.employeeprofile')),
            ],
        ),
        migrations.CreateModel(
            name='StaffContract',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('contract_file', models.FileField(blank=True, null=True, upload_to='contracts/')),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tracker.employeeprofile')),
            ],
        ),
        migrations.CreateModel(
            name='StaffLeave',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('description', models.TextField()),
                ('status', models.CharField(choices=[('Pending', 'Pending'), ('Approved', 'Approved'), ('Rejected', 'Rejected')], default='Pending', max_length=10)),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tracker.employeeprofile')),
            ],
        ),
    ]
