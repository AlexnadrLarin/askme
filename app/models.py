from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist


class ProfileManager(models.Manager):

    def profile_sort(self):
        return self.order_by("-rating")[:5]


# Extending User Model Using a One-To-One Link
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(default='static/img/avatar6.png', upload_to='uploads')
    rating = models.IntegerField(default=0)

    objects = ProfileManager()

    def __str__(self):
        return self.user.username


class QuestionManager(models.Manager):
    def date_sort(self):
        return self.order_by('-date_created')

    def rating_sort(self):
        return self.order_by('-rating')

    def question_tag_sort(self, tag_name):
        question_list = []
        for question in self.all():
            try:
                if question.tag_set.get(tag_name=tag_name):
                    question_list.append(question)
            except ObjectDoesNotExist:
                continue
        return question_list


class Question(models.Model):
    author = models.ForeignKey(Profile, on_delete=models.PROTECT)
    title = models.CharField(max_length=255, blank=False)
    text = models.TextField(blank=False)
    rating = models.IntegerField(default=0)
    date_created = models.DateTimeField(auto_now_add=True)

    objects = QuestionManager()

    def __str__(self):
        return self.title


class Answer(models.Model):
    author = models.ForeignKey(Profile, on_delete=models.PROTECT)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    text = models.TextField(blank=False)
    rating = models.IntegerField(default=0)
    date_created = models.DateTimeField(auto_now_add=True)
    correct = models.BooleanField(default=False)


class Tag(models.Model):
    tag = models.ManyToManyField(Question)
    tag_name = models.CharField(max_length=255, blank=False)

    def __str__(self):
        return self.tag_name


