# Generated by Django 3.2 on 2021-07-09 13:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rota12', '0003_parametros'),
    ]

    operations = [
        migrations.AlterField(
            model_name='parametros',
            name='Codigo',
            field=models.IntegerField(default=0),
        ),
    ]