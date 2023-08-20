from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
from django.urls import reverse


class Author(models.Model):
    author_user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating_author = models.IntegerField(default=0)

    def update_rating(self):
        post_rating = self.post_set.all().aggregate(sum=Sum('rating'))['sum']
        user_rating = self.author_user.comment_set.all().aggregate(sum=Sum('rating'))['sum']
        comment_rating = Comment.objects.filter(post__author=self).aggregate(sum=Sum('rating'))['sum']
        self.rating_author = post_rating * 3 + user_rating + comment_rating
        self.save()


class Category(models.Model):
    category_name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.category_name


class Post(models.Model):
    article = 'a'
    news = 'n'
    TYPES = [(article, 'Статья'),
             (news, 'Новость')]

    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    title = models.CharField(max_length=255)
    content = models.TextField()
    type = models.CharField(max_length=1, choices=TYPES, default=news)
    rating = models.IntegerField(default=0)

    category = models.ManyToManyField(Category, through='PostCategory')

    def preview(self):
        return self.content[:124] + '...'

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def get_absolute_url(self):
        return reverse('news', kwargs={'pk': self.pk})


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(max_length=3000)
    date = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()
