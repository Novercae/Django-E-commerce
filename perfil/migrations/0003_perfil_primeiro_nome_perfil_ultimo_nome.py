# Generated by Django 4.0.4 on 2022-05-05 19:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('perfil', '0002_remove_perfil_nome_endereco'),
    ]

    operations = [
        migrations.AddField(
            model_name='perfil',
            name='primeiro_nome',
            field=models.CharField(default=None, max_length=100, verbose_name='Nome'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='perfil',
            name='ultimo_nome',
            field=models.CharField(default=None, max_length=100, verbose_name='Sobrenome'),
            preserve_default=False,
        ),
    ]