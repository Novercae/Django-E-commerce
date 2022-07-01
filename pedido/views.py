from multiprocessing import context
from django.shortcuts import redirect
from django.views.generic import ListView, DetailView
from django.views import View
from django.http import HttpResponse
from django.contrib import messages
from produto.models import Variacao
from .models import Pedido, ItemPedido
from django.urls import reverse

from utils import reutilizaveis


class DispatchLoginRequiredMixin(View):
    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return redirect('perfil:criar')

        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(user=self.request.user)


class Pagar(DispatchLoginRequiredMixin, DetailView):
    template_name = 'pedido/pagar.html'
    model = Pedido
    pk_url_kwarg = 'pk'
    context_object_name = 'pedido'

    # Não deixa ver pedidos de outros usuários
    


class SalvarPedido(View):
    template_name = 'pedido/pagar.html'

    def get(self, *args, **kwargs):
        cart = self.request.session.get('cart')
        if not self.request.user.is_authenticated:
            messages.error(self.request, 'Precisa Fazer Login.')
            return redirect('perfil:criar')

        if not cart:
            messages.error(self.request, 'Não há nenhum produto no carrinho.')
            return redirect('pedido:listar')

        cart_variation_ids = [v for v in cart]
        bd_variations = list(Variacao.objects.select_related(
            'produto').filter(id__in=cart_variation_ids))

        for variacao in bd_variations:
            vid = str(variacao.id)

            estoque = variacao.estoque
            qtd_cart = cart[vid]['quantidade']
            preco_unt = cart[vid]['preco_unitario']
            preco_unt_promo = cart[vid]['preco_unitario_promo']

            error_msg_estoque = ''

            if qtd_cart > estoque:
                cart[vid]['quantidade'] = estoque
                cart[vid]['preco_quantitatico'] = estoque * preco_unt
                cart[vid]['preco_quantitatico_promo'] = estoque * preco_unt_promo

                error_msg_estoque = 'Estoque insuficiente para alguns produtos do seu carrinho. '\
                    'Reduzimos a quantidade dessses produtos para o estoque mínimo. '\
                    'Por favor, verifique seu carrinho.'

            if error_msg_estoque:
                messages.error(self.request, error_msg_estoque)
                self.requesrt.session.save()
                return redirect('produto:cart')

        qtd_total_cart = reutilizaveis.cart_total_qtd(cart)
        total_cart = reutilizaveis.cart_total_price(cart)

        pedido = Pedido(
            user=self.request.user,
            total=total_cart,
            qtd_total=qtd_total_cart,
            status='C'
        )
        pedido.save()

        ItemPedido.objects.bulk_create([
            ItemPedido(
                pedido=pedido,
                produto=v['produto_nome'],
                produto_id=v['produto_id'],
                variacao=v['variacao_nome'],
                variacao_id=v['variacao_id'],
                preco=v['preco_quantitativo'],
                preco_promocional=v['preco_quantitativo_promo'],
                quantidade=v['quantidade'],
                imagem=v['imagem'],
            ) for v in cart.values()
        ])

        contexto = {}

        # apagando o Carrinho
        del self.request.session['cart']

        return redirect(
            reverse(
                'pedido:pagar',
                kwargs={
                    'pk': pedido.id
                }
            )
        )


class Detalhe(DispatchLoginRequiredMixin, DetailView):
    model = Pedido
    template_name = 'pedido/detalhe.html'
    pk_url_kwarg = 'pk'
    context_object_name = 'pedido'


class Lista(DispatchLoginRequiredMixin, ListView):
    model = Pedido
    context_object_name = 'pedidos'
    template_name = 'pedido/lista.html'
    paginate_by = 10
    ordering = ['-id']

    
