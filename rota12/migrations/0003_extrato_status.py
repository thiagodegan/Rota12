# Generated by Django 3.2 on 2021-07-24 17:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rota12', '0002_auto_20210724_1422'),
    ]

    operations = [
        migrations.AddField(
            model_name='extrato',
            name='Status',
            field=models.CharField(choices=[('P', 'Pendente'), ('A', 'Aprovado'), ('R', 'Recusado')], default='P', max_length=1),
        ),
    ]
