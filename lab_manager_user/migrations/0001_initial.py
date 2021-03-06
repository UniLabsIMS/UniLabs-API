# Generated by Django 3.2.6 on 2021-08-27 14:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('lab', '0003_rename_lab_id_lab_id'),
        ('department', '0001_initial'),
        ('custom_user', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='LabManager',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='custom_user.user')),
                ('department', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='department.department')),
                ('lab', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lab.lab')),
            ],
            options={
                'abstract': False,
            },
            bases=('custom_user.user',),
        ),
    ]
