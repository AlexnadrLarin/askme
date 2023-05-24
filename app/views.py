from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.http import Http404
from django.core.exceptions import ObjectDoesNotExist
import django.contrib.auth as auth
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User

from .forms import LoginForm, CreateUserForm
from .models import Question, Answer, Tag, Profile


def paginate(objects_list, request, per_page=10):
    paginator = Paginator(objects_list, per_page)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return page_obj


def username_exists(username):
    return User.objects.filter(username=username).exists()


context = {'members': Profile.objects.profile_sort(),
           'tags': Tag.objects.all()[:9]}


def logout(request):
    auth.logout(request)
    messages.info(request, "Log out successfully!")
    return redirect(reverse('root'))


def index(request):
    context['page_obj'] = paginate(Question.objects.date_sort(), request)
    return render(request, 'index.html', context)


def login(request):
    if request.user.is_authenticated:
        messages.info(request, "Already log in!")
        return redirect(reverse('root'))
    else:
        if request.method == 'GET':
            login_form = LoginForm()
        elif request.method == 'POST':
            login_form = LoginForm(request.POST)
            if login_form.is_valid():
                user = auth.authenticate(request=request, **login_form.cleaned_data)
                if user:
                    auth.login(request, user)
                    messages.success(request, "Log in successfully!")
                    return redirect(reverse('root'))
                login_form.add_error(None, "Invalid username or password!")
        context['form'] = login_form
        return render(request, "login.html", context)



@login_required(login_url="login")
def profile_edit(request):
    if request.method == "POST":
        user_form = UpdateUserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if user_form.is_valid():
            if not username_exists(user_form.cleaned_data.get('username')):
                user_form.save()
            else:
                messages.error(request, "Username is already exists!")
        if profile_form.is_valid():
            profile_form.save()
        return redirect(reverse('profile_edit'))
    else:
        user_form = UpdateUserForm(instance=request.user)
        profile_form = ProfileForm(request.FILES, instance=request.user.profile)
    context['user_form'] = user_form
    context['profile_form'] = profile_form
    return render(request, 'profile_edit.html', context)


def signup(request):
    if request.user.is_authenticated:
        messages.info(request, "Already registered!" )
        return redirect(reverse('root'))
    else:
        signup_form = CreateUserForm(request.POST)
        if request.method == 'POST':
            if signup_form.is_valid():
                if not username_exists(signup_form.cleaned_data.get('username')):
                    signup_form.save()
                    messages.success(request, "Account was created for " + signup_form.cleaned_data.get("username"))
                    return redirect(reverse('root'))
                else:
                    messages.error(request, "Username is already exists!")
            else:
                messages.error(request, "It didn't save!")
        context['form'] = signup_form
        return render(request, 'signup.html', context)


@login_required(login_url="login")
def ask(request):
    return render(request, 'ask.html', context)


def hot(request):
    context['page_obj'] = paginate(Question.objects.rating_sort(), request)
    return render(request, 'hot.html', context)


def question(request, question_id):
    try:
        context['page_obj'] = paginate(Answer.objects.filter(question=question_id).order_by("-rating"), request)
        context['question'] = Question.objects.get(id=question_id)
        return render(request, 'question.html', context)
    except ObjectDoesNotExist:
        raise Http404


def tag(request, tag_name):
    try:
        context['page_obj'] = paginate(Question.objects.question_tag_sort(tag_name), request)
        context['tag'] = Tag.objects.get(tag_name=tag_name)
        return render(request, 'tag.html', context)
    except ObjectDoesNotExist:
        raise Http404
