""" Integrate with Tornado. """
from __future__ import absolute_import

import time
from datetime import timedelta

import logging
from tornado import gen, log
from tornado.ioloop import IOLoop

from .core import Story


logger = logging.getLogger('Avalon')
logger.addHandler(logging.StreamHandler())
logger.setLevel('INFO')

DEFAULT_TIMEOUT = 5


class Script(object):

    """ Talks stories.

    :param story: :class:`avalon.core.Story`
    :param avalon: :class:`avalon.engine.Avalon`
    :param timeout: timeout in seconds or `datetime.timedelta`
                    Time beetwen store iterations.

    """

    def __init__(self, story, timeout=None):
        self.story = story
        self.avalon = None
        self.timeout = timeout or DEFAULT_TIMEOUT

    @property
    def timeout(self):
        """ Return self timeout. """
        return self._timeout

    @timeout.setter
    def timeout(self, value):
        """ Convert timeout to ms. """
        if isinstance(value, timedelta):
            value = value.days * 3600 * 24 + value.seconds
        self._timeout = value  # noqa

    @gen.coroutine
    def __call__(self, pipe=None):
        """ Make story. """

        logger.info('Talk story: %s', self.story)

        for action, guard in iter(self.story):

            if not guard(pipe):
                continue

            def callback(pipe, callback=None):
                logger.info('Do action: %s', action.__name__)
                args = [pipe] if pipe else []
                try:
                    pipe = action(*args)
                except Exception as e:  # noqa
                    logger.error(e)
                    logger.error(
                        'Script has exceptions. Stop story: %s.', self.story)
                    self.avalon.forget(self)
                    if not self.avalon.io_loop._stopped:  # noqa
                        raise gen.Return('Stopped.')

                callback(pipe)

            pipe = yield gen.Task(callback, pipe)

            yield self.avalon.add_timeout(self.timeout, async=True)

        self.begin()

    def begin(self, timeout=None):
        """ Going to avalon. """

        if not self.avalon:
            raise RuntimeError('The script are not registered.')

        if timeout:
            self.timeout = timeout

        self.avalon.add_timeout(self.timeout, self)


class Avalon(object):

    """ IOLoop. """

    def __init__(self, io_loop=None, spam=False):
        self.io_loop = io_loop or IOLoop.instance()
        self.scripts = set()
        self.spam = False

    def start(self):
        """ Start IOLoop. """
        if not self.scripts:
            raise RuntimeError('Stories hasn\'t been found. Setup them first.')

        logger.info('Start Avalon.')

        for script in list(self.scripts):
            script.begin()

        self.io_loop.start()

    def stop(self):
        """ Stop IOLoop. """
        logger.info('Stop Avalon.')
        self.io_loop.stop()

    def register(self, script, timeout=None):
        """ Register a script in the Avalon.

        :param script: Script or story. If param is story,
                       script will be created.

        :return Script:

        """

        if isinstance(script, Story):
            script = Script(script, timeout=timeout)

        log.access_log.info('Register story: %s', script.story)

        script.avalon = self
        self.scripts.add(script)
        return script

    def rewind(self, seconds=10):
        """ Spam stories.

        Disable timeouts.

        """
        self.spam = True

        def stop():
            logger.info('Stop spam.')
            self.io_loop.stop()

        self.io_loop.add_timeout(time.time() + seconds, stop)
        self.start()

    def forget(self, script):
        """ Remove a script from the Avalon. """
        self.scripts.remove(script)
        if not self.scripts:
            self.stop()

    def add_timeout(self, timeout, callback=None, async=False):
        """ Pause story execution.

        :return object: Callback's result.

        """
        if not callback:
            callback = lambda callback: callback()

        if self.spam:
            timeout = 0

        deadline = time.time() + timeout

        if async:
            return gen.Task(self.io_loop.add_timeout, deadline)

        return self.io_loop.add_timeout(deadline, callback)


avalon = Avalon()
