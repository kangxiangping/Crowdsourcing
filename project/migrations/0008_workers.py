# Generated by Django 3.1.7 on 2021-05-22 21:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0003_auto_20210428_2222'),
        ('project', '0007_task_gold'),
    ]

    operations = [
        migrations.CreateModel(
            name='Workers',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('qw', models.FloatField(null=True)),
                ('projectId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='project.project')),
                ('worker', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='login.user')),
            ],
            options={
                'db_table': 'Workers',
            },
        ),
    ]
