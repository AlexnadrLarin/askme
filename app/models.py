from django.db import models
from django.contrib.auth.models import User


# Extending User Model Using a One-To-One Link
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(default='static/img/avatar6.png', upload_to='uploads')
    rating = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username


class Question(models.Model):
    author = models.OneToOneField(Profile, on_delete=models.PROTECT)
    title = models.CharField(max_length=255, blank=False)
    text = models.TextField(blank=False)
    rating = models.IntegerField(default=0)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Answer(models.Model):
    author = models.OneToOneField(Profile, on_delete=models.PROTECT)
    question = models.OneToOneField(Question, on_delete=models.PROTECT)
    text = models.TextField(blank=False)
    rating = models.IntegerField(default=0)
    date_created = models.DateTimeField(auto_now_add=True)
    correct = models.BooleanField(default=False)


class Tag(models.Model):
    tag = models.ManyToManyField(Question)
    tag_name = models.CharField(max_length=255, blank=False)

    def __str__(self):
        return self.tag_name


