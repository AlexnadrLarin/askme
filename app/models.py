from django.db import models
import random

# Create your models here.
TAG_NAMES = [
    {
        'tag_name': i,
        'color': ['black', 'red', 'green']
    } for i in ['perl', 'Python', 'TechnoPark', 'MySQL', 'django', 'Mail.ru', 'Voloshin', 'Firefox', 'C++']
]

MEMBERS = [
    {
        'member_name': i,
    } for i in ['Mr. Freeman', 'Dr. House', 'Bender', 'Queen Victoria', 'V. Pupkin']
]

QUESTIONS = [
    {
        'id': i,
        'title': f'Question {i}',
        'text': f'Text {i}',
        'tags': [random.choice(TAG_NAMES), random.choice(TAG_NAMES)],
    } for i in range(100)
]

ANSWERS = [
    {
        'text': f'Text {i}',
    } for i in range(40)
]

