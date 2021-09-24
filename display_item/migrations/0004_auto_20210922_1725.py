# Generated by Django 3.2.6 on 2021-09-22 11:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('item_category', '0003_alter_itemcategory_table'),
        ('display_item', '0003_alter_displayitem_table'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='displayitem',
            options={'ordering': ('-added_on',)},
        ),
        migrations.AlterUniqueTogether(
            name='displayitem',
            unique_together={('name', 'item_category')},
        ),
    ]