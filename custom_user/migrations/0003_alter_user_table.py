# Generated by Django 3.2.6 on 2021-09-17 07:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('custom_user', '0002_alter_user_role'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='user',
            table='custom_user',
        ),
    ]
