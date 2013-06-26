from unittest import TestCase


class AvalonMainTest(TestCase):

    def test_main(self):
        from avalon import __version__

        self.assertTrue(__version__)

    def test_story(self):
        from avalon.core import story, Story

        @story
        def get_one():
            return 1

        self.assertTrue(isinstance(get_one, Story))
        self.assertEqual(get_one.weight, 100)
        self.assertEqual(get_one(), 1)

        @story(chance=50, weight=50)
        def maybe_two(data=None):
            return 2

        self.assertTrue(isinstance(maybe_two, Story))
        results = list(maybe_two() for _ in range(30))
        self.assertTrue(2 in results)
        self.assertTrue(None in results)

        st = get_one & maybe_two
        self.assertEqual(len(st.queue), 2)
        results = list(st() for _ in range(50))
        self.assertTrue(1 in results)
        self.assertTrue(2 in results)
        self.assertFalse(None in results)

        st = get_one | maybe_two
        self.assertEqual(len(st.queue), 2)
        results = list(st() for _ in range(50))
        self.assertTrue(1 in results)
        self.assertTrue(2 in results)
        self.assertTrue(None in results)

        @story
        def get_three(param=None):
            return 3

        st = get_one & (maybe_two | get_three)
        results = list(st() for _ in range(50))
        self.assertTrue(1 in results)
        self.assertTrue(2 in results)
        self.assertTrue(3 in results)
        self.assertFalse(None in results)

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
