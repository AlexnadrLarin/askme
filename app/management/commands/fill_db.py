import random
import sys

from django.db import transaction
from django.core.management.base import BaseCommand
from django.db.utils import IntegrityError

sys.path.append('../app/')
from app.models import User, Profile, Question, Tag, Answer
from app.factories import (UserFactory, ProfileFactory, QuestionFactory, AnswerFactory, TagFactory)


class Command(BaseCommand):
    help = "Generates test data"

    def add_arguments(self, parser):
        parser.add_argument("ratio", type=int)

    @transaction.atomic
    def handle(self, *args, **kwargs):
        ratio = kwargs["ratio"]
        NUM_USERS = ratio
        NUM_QUESTIONS = ratio * 10
        NUM_ANSWERS = ratio * 100
        NUM_TAGS = ratio

        models = [Answer, Tag, Question, Profile, User]
        for m in models:
            m.objects.all().delete()

        profiles = []
        for _ in range(NUM_USERS):
            try:
                person = UserFactory()
                profile = ProfileFactory(user=person)
                profiles.append(profile)
            except:
                continue

        questions = []
        for _ in range(NUM_QUESTIONS):
                author = random.choice(profiles)
                question = QuestionFactory(author=author)
                questions.append(question)

                for _ in range(round(NUM_ANSWERS/NUM_QUESTIONS)):
                        author = random.choice(profiles)
                        AnswerFactory(author=author, question=question)

        for _ in range(NUM_TAGS):
            tag = TagFactory(tag=[random.choice(questions) for i in range(5)])



