# Generated by Django 3.2.6 on 2021-09-17 07:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('item_category', '0002_rename_item_category_itemcategory'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='itemcategory',
            table='item_category',
        ),
    ]