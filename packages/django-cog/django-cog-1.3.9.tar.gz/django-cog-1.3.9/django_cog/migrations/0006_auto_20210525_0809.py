# Generated by Django 2.2.23 on 2021-05-25 12:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('django_cog', '0005_auto_20210519_1006'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='taskrun',
            options={},
        ),
        migrations.AlterField(
            model_name='pipeline',
            name='schedule',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='django_celery_beat.CrontabSchedule'),
        ),
    ]
