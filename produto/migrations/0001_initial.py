# Generated by Django 4.0.4 on 2022-04-28 18:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Produto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=100)),
                ('descricao_curta', models.CharField(max_length=255)),
                ('descricao_longa', models.TextField()),
                ('imagem', models.ImageField(blank=True, null=True, upload_to='produto_imagens/%Y/%m/')),
                ('slug', models.SlugField(blank=True, null=True, unique=True)),
                ('preco_marketing', models.FloatField(default=0)),
                ('preco_marketing_promo', models.FloatField(blank=True, null=True)),
                ('tipo', models.CharField(choices=[('V', 'Variável'), ('S', 'Simples')], default='V', max_length=1)),
            ],
        ),
        migrations.CreateModel(
            name='Variacao',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(blank=True, max_length=50, null=True)),
                ('preco', models.FloatField()),
                ('preco_promo', models.FloatField(default=None)),
                ('estoque', models.PositiveIntegerField(default=1)),
                ('produto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='produto.produto')),
            ],
        ),
    ]