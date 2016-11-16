
from django.db import models
from django.utils import timezone


class Post(models.Model):
    author = models.ForeignKey('auth.User', related_name='posts')
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now())
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


class Comment(models.Model):
    author = models.ForeignKey('auth.User', related_name='comments')
    post = models.ForeignKey('blog.Post', related_name='comments')
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now())
    published_date = models.DateTimeField(blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    class Meta:
        ordering = ["-created_date"]
