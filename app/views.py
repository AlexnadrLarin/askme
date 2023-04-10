from django.shortcuts import render, redirect
from django.core.paginator import Paginator

from .models import Question, Answer, Tag, Profile


def paginate(objects_list, request, per_page=10):
    paginator = Paginator(objects_list, per_page)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return page_obj


def index(request):
    context = {'members': Profile.objects.order_by("-rating")[:5],
               'tags': Tag.objects.all()[:10],
               'page_obj': paginate(Question.objects.date_sort(), request)}
    return render(request, 'index.html', context)


def login(request):
    context = {'members': Profile.objects.order_by("-rating")[:5],
               'tags': Tag.objects.all()[:10]}
    return render(request, 'login.html', context)


def settings(request):
    context = {'members': Profile.objects.order_by("-rating")[:5],
               'tags': Tag.objects.all()[:10]}
    return render(request, 'settings.html', context)


def signup(request):
    context = {'members': Profile.objects.order_by("-rating")[:5],
               'tags': Tag.objects.all()[:10]}
    return render(request, 'signup.html', context)


def ask(request):
    context = {'members': Profile.objects.order_by("-rating")[:5],
               'tags': Tag.objects.all()[:10]}
    return render(request, 'ask.html', context)


def hot(request):
    context = {'members': Profile.objects.order_by("-rating")[:5],
               'tags': Tag.objects.all(),
               'page_obj': paginate(Question.objects.rating_sort(), request)}
    return render(request, 'hot.html', context)


def question(request, question_id):
    context = {'members': Profile.objects.order_by("-rating")[:5],
               'tags': Tag.objects.all(),
               'page_obj': paginate(Answer.objects.filter(question=question_id), request),
               'question': Question.objects.get(id=question_id)}
    return render(request, 'question.html', context)


def tag(request, tag_name):
    context = {'members': Profile.objects.order_by("-rating")[:5],
               'tags': Tag.objects.all()[:10],
               'page_obj': paginate(Question.objects.question_tag_sort(tag_name), request),
               'tag': Tag.objects.get(tag_name=tag_name)}
    return render(request, 'tag.html', context)
