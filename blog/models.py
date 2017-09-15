
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
            self.author.profile.score +=1
            self.author.save()

    def minus(self):
        if self.rate > 0:
            self.rate -= 1
            self.save()
            self.author.profile.score -=1
            self.author.save()

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
    description = models.TextField()

    def __str__(self):
        return self.name


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
        ordering = ["published_date"]  # TODO: Think about it! (mb not '-')


class Profile(models.Model):
    user = models.OneToOneField('auth.User',on_delete=models.CASCADE)
    name = models.CharField(max_length=200,blank=True)
    likes = models.ManyToManyField(Post, related_name="liker")
    dislikes = models.ManyToManyField(Post, related_name="disliker")
    score = models.IntegerField(default=20)

    def like(self, post):  # return True if added to likes
        if post in self.dislikes.all():
            self.dislikes.remove(post)
            post.plus()
            return False
        elif not post in self.likes.all():
            self.likes.add(post)
            post.plus()
            return True

    def dislike(self, post):
        if post in self.likes.all():
            self.likes.remove(post)
            post.minus()
            return False
        elif not post in self.dislikes.all():
            self.dislikes.add(post)
            post.minus() 
            return True   

    def __str__(self):
        return str(self.user.pk)+": "+self.name

        

from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender = User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance,name=instance.username)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()