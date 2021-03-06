# Generated by Django 3.2.6 on 2021-09-24 16:54

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('lab', '0004_alter_lab_table'),
        ('student_user', '0002_alter_student_table'),
        ('item', '0003_alter_item_options'),
    ]

    operations = [
        migrations.CreateModel(
            name='BorrowLog',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('state', models.CharField(choices=[('Borrowed', 'Borrowed'), ('Temp_Borrowed', 'Temp_Borrowed'), ('Returned', 'Returned')], max_length=31)),
                ('due_date', models.DateField(blank=True)),
                ('returned_date', models.DateField(blank=True)),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='item.item')),
                ('lab', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lab.lab')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='student_user.student')),
            ],
        ),
    ]
