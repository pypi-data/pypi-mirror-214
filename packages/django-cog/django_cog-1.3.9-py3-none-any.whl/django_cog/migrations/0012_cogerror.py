# Generated by Django 2.2.23 on 2021-09-15 13:26

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('django_cog', '0011_cogerrorhandler'),
    ]

    operations = [
        migrations.CreateModel(
            name='CogError',
            fields=[
                ('timestamp', models.DateTimeField(auto_created=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('modified_date', models.DateTimeField(auto_now=True)),
                ('traceback', models.TextField(blank=True, null=True)),
                ('task_run', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='errors', to='django_cog.TaskRun')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
