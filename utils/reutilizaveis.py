def get_format_price(value):
    return f'R$ {value:,.2f}'

def cart_total_qtd(cart):
    return sum(item['quantidade'] for item in cart.values())

def cart_total_price(cart):
    total = 0
    for item in cart.values():
        if item['preco_quantitativo_promo'] or not item['preco_quantitativo_promo'] == 0:
            total += item['preco_quantitativo_promo']
        else:
            total += item['preco_quantitativo']
    return total