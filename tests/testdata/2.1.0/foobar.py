
import foobarImplChainsaw
import foobarImplRocket
import foobarImplShotgun

FOOBAR = foobarImplChainsaw.num +\
    foobarImplRocket.num +\
    foobarImplShotgun.num


class Doer(object):

    def __init__(self):
        self.version = 1

    def do(self):
        return self.version
