# Generated by Django 5.1.6 on 2025-03-01 00:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0007_employeeprofile_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='suppliercontract',
            name='contract_details',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='suppliercontract',
            name='contract_file',
            field=models.FileField(blank=True, null=True, upload_to='supplier_contracts/'),
        ),
    ]
