# Generated by Django 3.2.6 on 2021-09-25 04:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('item', '0005_alter_borrowlog_table'),
    ]

    operations = [
        migrations.AlterField(
            model_name='borrowlog',
            name='due_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='borrowlog',
            name='returned_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
