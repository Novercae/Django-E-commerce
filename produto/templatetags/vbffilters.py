from django.template import Library
from utils import reutilizaveis

register = Library()

@register.filter
def format_price(value):
    return reutilizaveis.get_format_price(value)

@register.filter
def cart_total_qtd(value):
    return reutilizaveis.cart_total_qtd(value)

@register.filter
def cart_total_price(value):
    return reutilizaveis.cart_total_price(value)
