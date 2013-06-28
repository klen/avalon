from unittest import TestCase
from tornado.testing import AsyncTestCase


class AvalonMainTest(TestCase):

    def test_main(self):
        from avalon import __version__

        self.assertTrue(__version__)

    def test_story(self):
        from avalon import story
        from avalon.core import Story

        @story
        def get_one():
            return 1

        self.assertTrue(isinstance(get_one, Story))
        self.assertEqual(get_one.weight, 100)
        self.assertEqual(get_one.timeout, 10)
        self.assertEqual(get_one(), 1)

        @story(chance=50, weight=50, timeout=.2)
        def maybe_two(data=None):
            return 2

        self.assertTrue(isinstance(maybe_two, Story))
        self.assertEqual(maybe_two.timeout, .2)
        results = list(maybe_two() for _ in range(30))
        self.assertTrue(2 in results)
        self.assertTrue(None in results)

        st = get_one & maybe_two
        self.assertEqual(len(st.queue), 2)
        results = list(st() for _ in range(60))
        self.assertTrue(1 in results)
        self.assertTrue(2 in results)
        self.assertFalse(None in results)

        st = get_one | maybe_two
        self.assertEqual(len(st.queue), 2)
        results = list(st() for _ in range(60))
        self.assertTrue(1 in results)
        self.assertTrue(2 in results)
        self.assertTrue(None in results)

        @story
        def get_three(param=None):
            return 3

        st = get_one & (maybe_two | get_three)
        results = list(st() for _ in range(60))
        self.assertTrue(1 in results)
        self.assertTrue(2 in results)
        self.assertTrue(3 in results)
        self.assertFalse(None in results)

        g = iter(st)
        actions = list(g)
        self.assertEqual(len(actions), 2)

    def test_guard(self):
        import random
        from avalon.core import story

        def guard(param=None):
            return random.choice((True, False))

        @story(guard=guard)
        def get_one():
            return 1

        results = list(get_one() for _ in range(30))
        self.assertTrue(None in results)


class AvalonTest(AsyncTestCase):

    def test_avalon(self):

        from avalon.engine import Avalon
        from avalon import story

        av = Avalon(self.io_loop)

        @story(timeout=.5)
        def stop():
            self.stop()

        av.make_story(stop)

        self.wait()
        self.wait()

    def test_stories(self):
        from .stories import test_story
        from avalon.engine import Avalon

        av = Avalon(self.io_loop)
        av.make_story(test_story)
