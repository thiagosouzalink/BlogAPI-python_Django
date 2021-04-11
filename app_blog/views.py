from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.views.generic.base import TemplateView
from django.views.generic import (
    ListView, 
    CreateView, 
    UpdateView, 
    DeleteView, 
    DetailView
)

from .models import CustomUser, Post
from .forms import UserForm, UserEditForm, PostForm


# Página inicial
class IndexListView(ListView):

    model = Post
    template_name = 'app_blog/index.html'
    context_object_name = 'posts'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_queryset(self):
        self.object_list = Post.objects.filter(author=self.request.user).order_by('created_date')
        return self.object_list


# Página de login
class LoginTemplateView(TemplateView):

    template_name = 'app_blog/login.html'


# Formulário de cadastro do usuário
class UserCadastroCreateView(CreateView):

    template_name = 'app_blog/user_cadastro.html'
    form_class = UserForm

    def form_valid(self, form):
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('login')


# Formulário para editar usuário
class UserEditUpdateView(UpdateView):

    template_name = 'app_blog/user_edit.html'
    form_class = UserEditForm

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_object(self):
        user_id = self.kwargs.get('user_id')
        user = self.request.user
        return get_object_or_404(CustomUser, id=user_id, username=user)

    def form_valid(self, form):
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('index')


# Formulário para criar post
class PostCreateView(CreateView):

    template_name = 'app_blog/post_cadastro.html'
    form_class = PostForm

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def form_valid(self, form):
        post = form.save(commit=False)
        post.author = self.request.user
        post.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('index')


# Formulário para editar post
class PostUpdateView(UpdateView):

    template_name = 'app_blog/post_cadastro.html'
    form_class = PostForm

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_object(self):
        post_id = self.kwargs.get('post_id')
        user = self.request.user
        return get_object_or_404(Post, id=post_id, author=user)

    def form_valid(self, form):
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('index')


# Excluir post
class PostDeleteView(DeleteView):

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_object(self):
        post_id = self.kwargs.get('post_id')
        user = self.request.user
        return get_object_or_404(Post, id=post_id, author=user)

    def get_success_url(self):
        return reverse('index')


# Post em detalhes
class PostDetailView(DetailView):
    
    model = Post
    template_name = 'app_blog/post_detail.html'

    def get_object(self):
        post_id = self.kwargs.get('post_id')
        return get_object_or_404(Post, id=post_id)


# Página de perfil do usuário
def user_perfil(request, username):
    template_name = 'app_blog/user_perfil.html'
    current_user = request.user.username
    if current_user == username:
        return redirect('index')    
    else:
        wanted_user = get_object_or_404(CustomUser, username=username)
        return render(request, template_name, {'wanted_user': wanted_user})


# Submter login
def submit_login(request):
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('index')
        else:
            messages.error(request, "Login/Senha inválido! Por favor tente novamente.")
            return redirect('login')


# Página de ERRO 404
def error_404(request, exception):
    return render(request, '404.html')