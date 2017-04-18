
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Post(models.Model):
    author = models.ForeignKey('auth.User', related_name='posts')
    blog = models.ForeignKey('Blog', related_name='blog',blank=True, null=True)
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    published_date = models.DateTimeField(blank=True, null=True)
    visited = models.PositiveIntegerField(default=0, blank=True, null=True)
    rate = models.PositiveIntegerField(default=0, blank=True, null=True)

    def plus(self):
        if self.rate < 99999:
            self.rate += 1
            self.save()

    def minus(self):
        if self.rate > 0:
            self.rate -= 1
            self.save()

    def visit(self):
        self.visited += 1
        self.save()

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title


class Blog(models.Model):
    name = models.CharField(max_length=200)
    moderators = models.ManyToManyField(User, through='Moderator', through_fields=('blog', 'user'))

    def __str__(self):
        return self.name


class Moderator(models.Model):
    blog = models.ForeignKey(Blog)
    user = models.ForeignKey(User)
    big_boss = models.ForeignKey(User, related_name="moderator_boss")
    invite_message = models.CharField(max_length=64)


class Comment(models.Model):
    author = models.ForeignKey('auth.User', related_name='comments')
    post = models.ForeignKey('blog.Post', related_name='comments')
    text = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    published_date = models.DateTimeField(blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    class Meta:
        ordering = ["-published_date"]
