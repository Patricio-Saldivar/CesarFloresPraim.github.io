# Generated by Django 2.1 on 2018-08-25 21:05

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Familia',
            fields=[
                ('usuario', models.CharField(db_column='usuario', max_length=25, primary_key=True, serialize=False)),
                ('contrasenia1', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=50)),
                ('celular', models.CharField(max_length=15)),
            ],
        ),
    ]
