# Generated by Django 3.1.7 on 2021-04-28 19:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('login', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Dataset',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False, unique=True)),
                ('coverUrl', models.CharField(max_length=100, unique=True)),
                ('gmtCreate', models.BigIntegerField()),
                ('imgCount', models.IntegerField()),
                ('isUsed', models.IntegerField()),
                ('name', models.CharField(max_length=20)),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='login.user')),
            ],
            options={
                'db_table': 'dataset',
            },
        ),
        migrations.CreateModel(
            name='Picture',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False, unique=True)),
                ('url', models.CharField(max_length=100, unique=True)),
                ('name', models.CharField(max_length=20)),
                ('datasetId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dataset.dataset')),
            ],
            options={
                'db_table': 'picture',
            },
        ),
    ]
