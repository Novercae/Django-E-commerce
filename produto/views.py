from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views import View
from .models import Produto, Variacao
from django.shortcuts import redirect, get_object_or_404, render
from django.contrib import messages
from perfil.models import Perfil
from django.db.models import Q


class ListaProduto(ListView):
    model = Produto
    template_name = 'produto/lista.html'
    context_object_name = 'produtos'
    paginate_by = 6
    ordering = ['-id']


class Busca(ListaProduto):
    def get_queryset(self, *args, **kwargs):
        termo = self.request.GET.get('termo') or self.request.session['termo']
        qs = super().get_queryset(*args, **kwargs)

        if not termo:
            return qs

        self.request.session['termo'] = termo

        qs = qs.filter(
            Q(nome__icontains=termo) |
            Q(descricao_longa__icontains=termo) |
            Q(descricao_curta__icontains=termo)
        )

        self.request.session.save()
        return qs


class DetalheProduto(DetailView):
    model = Produto
    template_name = 'produto/detalhe.html'
    context_object_name = 'produto'
    slug_url_kwarg = 'slug'


class AddtoCart(View):
    def get(self, *args, **kwargs):
        http_referer = self.request.META.get('HTTP_REFERER')
        variacao_id = self.request.GET.get('vid')

        if not variacao_id:
            messages.error(self.request, 'Produto Inexistente')
            return redirect(http_referer)

        variacao = get_object_or_404(Variacao, pk=variacao_id)
        variacao_estoque = variacao.estoque
        produto = variacao.produto

        produto_id = produto.id
        produto_nome = produto.nome
        variacao_nome = variacao.nome or ''
        preco_unitario = variacao.preco
        preco_unitario_promo = variacao.preco_promo
        quantidade = 1
        slug = produto.slug
        imagem = produto.imagem

        if imagem:
            imagem = imagem.url
        else:
            imagem = ''

        if variacao.estoque < 1:
            messages.error(self.request, 'Produto sem estoque')
            return redirect(http_referer)

        if not self.request.session.get('cart'):
            self.request.session['cart'] = {}
            self.request.session.save()

        cart = self.request.session['cart']

        if variacao_id in cart:
            quantidade_carrinho = cart[variacao_id]['quantidade']
            quantidade_carrinho += 1

            if quantidade_carrinho > variacao_estoque:
                messages.warning(self.request,
                                 f'Produto com apenas {variacao_estoque} unidades em estoque, '
                                 f'{variacao_estoque} adcionado ao carrinho')
                quantidade_carrinho = variacao_estoque

            cart[variacao_id]['quantidade'] = quantidade_carrinho
            cart[variacao_id]['preco_quantitativo'] = float(
                preco_unitario) * quantidade_carrinho
            cart[variacao_id]['preco_quantitativo_promo'] = float(
                preco_unitario_promo) * quantidade_carrinho
            self.request.session.save()
            messages.success(
                self.request, f'{produto_nome} {variacao_nome} adicionado ao carrinho')
            return redirect(http_referer)

        else:
            cart[variacao_id] = {
                'produto_id': produto_id,
                'produto_nome': produto_nome,
                'variacao_nome': variacao_nome,
                'variacao_id': variacao_id,
                'preco_unitario': float(preco_unitario),
                'preco_unitario_promo': float(preco_unitario_promo),
                'preco_quantitativo': float(preco_unitario),
                'preco_quantitativo_promo': float(preco_unitario_promo),
                'quantidade': quantidade,
                'slug': slug,
                'imagem': imagem
            }
            self.request.session.save()
            messages.success(
                self.request, f'{produto_nome} {variacao_nome} adicionado ao carrinho')

        return redirect(http_referer)


class RemovefromCart(View):
    def get(self, *args, **kwargs):
        http_referer = self.request.META.get('HTTP_REFERER')
        variacao_id = self.request.GET.get('vid')

        if not variacao_id:
            return redirect(http_referer)

        if not self.request.session.get('cart'):
            return redirect(http_referer)

        if variacao_id not in self.request.session['cart']:
            return redirect(http_referer)

        cart = self.request.session['cart'][variacao_id]

        messages.success(
            self.request, f'{cart["produto_nome"]} {cart["variacao_nome"]} removido do carrinho')

        del self.request.session['cart'][variacao_id]
        self.request.session.save()
        return redirect(http_referer)


class Cart(View):
    def get(self, *args, **kwargs):
        contexto = {
            'cart': self.request.session.get('cart', {})
        }

        return render(self.request, 'produto/cart.html', contexto)


class ResumodaCompra(View):
    def get(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return redirect('perfil:criar')

        perfil = Perfil.objects.filter(username=self.request.user).exists()

        if not perfil:
            messages.error(self.request, 'Usuário sem perfil!')
            return redirect('perfil:criar')

        if not self.request.session.get('cart'):
            messages.error(self.request, 'Carrinho vazio!')
            return redirect('produto:lista')

        contexto = {
            'usuario': self.request.user,
            'cart': self.request.session['cart']
        }
        return render(self.request, 'produto/resumodacompra.html', contexto)
