""" Core Avalon classes. """
from mixer.auto import mixer
import random
from operator import and_, or_


def story(action=None, **kwargs):
    """ Use Story as decorator.

    :return Story:

    """

    if action:
        return Story([action], **kwargs)

    def wrapper(action):
        return story(action, **kwargs)

    return wrapper


class Story(object):

    """ Store action's queue. """

    guard = staticmethod(lambda x: True)

    def __init__(
            self, queue, chance=None, guard=None, weight=100, operator=and_):
        self.queue = queue
        self.weight = weight
        self.operator = operator

        self.__name__ = queue[0].__name__ if queue else 'story'

        guard = guard or self.guard
        if chance:

            def g(param=None):
                test = random.randint(0, 100)
                return False if test >= chance else guard(param)

            self.guard = g

        else:

            self.guard = guard

    def __repr__(self):
        return '<Story "%s">' % self.__name__

    def __call__(self, param=None):
        queue = list(self.queue)
        st = self

        while queue:

            if st.operator is or_:
                choices = [(queue.pop(0), st.weight)]
                operator = st.operator

                while queue and operator is or_:
                    action = queue.pop(0)
                    if isinstance(action, Story):
                        choices.append((action, action.weight))
                        operator = action.operator

                    else:
                        choices.append(action, 0)
                        operator = and_

                action = weighted_choice(choices)

            else:

                action = queue.pop(0)

            if isinstance(action, Story):
                st = action

            if st.guard and not st.guard(param):

                return param

            args = [param] if param else []
            param = action(*args)

        return param

    def __and__(self, s):
        return self.__operation__(s)

    def __or__(self, s):
        return self.__operation__(s, or_)

    def __operation__(self, st, operator=and_):
        if not isinstance(st, Story):
            raise ValueError('Must be instance of Story.')

        st_ = Story(
            list(self.queue), guard=self.guard, weight=self.weight,
            operator=operator)
        st_.queue.append(st)
        return st_


class ActorMeta(type):

    """ Create instance by model. """

    def __call__(cls, model, **params):
        return mixer.blend(model, **params)


Actor = ActorMeta('Actor', (object,), dict())


def weighted_choice(choices):
    """ Randomly choice by weight.

    :return choice:

    """
    total = sum(w for c, w in choices)
    r = random.uniform(0, total)
    upto = 0
    for c, w in choices:
        if upto + w > r:
            return c
        upto += w
    assert False, "Shouldn't get here"
