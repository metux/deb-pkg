__all__ = [ "targetspec", "poolspec", "pkgspec", "config" ]

from config import Config

"""create new global config object and load config file"""
def load(fn):
    cf = Config()
    cf.load(fn)
    return cf
