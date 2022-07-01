from django import forms
from django.contrib.auth.models import User
from . import models


class PerfilForm(forms.ModelForm):
    class Meta:
        model = models.Perfil
        fields = '__all__'
        exclude = ['username']


class UserForm(forms.ModelForm):
    password = forms.CharField(
        required=False,
        widget=forms.PasswordInput,
        label='Senha',
        )
    password2 = forms.CharField(
        required=False,
        widget=forms.PasswordInput,
        label='Corfimação de senha',
        )

    def __init__(self, user=None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.user = user

    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        

    def clean(self, *args, **kwargs):
        data = self.data
        cleaned = self.cleaned_data
        validation_error_msgs = {}

        # Pegando as informaçoes para checagem
        usuario_data = cleaned.get('username')
        email_data = cleaned.get('email')
        password_data = cleaned.get('password')
        password2_data = cleaned.get('password2')
        
        # pegando informaçoes no banco de dados
        usuario_db = User.objects.filter(username=usuario_data).first()
        email_db = User.objects.filter(email=email_data).first()

        # Error messages
        error_msg_usuario = 'Usuário já existe'
        error_msg_email = 'Email já existe'
        error_msg_password_short = 'Senha deve ter no mínimo 6 caracteres'
        error_msg_password_match = 'Senha não confere'
        error_required_field = 'Campo obrigatório'


        # Usuario logados: atualização
        if self.user:
            if usuario_data != self.user.username:
                if usuario_db:
                    validation_error_msgs['username'] = error_msg_usuario
            if password_data:
                if password_data != password2_data:
                    validation_error_msgs['password2'] = error_msg_password_match
                if password_data and len(password_data) < 6:
                    validation_error_msgs['password'] = error_msg_password_short
                if email_data != self.user.email:
                    if email_db:
                        validation_error_msgs['email'] = error_msg_email

        # Usuarios não logados: cadastro
        else:
            if usuario_db:
                validation_error_msgs['username'] = error_msg_usuario

            if email_db:
                validation_error_msgs['email'] = error_msg_email

            if not password_data:
                validation_error_msgs['password'] = error_required_field

            if not password2_data:
                validation_error_msgs['password2'] = error_required_field

            if password_data != password2_data:
                validation_error_msgs['password2'] = error_msg_password_match

            if password_data and len(password_data) < 6:
                validation_error_msgs['password'] = error_msg_password_short



        if validation_error_msgs:
            raise forms.ValidationError(validation_error_msgs)