# Generated by Django 3.1.7 on 2021-04-29 17:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0004_auto_20210429_1705'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='taskCount',
            field=models.IntegerField(null=True),
        ),
    ]
