from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.http import Http404
from django.core.exceptions import ObjectDoesNotExist

from .models import Question, Answer, Tag, Profile


def paginate(objects_list, request, per_page=10):
    paginator = Paginator(objects_list, per_page)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return page_obj


context = {'members': Profile.objects.profile_sort(),
           'tags': Tag.objects.all()[:10]}


def index(request):
    context['page_obj'] = paginate(Question.objects.date_sort(), request)
    return render(request, 'index.html', context)


def login(request):
    return render(request, 'login.html', context)


def settings(request):
    return render(request, 'settings.html', context)


def signup(request):
    return render(request, 'signup.html', context)


def ask(request):
    return render(request, 'ask.html', context)


def hot(request):
    context['page_obj'] = paginate(Question.objects.rating_sort(), request)
    return render(request, 'hot.html', context)


def question(request, question_id):
    try:
        context['page_obj'] = paginate(Answer.objects.filter(question=question_id), request)
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
