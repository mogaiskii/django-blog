
from django.db import models
from django.utils import timezone


class Post(models.Model):
    author = models.ForeignKey('auth.User')
    title = models.CharField(max_length=200)
    text = models.TextField()
    rate = models.PositiveIntegerField(default=0, blank=True, null=True)
    created_date = models.DateTimeField(default=timezone.now())
    published_date = models.DateTimeField(blank=True, null=True)
    last_edit_date = models.DateTimeField(blank=True, null=True)
    visited = models.PositiveIntegerField(default=0, blank=True, null=True)
    def plus(self):
        if self.rate<99999:
            self.rate+=1
            self.save()

    def minus(self):
        if self.rate>0:
            self.rate-=1
            self.save()

    def visit(self):
        self.visited+=1
        self.save()

    def publish(self):
        self.published_date = timezone.now()
        self.last_edit_date = self.published_date
        self.save()

    def __str__(self):
        return self.title