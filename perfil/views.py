from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
import copy

from django.http import HttpResponse

from . import forms, models


class BasePerfilView(View):
    template_name = 'perfil/criar.html'

    def setup(self, *args, **kwargs):
        super().setup(*args, **kwargs)

        self.cart = copy.deepcopy(self.request.session.get('cart', {}))

        self.perfil = None

        if self.request.user.is_authenticated:
            self.perfil = models.Perfil.objects.filter(
                username=self.request.user).first()

            self.contexto = {
                'userform': forms.UserForm(
                    data=self.request.POST or None,
                    user=self.request.user,
                    instance=self.request.user,
                ),
                'perfilform': forms.PerfilForm(
                    data=self.request.POST or None,
                    instance=self.perfil,
                ),
            }

        else:
            self.contexto = {
                'userform': forms.UserForm(
                    data=self.request.POST or None,
                ),
                'perfilform': forms.PerfilForm(
                    data=self.request.POST or None,),
            }

        self.userform = self.contexto['userform']
        self.perfilform = self.contexto['perfilform']

        if self.request.user.is_authenticated:
            self.template_name = 'perfil/atualizar.html'

        self.renderizar = render(
            self.request, self.template_name, self.contexto)

    def get(self, request, *args, **kwargs):
        return self.renderizar


class Criar(BasePerfilView):
    def post(self, *args, **kwargs):
        if not self.userform.is_valid() or not self.perfilform.is_valid():
            messages.error(
                self.request, 'Existe(m) erro(s) no formulário,  verifique os campos abaixos.')
            return self.renderizar

        primeiro_nome = self.perfilform.cleaned_data['primeiro_nome']
        ultimo_nome = self.perfilform.cleaned_data['ultimo_nome']
        username = self.userform.cleaned_data['username']
        password = self.userform.cleaned_data['password']
        email = self.userform.cleaned_data['email']

        # User Logado
        if self.request.user.is_authenticated:
            usuario = get_object_or_404(
                User, username=self.request.user.username)

            if password:
                usuario.set_password(password)

            usuario.primeiro_nome = primeiro_nome
            usuario.ultimo_nome = ultimo_nome
            usuario.email = email
            usuario.save()

            if not self.perfil:
                self.perfilform.cleaned_data['username'] = usuario
                perfil = models.Perfil(**self.perfilform.cleaned_data)
                perfil.save()
            else:
                self.perfilform.save(commit=False)
                perfil.usuario = usuario
                perfil.save()

        # User não logado
        else:
            usuario = self.userform.save(commit=False)
            usuario.set_password(password)
            usuario.save()

            perfil = self.perfilform.save(commit=False)
            perfil.usuario = usuario
            perfil.save()

        if password:
            autentica = authenticate(
                self.request, username=username, password=password)
            if autentica:
                login(self.request, user=usuario)

        self.request.session['cart'] = self.cart
        self.request.session.save()

        messages.success(self.request, 'Perfil criado com sucesso!')

        return redirect('perfil:cart')


class Atualizar(View):
    def get(self, *args, **kwargs):
        return HttpResponse('Atualizar')


class Login(View):
    def post(self, *args, **kwargs):
        username = self.request.POST.get('username')
        password = self.request.POST.get('password')

        if not username or not password:
            messages.error(self.request, 'Usuário ou senha inválidos!')
            return redirect('perfil:criar')

        autentica = authenticate(
            self.request, username=username, password=password)

        if autentica:
            login(self.request, user=autentica)
            messages.success(self.request, 'Login realizado com sucesso!')
            return redirect('produto:cart')

        else:
            messages.error(self.request, 'Usuário ou senha inválidos!')
            return redirect('perfil:criar')


class Logout(View):
    def get(self, *args, **kwargs):
        cart = copy.deepcopy(self.request.session.get('cart'))

        logout(self.request)

        self.request.session['cart'] = cart
        self.request.session.save()

        return redirect('produto:lista')
