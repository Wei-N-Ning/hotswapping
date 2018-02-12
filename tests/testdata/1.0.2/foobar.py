
import foobarImplChainsaw
import foobarImplRocket

FOOBAR = foobarImplChainsaw.num + foobarImplRocket.num


class Doer(object):

    def __init__(self):
        self.version = 0

    def do(self):
        return self.version
