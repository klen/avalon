from unittest import TestCase
from .django_app.models import *  # noqa
from django.core.management import call_command


class AvalonDjangoTest(TestCase):

    @classmethod
    def setUpClass(cls):
        call_command('syncdb', interactive=False)

    @classmethod
    def tearDownClass(cls):
        call_command('flush', interactive=False)

    def test_actor(self):
        from avalon.core import Actor
        from django.contrib.auth.models import User

        user = Actor(User)
        self.assertTrue(user)
        self.assertTrue(user.pk)
        self.assertTrue(user.username)

    def test_action(self):
        from avalon.core import story, Actor
        from django.contrib.auth.models import User

        @story
        def create():
            return Actor(User, is_active=False)

        @story(chance=70)
        def verified(user):
            user.is_active = True
            user.save()
            return user

        @story(chance=30)
        def rejected(user):
            user.is_active = False
            user.save()
            return user

        st = create & (verified | rejected)

        statuses = []
        for _ in range(20):
            user = st()
            statuses.append(user.is_active)
        self.assertTrue(True in statuses)
        self.assertTrue(False in statuses)
