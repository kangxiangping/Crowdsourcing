# Generated by Django 3.1.7 on 2021-05-30 20:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0009_auto_20210525_1914'),
    ]

    operations = [
        migrations.AddField(
            model_name='workers',
            name='qws',
            field=models.CharField(default='', max_length=200),
        ),
    ]
