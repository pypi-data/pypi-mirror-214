# Generated by Django 2.2.23 on 2021-09-15 14:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('django_cog', '0014_auto_20210915_1035'),
    ]

    operations = [
        migrations.AddField(
            model_name='cogerror',
            name='error_type',
            field=models.CharField(blank=True, max_length=1024, null=True),
        ),
    ]
