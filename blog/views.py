from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from .models import Post
from .forms import PostForm,CommentForm
from django.shortcuts import redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
# Create your views here.


def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'blog/post_list.html',{'posts': posts})


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
            post.last_edit_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})


@login_required
def add_comment_to_post(request,pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.publish()
            # data = {
            #     "author": str(comment.author),
            #     "published_date": str(comment.published_date),
            #     "text": str(comment.text),
            # }
            # return JsonResponse(data)
            return redirect('post_detail', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'blog/add_comment_to_post.html', {'form': form})


def plus(request,pk):
    post = get_object_or_404(Post, pk=pk)
    post.plus()
    data = {
        "rate": str(post.rate),
    }
    return JsonResponse(data)


def minus(request,pk):
    post = get_object_or_404(Post, pk=pk)
    post.minus()
    data = {
        "rate": str(post.rate),
    }
    return JsonResponse(data)


def best_posts(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('rate')
    return render(request, 'blog/post_list.html',{'posts': posts})


def popular(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('visited')
    return render(request, 'blog/post_list.html',{'posts': posts})
