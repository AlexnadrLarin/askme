import random
import factory
from factory.django import DjangoModelFactory

from .models import User, Profile, Question, Tag, Answer


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Faker("user_name")
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    password = factory.Faker("password")
    email = factory.Faker("email")


class ProfileFactory(DjangoModelFactory):
    class Meta:
        model = Profile

    user = factory.SubFactory(UserFactory)
    rating = factory.Faker("pyint")


class QuestionFactory(DjangoModelFactory):
    class Meta:
        model = Question

    author = factory.SubFactory(ProfileFactory)
    title = factory.Faker("sentence", nb_words=3, variable_nb_words=True)
    text = factory.Faker("sentence", nb_words=5, variable_nb_words=True)
    rating = factory.Faker("pyint")


class AnswerFactory(DjangoModelFactory):
    class Meta:
        model = Answer

    author = factory.SubFactory(ProfileFactory)
    question = factory.SubFactory(QuestionFactory)
    text = factory.Faker("sentence", nb_words=8, variable_nb_words=True)
    rating = factory.Faker("pyint")


class TagFactory(DjangoModelFactory):
    class Meta:
        model = Tag

    tag_name = factory.Faker("word")

    @factory.post_generation
    def tag(self, create, extracted, **kwargs):
        if not create:
            # Simple build, do nothing.
            return

        if extracted:
            # A list of groups were passed in, use them
            for tag_ in extracted:
                self.tag.add(tag_)



