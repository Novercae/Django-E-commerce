from tabnanny import check
from django.db import models
import os
from django.conf import settings
from PIL import Image
from django.utils.text import slugify
from utils.reutilizaveis import get_format_price



class Produto(models.Model):

    nome = models.CharField(max_length=100)

    descricao_curta = models.CharField(max_length=255)

    descricao_longa = models.TextField()

    imagem = models.ImageField(
        upload_to='produto_imagens/%Y/%m/', blank=True, null=True)

    slug = models.SlugField(unique=True, blank=True, null=True)

    preco_marketing = models.FloatField(default=0)

    preco_marketing_promo = models.FloatField(blank=True, null=True)

    tipo = models.CharField(

        default='V',

        max_length=1,

        choices=(

            ('V', 'Variável'),
            ('S', 'Simples'),
        )
    )

    def get_preco_formatado(self):
        return get_format_price(self.preco_marketing)
    get_preco_formatado.short_description = 'Preço'

    def get_preco_promo_formatado(self):
        if self.preco_marketing_promo:
            return get_format_price(self.preco_marketing_promo)
        else:
            return 'Sem promoção'
    get_preco_promo_formatado.short_description = 'Preço de promomoção'

    @staticmethod
    def resize_image(img, new_width=800):
        img_full_path = os.path.join(settings.MEDIA_ROOT, img.name)
        img_pil = Image.open(img_full_path)
        original_width, original_height = img_pil.size

        if original_width <= new_width:
            img_pil.close()
            return

        new_height = round((new_width * original_height) / original_width)

        new_img = img_pil.resize((new_width, new_height), Image.LANCZOS)
        new_img.save(
            img_full_path,
            optimize=True,
            quality=50
        )

    def save(self, *args, **kwargs):
        if not self.slug:
            slug = f'{slugify(self.nome)}'
            self.slug = slug

        super().save(*args, **kwargs)

        max_image_size = 800

        if self.imagem:
            self.resize_image(self.imagem, max_image_size)


    def __str__(self):
        return self.nome


class Variacao(models.Model):
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    nome = models.CharField(max_length=50, blank=True, null=True)
    preco = models.FloatField()
    preco_promo = models.FloatField(default=None,)
    estoque = models.PositiveIntegerField(default=1)

    
    def check_preco(preco_promo, preco):
        if preco_promo is None:
            preco_promo = preco
        else:
            return
    check_preco(preco_promo, preco)
    def __str__(self):
        return self.nome or self.produto.nome

    class meta:
        verbose_name = 'Variação'
        verbose_name_plural = 'Variações'
