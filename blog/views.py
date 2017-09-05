import json
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.http import JsonResponse
from .models import Post, Comment
from .forms import PostForm, CommentForm
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.views.generic import ListView
from django.views.generic.edit import FormView
from django.views.generic.base import ContextMixin
from django.contrib.auth.models import User

from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import CreateView
# Create your views here.
# TODO: write a todo
# TODO: make here PEP


class SideBarMixin(ContextMixin):

    def get_context_data(self, **kwargs):
        context = super(SideBarMixin, self).get_context_data(**kwargs)

        return context


class PostList(ListView):
    model = Post
    ordering = "-created_date"
    context_object_name = "posts"
    template_name = "blog/post_list.html"
    paginate_by = 7
    paginate_orphans = 3
    allow_empty = True
    page_kwarg = "pn"


@csrf_protect
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.visit()
    return render(request, 'blog/post_detail.html', {'post': post})


@login_required
def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})


@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})


@login_required
def plus(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.plus()
    data = {
        "rate": str(request.method),
    }
    return JsonResponse(data)


@login_required
def minus(request,pk):
    post = get_object_or_404(Post, pk=pk)
    post.minus()
    data = {
        "rate": str(post.rate),
    }
    return JsonResponse(data)


def best_posts(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-rate')
    return render(request, 'blog/post_list.html', {'posts': posts})


def popular(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-visited')
    return render(request, 'blog/post_list.html', {'posts': posts})

@login_required
def comment_create(request, pk):
    print("id:", request.user.id)
    print("text: {}".format( (request.body).decode('utf-8') ))
    form = CommentForm()
    comment = form.save(commit=False)
    comment.text = json.loads( request.body.decode("utf-8") )
    comment.post = Post.objects.get(pk=pk)
    comment.author = request.user
    comment.publish()
    # if form.is_valid():
    #     form.save()
    # else:
    #     return JsonResponse(form.errors ,status=400)
    data = {
        'is_recived': True,
    }
    return JsonResponse(dict(data))


class RegisterFormView(FormView):
    form_class = UserCreationForm

    # Ссылка, на которую будет перенаправляться пользователь в случае успешной регистрации.
    # В данном случае указана ссылка на страницу входа для зарегистрированных пользователей.
    success_url = "accounts/login/"

    # Шаблон, который будет использоваться при отображении представления.
    template_name = "registration/login.html"

    def form_valid(self, form):
        # Создаём пользователя, если данные в форму были введены корректно.
        form.save()

        # Вызываем метод базового класса
        return super(RegisterFormView, self).form_valid(form)