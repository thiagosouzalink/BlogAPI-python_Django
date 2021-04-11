from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.urls import reverse


# Criar usuários
class UserManager(BaseUserManager):

    use_in_migrations = True

    def _create_user(self, username, email, password, **extra_fields):
        if not username:
            raise ValueError("O nome de usuário é obrigatório.")
        if not email:
            raise ValueError("O E-mail é obrigatório.")
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(username, email, password, **extra_fields)

    def create_superuser(self, username, email, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser precisa ter is_superuser=True')
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser precisa ter is_staff=True')

        return self._create_user(username, email, password, **extra_fields)


# Model usuário
class CustomUser(AbstractUser):

    email = models.EmailField('E-mail', unique=True)
    first_name = models.CharField('Nome', max_length=30)
    last_name = models.CharField('Sobrenome', max_length=150)
    facebook = models.CharField('Facebook', max_length=100, blank=True)
    instagram = models.CharField('Instagram', max_length=100, blank=True)
    twitter = models.CharField('Twitter', max_length=100, blank=True)
    is_staff = models.BooleanField('Membro da Equipe', default=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name']

    class Meta:
        verbose_name = 'Usuário'
        verbose_name_plural = 'Usuários'

    def __str__(self):
        return self.username

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    def get_profile_url(self):
        return reverse('user_edit', kwargs={'username': self.username, 'user_id': self.id})

    objects = UserManager()


# Model post
class Post(models.Model):

    author = models.ForeignKey(CustomUser, verbose_name='Autor', related_name='posts', on_delete=models.CASCADE)
    title = models.CharField('Título', max_length=255)
    text = models.TextField('Texto')
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.title} - {self.author}'

    def get_detail_url(self):
        return reverse('post_detail', kwargs={'username': self.author, 'post_id': self.id})

    def get_update_url(self):
        return reverse('post_update', kwargs={'username': self.author, 'post_id': self.id})

    def get_delete_url(self):
        return reverse('post_delete', kwargs={'username': self.author, 'post_id': self.id})