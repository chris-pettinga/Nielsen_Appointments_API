# Generated by Django 3.2.9 on 2021-11-25 15:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointment',
            name='status',
            field=models.CharField(choices=[('a', 'Completed without issue'), ('b', 'Completed with issues'), ('c', 'Client did not show up')], max_length=2, null=True, verbose_name='Status of the appointment'),
        ),
    ]
