from django import forms
from .models import Profile, Question, Tag, Answer
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["avatar"]
        exclude = ["user"]


class UpdateUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['title', 'text']


class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['text']


class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ['tag_name']