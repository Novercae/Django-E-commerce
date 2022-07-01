import email
from django.db import models
from django.contrib.auth.models import User
import re
from utils import *
from django.forms import ValidationError

from utils.validacpf import valida_cpf


class Perfil(models.Model):
    username = models.OneToOneField(
        User, on_delete=models.CASCADE, verbose_name='Usuário')
    primeiro_nome = models.CharField(max_length=100, verbose_name='Nome')
    ultimo_nome = models.CharField(max_length=100, verbose_name='Sobrenome')
    idade = models.PositiveIntegerField(verbose_name='Idade')
    data_nacimento = models.DateField(verbose_name='Data de Nascimento')
    cpf = models.CharField(max_length=11, verbose_name='CPF')
    email = models.EmailField(verbose_name='E-mail')

    endereco = models.CharField(max_length=50, verbose_name='Endereço')
    numero = models.CharField(max_length=5, verbose_name='Número')
    complemento = models.CharField(max_length=30, verbose_name='Complemento', blank=True)
    bairro = models.CharField(max_length=30)
    cep = models.CharField(max_length=8)
    cidade = models.CharField(max_length=30)
    estado = models.CharField(
        max_length=2,
        default='AC',
        choices=(
            ('AC', 'Acre'),
            ('AL', 'Alagoas'),
            ('AP', 'Amapá'),
            ('AM', 'Amazonas'),
            ('BA', 'Bahia'),
            ('CE', 'Ceará'),
            ('DF', 'Distrito Federal'),
            ('ES', 'Espírito Santo'),
            ('GO', 'Goiás'),
            ('MA', 'Maranhão'),
            ('MT', 'Mato Grosso'),
            ('MS', 'Mato Grosso do Sul'),
            ('MG', 'Minas Gerais'),
            ('PA', 'Pará'),
            ('PB', 'Paraíba'),
            ('PR', 'Paraná'),
            ('PE', 'Pernambuco'),
            ('PI', 'Piauí'),
            ('RJ', 'Rio de Janeiro'),
            ('RN', 'Rio Grande do Norte'),
            ('RS', 'Rio Grande do Sul'),
            ('RO', 'Rondônia'),
            ('RR', 'Roraima'),
            ('SC', 'Santa Catarina'),
            ('SP', 'São Paulo'),
            ('SE', 'Sergipe'),
            ('TO', 'Tocantins'),
        )
    )

    def __str__(self):
        return self.username

    # TODO: Checar se falta algun error
    def clean(self):
        error_messages = {}

        cpf_enviado = self.cpf or None
        cpf_salvo = None
        perfil = Perfil.objects.filter(cpf=cpf_enviado).first()

        if perfil:
            cpf_salvo = perfil.cpf

            if cpf_salvo is not None and self.pk != perfil.pk:
                error_messages['cpf'] = 'CPF já cadastrado'
        
        if not valida_cpf(self.cpf):
            error_messages['cpf'] = 'CPF inválido'

        if error_messages:
            raise ValidationError(error_messages)

        if re.search(r'[^0-9]', self.cep) or len(self.cep) != 8:
            error_messages['cep'] = 'CEP inválido, digite somente os 8 digitos do CEP'

        if error_messages:
            raise ValidationError(error_messages)
    
    class Meta:
        verbose_name = 'Perfil'
        verbose_name_plural = 'Perfis'



        

