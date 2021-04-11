from django import forms

from .models import CustomUser, Post


class UserForm(forms.ModelForm):

    first_name = forms.CharField(
        label='Nome',
        error_messages={'max_length': 'Nome não pode ter mais de 30 caracteres'}, widget=forms.TextInput(attrs={'placeholder':'Nome'})
    )
    last_name = forms.CharField(
        label='Sobrenome',
        error_messages={'max_length': 'Sobrenome não pode ter mais de 150 caracteres'},
        widget=forms.TextInput(attrs={'placeholder':'Sobrenome'})
    )
    username = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Username'})
    )
    email = forms.EmailField(
        widget=forms.TextInput(attrs={'placeholder': 'E-mail'})
    )
    password = forms.CharField(
        label='Senha',
        help_text="Digite uma senha segura",
        widget=forms.PasswordInput(attrs={'placeholder':'Senha'})
    )
    password2 = forms.CharField(
        label='Confirmar senha',
        widget=forms.PasswordInput(attrs={'placeholder':'Repetir senha'})
    )
    facebook = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'https://www.facebook.com/seu_username'}), 
        required=False
    )
    instagram = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'https://www.instagram.com/seu_username'}), 
        required=False
    )
    twitter = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'https://www.twitter.com/seu_username'}), 
        required=False
    )

    class Meta:
        model = CustomUser
        fields = (
            'first_name',
            'last_name',
            'email',
            'username',
            'facebook',
            'instagram',
            'twitter'
        )

    def clean_password2(self):
        passwords = self.cleaned_data
        if passwords['password2'] != passwords['password']:
            raise forms.ValidationError('Senhas diferentes.')
        return passwords['password2']

    def save(self, commit=True):
        user = CustomUser.objects.create_user(
            username=self.cleaned_data['username'],
            email=self.cleaned_data['email'],
            password=self.cleaned_data['password'],
            first_name=self.cleaned_data['first_name'],
            last_name=self.cleaned_data['last_name'],
            facebook=self.cleaned_data['facebook'],
            instagram=self.cleaned_data['instagram'],
            twitter=self.cleaned_data['twitter']
        )
        return user


class UserEditForm(forms.ModelForm):

    class Meta:
        model = CustomUser
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'facebook',
            'instagram',
            'twitter'
        )

class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = (
            'title',
            'text'
        )
