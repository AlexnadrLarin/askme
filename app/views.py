from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.http import Http404
from django.core.exceptions import ObjectDoesNotExist
import django.contrib.auth as auth
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User


from .forms import LoginForm, CreateUserForm, ProfileForm, UpdateUserForm, QuestionForm, AnswerForm, TagForm
from .models import Question, Answer, Tag, Profile


def paginate(objects_list, request, per_page=10):
    paginator = Paginator(objects_list, per_page)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return page_obj


def username_exists(username):
    return User.objects.filter(username=username).exists()


def question_exists(title):
    return Question.objects.filter(title=title).exists()


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
        if user_form.is_valid() and user_form.changed_data != []:
            if not username_exists(user_form.cleaned_data.get('username')):
                user_form.save()
                messages.success(request, "User data changed successfully!")
            else:
                messages.error(request, "User already exists!")

        if profile_form.changed_data:
            if profile_form.is_valid():
                print(profile_form.changed_data)
                profile_form.save()
                messages.success(request, "Photo changed successfully!")
            else:
                messages.error(request, "Invalid photo format!")

        return redirect(reverse('profile_edit'))
    elif request.method == "GET":
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
        if request.method == 'POST':
            signup_form = CreateUserForm(request.POST)
            if signup_form.is_valid():
                if not username_exists(signup_form.cleaned_data.get('username')):
                    signup_form.save()
                    messages.success(request, "Account was created for " + signup_form.cleaned_data.get("username"))
                    new_user = auth.authenticate(username=signup_form.cleaned_data['username'],
                                            password=signup_form.cleaned_data['password1'],
                                            )
                    auth.login(request, new_user)
                    return redirect(reverse('root'))
                else:
                    messages.error(request, "Username is already exists!")
            else:
                messages.error(request, "It didn't save!")
        elif request.method == 'GET':
            signup_form = CreateUserForm()

        context['form'] = signup_form
        return render(request, 'signup.html', context)


@login_required(login_url="login")
def ask(request):
    if request.method == 'GET':
        question_form = QuestionForm()
        tag_form = TagForm()
    if request.method == "POST":
        question_form = QuestionForm(request.POST)
        tag_form = TagForm()
        if question_form.is_valid():
            if not question_exists(question_form.cleaned_data.get('title')):
                question = question_form.save(commit=False)
                question.author = request.user.profile
                tag_names = request.POST.get("tag_name").split(" ")

                question.save()
                messages.success(request, "Question was created!")
                return redirect("question", question_id=question.id)
            else:
                messages.error(request, "Question is already exists!")
        else:
            messages.error(request, "It didn't save!")
    context['question_form'] = question_form
    context['tag_form'] = tag_form
    return render(request, 'ask.html', context)


def hot(request):
    context['page_obj'] = paginate(Question.objects.rating_sort(), request)
    return render(request, 'hot.html', context)


def question(request, question_id):
    try:
        context['page_obj'] = paginate(Answer.objects.filter(question=question_id).order_by("-rating"), request)
        context['question'] = Question.objects.get(id=question_id)
        if request.method == 'GET':
            answer_form = AnswerForm()
        if request.method == 'POST':
            answer_form = AnswerForm(request.POST)
            if answer_form.is_valid():
                answer = answer_form.save(commit=False)
                answer.question = context['question']
                answer.author = request.user.profile
                answer.save()
                messages.success(request, "Answer was created!")
                return redirect("question", question_id=question_id)
            else:
                messages.error(request, "It didn't save!")
        context['answer_form'] = answer_form
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
