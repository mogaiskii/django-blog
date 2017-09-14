import json
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.http import JsonResponse
from .models import Post, Comment, Blog
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

# TODO: make here PEP
# TODO: CBV only?


# /
# /page/:pn
class PostList(ListView):
    model = Post
    ordering = "-created_date"
    context_object_name = "posts"
    template_name = "blog/post_list.html"
    paginate_by = 7
    paginate_orphans = 3
    allow_empty = True
    page_kwarg = "pn"


# /post/:pk
# @csrf_protect  # useless?
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.visit()
    return render(request, 'blog/post_detail.html', {'post': post})


# /post/new  #(pk=None => new Post)
# /post/:pk/edit
@login_required
def post_edit(request, pk=None):
    if pk:
        post = get_object_or_404(Post, pk=pk)
    else:
        post = None
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else: # GET:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})



# /post/plus/:pk
# /post/minus/:pk
@login_required
def rate(request,pk,change):
    post = get_object_or_404(Post, pk=pk)
    if change == 'plus':
        post.plus()
    elif change == 'minus':
        post.minus()
    data = {
        "rate": str(post.rate),
    }
    return JsonResponse(data)


# /post/best
def best_posts(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-rate')
    return render(request, 'blog/post_list.html', {'posts': posts})


# /post/popular
def popular(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-visited')
    return render(request, 'blog/post_list.html', {'posts': posts})


# /post/:pk/comment
@login_required
def comment_create(request, pk):
    form = CommentForm()
    comment = form.save(commit=False)
    comment.text = json.loads( request.body.decode("utf-8") )
    comment.post = Post.objects.get(pk=pk)
    comment.author = request.user
    comment.publish()
    data = {
        'is_recived': True,
    }
    return JsonResponse(dict(data))



def blog_detail(request,pk):
    blog = get_object_or_404(Blog,pk=pk)
    data = {}
    data['blog'] = blog
    data['posts'] = Post.objects.filter(blog=blog).order_by('-created_date')
    return render(request, 'blog/blog_posts.html', data)


# /accounts/register
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