import random

from django.shortcuts import render, redirect
from django.core.paginator import Paginator



def paginate(objects_list, request, per_page=10):
    paginator = Paginator(objects_list, per_page)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return page_obj


def index(request):
    context = {'answers': ANSWERS, 'members': MEMBERS, 'tags': TAG_NAMES, 'page_obj': paginate(QUESTIONS, request)}
    return render(request, 'index.html', context)


def login(request):
    context = {'members': MEMBERS, 'tags': TAG_NAMES}
    return render(request, 'login.html', context)


def settings(request):
    context = {'members': MEMBERS, 'tags': TAG_NAMES}
    return render(request, 'settings.html', context)


def signup(request):
    context = {'members': MEMBERS, 'tags': TAG_NAMES}
    return render(request, 'signup.html', context)


def ask(request):
    context = {'members': MEMBERS, 'tags': TAG_NAMES}
    return render(request, 'ask.html', context)


def hot(request):
    hot_questions = [random.choice(QUESTIONS) for i in range(20)]
    context = {'answers': ANSWERS, 'members': MEMBERS, 'tags': TAG_NAMES, 'page_obj': paginate(hot_questions, request)}
    return render(request, 'hot.html', context)


def question(request, question_id):
    if question_id < len(QUESTIONS):
        context = {'members': MEMBERS, 'tags': TAG_NAMES, 'page_obj': paginate(ANSWERS, request), 'question': QUESTIONS[question_id]}
        return render(request, 'question.html', context)

    return redirect("root")


def tag(request, tag_name):
    for i in range(len(TAG_NAMES)):
        if TAG_NAMES[i]['tag_name'] == tag_name:
            question_array = []
            for QUESTION in QUESTIONS:
                for TAG in QUESTION['tags']:
                    if TAG['tag_name'] == tag_name:
                        question_array.append(QUESTION)

            context = {'answers': ANSWERS, 'members': MEMBERS, 'tags': TAG_NAMES, 'page_obj': paginate(question_array, request), 'tag_name': TAG_NAMES[i]['tag_name']}
            return render(request, 'tag.html', context)

    return redirect("root")
