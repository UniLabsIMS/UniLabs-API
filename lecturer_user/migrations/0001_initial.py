# Generated by Django 3.2.6 on 2021-09-17 06:57

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('custom_user', '0002_alter_user_role'),
        ('department', '0001_initial'),
        ('lab', '0003_rename_lab_id_lab_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='Lecturer',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='custom_user.user')),
                ('lecturer_id', models.CharField(max_length=255, unique=True)),
                ('department', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='department.department')),
            ],
            options={
                'db_table': 'lecturer',
            },
            bases=('custom_user.user',),
        ),
        migrations.CreateModel(
            name='LabLecturer',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('lab', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lab.lab')),
                ('lecturer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lecturer_user.lecturer')),
            ],
            options={
                'db_table': 'lab_lecturer',
                'unique_together': {('lecturer', 'lab')},
            },
        ),
    ]
