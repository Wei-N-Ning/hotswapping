
import types
import sys

import foobarImplChainsaw
import foobarImplRocket

FOOBAR = foobarImplChainsaw.num + foobarImplRocket.num


class Doer(object):

    def __init__(self):
        self.version = 0

    def do(self):
        return self.version


class Wicked(types.ModuleType):

    def __init__(self, *args, **kwargs):
        super(Wicked, self).__init__(*args, **kwargs)
        self.__file__ = lambda: None


sys.modules['wicked'] = Wicked('wicked')
