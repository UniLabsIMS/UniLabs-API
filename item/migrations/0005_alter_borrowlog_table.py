# Generated by Django 3.2.6 on 2021-09-25 02:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('item', '0004_borrowlog'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='borrowlog',
            table='borrow-log',
        ),
    ]